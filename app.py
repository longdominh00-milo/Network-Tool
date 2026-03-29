import traceback
import subprocess
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from exec_data import dict_upstream, generate_test_data, generate_comparison_data
from network_tool import get_srv_ips, get_ipaddrs_from_cli
from juniper_optimizer import run_juniper_compare, run_juniper_commit, run_juniper_delete, run_juniper_delete_commit
from config import JUNIPER_DEVICES, ISP_SUGGESTION_KEYWORDS, IPINFO_TOKEN, JUNIPER_USERS, INBOUND_PREFIXES, BGP_COMMUNITIES, DEFAULT_OPTIMIZER_DEVICES, PREFIX_DEVICE_MAPPING
import json
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, as_completed
#from werkzeug.security import check_password_hash, generate_password_hash
from inbound_optimizer import run_inbound_compare, run_inbound_commit

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

#app.config['SECRET_KEY'] = 'ban-nen-thay-doi-chuoi-bi-mat-nay'
CORS(app)

USER_FILE = 'users.json'

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'username' not in session:
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

@app.route('/get-juniper-users')
def get_juniper_users():
    """API trả về danh sách user được phép tối ưu."""
    return jsonify(JUNIPER_USERS)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     #Kiểm tra xem đã có user nào chưa
#     try:
#         with open(USER_FILE, 'r') as f:
#             data = json.load(f)
#         if len(data['users']) > 0:
#             # Nếu đã có user, không cho đăng ký nữa, chuyển về trang login
#             return redirect(url_for('login'))
#     except (IOError, json.JSONDecodeError):
#         # Nếu file chưa có hoặc lỗi, coi như chưa có user
#         pass

#     if request.method == 'POST':
#         data = request.get_json()
#         username = data.get('username')
#         password = data.get('password')

#         if not username or not password:
#             return jsonify({'success': False, 'message': 'Username and password are required.'})

#         # Lưu user mới
#         try:
#             with open(USER_FILE, 'r+') as f:
#                 users_data = json.load(f)
#                 if username in users_data['users']:
#                     return jsonify({'success': False, 'message': 'Username already exists.'})
                
#                 users_data['users'][username] = generate_password_hash(password)
#                 f.seek(0)
#                 json.dump(users_data, f, indent=4)
#         except (IOError, json.JSONDecodeError):
#             # Tạo file mới nếu chưa có
#             users_data = {"users": {username: generate_password_hash(password)}}
#             with open(USER_FILE, 'w') as f:
#                 json.dump(users_data, f, indent=4)

#         return jsonify({'success': True, 'redirect': url_for('login')})

#     # Nếu là request GET, hiển thị trang đăng ký
#     return render_template('register.html')

# --- Route Đăng nhập / Đăng xuất ---
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if 'username' in session:
#         return redirect(url_for('home'))
#     if request.method == 'POST':
#         data = request.get_json()
#         username = data.get('username')
#         password = data.get('password')

#         try:
#             with open(USER_FILE, 'r') as f:
#                 users_data = json.load(f)['users']
#         except IOError:
#             return jsonify({'success': False, 'message': 'User database not found.'})

#         user_hash = users_data.get(username)
#         if user_hash and check_password_hash(user_hash, password):
#             session['username'] = username
#             return jsonify({'success': True, 'redirect': url_for('home')})
#         else:
#             return jsonify({'success': False, 'message': 'Invalid username or password'})
#     return render_template('login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))

@app.route('/')
def home():
    """Phục vụ file index.html từ thư mục 'templates'."""
    return render_template('index.html')

@app.route('/get-predefined-sources')
def get_predefined_sources():
    """API trả về danh sách các upstream đã khai báo."""
    return jsonify(dict_upstream)

@app.route('/get-juniper-devices')
def get_juniper_devices():
    """API trả về danh sách tên các thiết bị Juniper."""
    device_names = list(JUNIPER_DEVICES.keys())
    return jsonify(device_names)

def run_task_on_all_devices(task_function, data, is_inbound=False):
    """
    Hàm helper được cập nhật để chọn đúng nhóm thiết bị dựa trên prefix.
    """
    target_devices = []
    
    if is_inbound:
        # Nếu là tác vụ Inbound, kiểm tra prefix để quyết định target
        dest_prefix = data.get('dest_prefix')
        target_devices = PREFIX_DEVICE_MAPPING.get(dest_prefix, DEFAULT_OPTIMIZER_DEVICES)
        print(f"DEBUG: Inbound task for {dest_prefix}. Targeting devices: {target_devices}")
    else:
        target_devices = DEFAULT_OPTIMIZER_DEVICES
        print(f"DEBUG: Outbound task. Targeting devices: {target_devices}")

    final_output = ""
    overall_status = "success"
    compare_results = []
    
    with ThreadPoolExecutor(max_workers=len(target_devices) or 1) as executor:
        future_to_device = {}
        if is_inbound:
            future_to_device = {
                executor.submit(task_function, device, data.get('dest_prefix'), data.get('upstream_name'), data.get('action'), data.get('username'), data.get('password')): device 
                for device in target_devices
            }
        else:
            future_to_device = {
                executor.submit(task_function, device, data.get('dest'), data.get('upstream'), data.get('username'), data.get('password')): device 
                for device in target_devices
            }
        
        for future in as_completed(future_to_device):
            device_name = future_to_device[future]
            try:
                result = future.result()
                final_output += f"--- LOGS FOR: {device_name} ---\n{result.get('output', 'No output.')}\n\n"
                if result.get('status') == 'error':
                    overall_status = "error"
                if 'compare_result' in result:
                    compare_results.append(result.get('compare_result'))
            except Exception as exc:
                final_output += f"--- FAILED TASK FOR: {device_name} ---\nAn exception occurred: {exc}\n\n"
                overall_status = "error"
    
    final_compare = "\n".join(filter(None, compare_results))
    return {"status": overall_status, "output": final_output.strip(), "compare_result": final_compare}

@app.route('/suggest-isp', methods=['POST'])
def suggest_isp():
    """
    Cập nhật để truy vấn ipinfo.io.
    """
    data = request.get_json()
    dest_ip = data.get('dest_ip')
    if not dest_ip:
        return jsonify({})

    try:
        # URL và tham số mới cho ipinfo.io
        api_url = f"https://ipinfo.io/{dest_ip}/json"
        params = {'token': IPINFO_TOKEN}
        
        response = requests.get(api_url, params=params, timeout=5)
        response.raise_for_status()
        
        ip_data = response.json()
        
        # ipinfo.io dùng trường 'org' cho thông tin AS và ISP
        org_info = ip_data.get('org', '').lower()
        suggestion = None
        
        for keyword, upstream_suggestion in ISP_SUGGESTION_KEYWORDS.items():
            if keyword in org_info:
                suggestion = f"Consider using upstream: {upstream_suggestion}."
                break
        
        # Trả về một object JSON có cấu trúc mới
        return jsonify({
            "org": ip_data.get('org'), # Gửi về trường 'org'
            "country": ip_data.get('country'),
            "suggestion": suggestion
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"API call failed: {e}"})

@app.route('/run-test', methods=['POST'])
def run_test():
    """API nhận yêu cầu, xử lý và chạy test mạng."""
    try:
        params = request.get_json()
        dict_cli_arg = {
            'dest': params.get('dest'), 'option': params.get('option'),
            'source': params.get('source'), 'count': int(params.get('count', 10)),
            'interval': float(params.get('interval', 0.2)),
            'port': params.get('port', '80')
        }
        all_server_ips = get_srv_ips()
        resolved_sources = get_ipaddrs_from_cli(all_server_ips, dict_cli_arg)
        dict_cli_arg['source'] = resolved_sources

        if not resolved_sources:
             return jsonify({'output': 'Error: No valid source IPs found matching your selection.'})

        test_data = generate_test_data(dict_cli_arg)
        return jsonify(test_data)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f"An unexpected server error occurred: {str(e)}"}), 500

@app.route('/run-compare', methods=['POST'])
def run_compare_route():
    data = request.get_json()
    # Chạy hàm compare trên tất cả các thiết bị
    result = run_task_on_all_devices(run_juniper_compare, data)
    # Thêm compare_result vào response, ở đây ta chỉ cần biết có thay đổi hay không
    # Để đơn giản, ta sẽ dựa vào output
    result['compare_result'] = result['output'] 
    return jsonify(result)

@app.route('/run-commit', methods=['POST'])
def run_commit_route():
    data = request.get_json()
    # Chạy hàm commit trên tất cả các thiết bị
    result = run_task_on_all_devices(run_juniper_commit, data)
    return jsonify(result)

@app.route('/run-delete-compare', methods=['POST'])
def run_delete_compare_route():
    """So sánh trước khi xóa tối ưu outbound."""
    data = request.get_json()
    dest_ip = data.get('dest')
    username = data.get('username')
    password = data.get('password')

    final_output = ""
    overall_status = "success"
    compare_results = []

    with ThreadPoolExecutor(max_workers=len(DEFAULT_OPTIMIZER_DEVICES) or 1) as executor:
        future_to_device = {
            executor.submit(run_juniper_delete, device, dest_ip, username, password): device
            for device in DEFAULT_OPTIMIZER_DEVICES
        }
        for future in as_completed(future_to_device):
            device_name = future_to_device[future]
            try:
                result = future.result()
                final_output += f"--- LOGS FOR: {device_name} ---\n{result.get('output', 'No output.')}\n\n"
                if result.get('status') == 'error':
                    overall_status = "error"
                if result.get('compare_result'):
                    compare_results.append(result.get('compare_result'))
            except Exception as exc:
                final_output += f"--- FAILED TASK FOR: {device_name} ---\nAn exception occurred: {exc}\n\n"
                overall_status = "error"

    final_compare = "\n".join(filter(None, compare_results))
    return jsonify({"status": overall_status, "output": final_output.strip(), "compare_result": final_compare})


@app.route('/run-delete-commit', methods=['POST'])
def run_delete_commit_route():
    """Commit xóa tối ưu outbound."""
    data = request.get_json()
    dest_ip = data.get('dest')
    username = data.get('username')
    password = data.get('password')

    final_output = ""
    overall_status = "success"

    with ThreadPoolExecutor(max_workers=len(DEFAULT_OPTIMIZER_DEVICES) or 1) as executor:
        future_to_device = {
            executor.submit(run_juniper_delete_commit, device, dest_ip, username, password): device
            for device in DEFAULT_OPTIMIZER_DEVICES
        }
        for future in as_completed(future_to_device):
            device_name = future_to_device[future]
            try:
                result = future.result()
                final_output += f"--- LOGS FOR: {device_name} ---\n{result.get('output', 'No output.')}\n\n"
                if result.get('status') == 'error':
                    overall_status = "error"
            except Exception as exc:
                final_output += f"--- FAILED TASK FOR: {device_name} ---\nAn exception occurred: {exc}\n\n"
                overall_status = "error"

    return jsonify({"status": overall_status, "output": final_output.strip()})
    
@app.route('/run-ip-comparison', methods=['POST'])
def run_ip_comparison():
    try:
        params = request.get_json()
        dest = params.get('dest')
        source_ips = params.get('source_ips') # Nhận một list 2 IP
        count = int(params.get('count', 10))
        interval = float(params.get('interval', 0.2))

        if not all([dest, source_ips]) or len(source_ips) != 2:
            return jsonify({'error': 'Destination and a list of 2 source IPs are required.'}), 400

        comparison_data = generate_comparison_data(dest, source_ips, count, interval)
        return jsonify(comparison_data)
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f"An unexpected server error occurred: {str(e)}"}), 500
    
@app.route('/run-nslookup', methods=['POST'])
def run_nslookup():
    """
    Cập nhật để thực thi nslookup với một DNS server cụ thể.
    """
    data = request.get_json()
    domain = data.get('domain')
    dns_server = data.get('server') # Lấy tham số server mới

    if not domain:
        return jsonify({'error': 'Domain name is required.'}), 400
    
    # Xây dựng câu lệnh an toàn
    command_args = ['nslookup', domain]
    # Nếu người dùng cung cấp DNS server, thêm nó vào câu lệnh
    if dns_server:
        # Kiểm tra đơn giản để tránh inject
        if any(char in dns_server for char in ";&|`$()"):
             return jsonify({'error': 'Invalid DNS server format.'}), 400
        command_args.append(dns_server)

    try:
        result = subprocess.run(
            command_args, # Dùng list các tham số
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
        full_output = result.stdout + result.stderr
        return jsonify({'output': full_output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-inbound-prefixes')
def get_inbound_prefixes():
    return jsonify(INBOUND_PREFIXES)

@app.route('/get-bgp-communities')
def get_bgp_communities():
    return jsonify(BGP_COMMUNITIES)

@app.route('/run-inbound-compare', methods=['POST'])
def run_inbound_compare_route():
    data = request.get_json()
    # Chạy trên tất cả các thiết bị
    results = run_task_on_all_devices(run_inbound_compare, data, is_inbound=True)
    return jsonify(results)

@app.route('/run-inbound-commit', methods=['POST'])
def run_inbound_commit_route():
    data = request.get_json()
    # Chạy trên tất cả các thiết bị
    results = run_task_on_all_devices(run_inbound_commit, data, is_inbound=True)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)