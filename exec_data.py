import subprocess
from concurrent.futures import ThreadPoolExecutor
import ipaddress
import shlex

dict_upstream = {
    'IPTP-SG (119.17.238.0)': '119.17.238.0',
    'IPTP-HKG (101.53.63.0)': '101.53.63.0',
    'NTT-HKG (101.53.55.0)': '101.53.55.0',
    '101.53.54.0/24': '101.53.54.0',
    '101.53.59.0/24': '101.53.59.0',
    'VIETTEL-QT (101.53.60.0)': '101.53.60.0',
    'CMC-QT (101.53.50.0)': '101.53.50.0',
    'FTTx-Viettel (27.74.240.151)': '10.20.12.0',
    'FTTx-VNPT (14.161.9.165)': '10.20.13.0',
    'LUMEN-HK (101.53.46.0)': '101.53.46.0',
    'LUMEN-SGP (101.53.48.0)': '101.53.48.0',
    'VNPT-QT (119.15.178.0)': '119.15.178.0',
    'HCL (154.81.60.0/24)': '10.20.22.0',
    'TMF (202.9.79.0/24)': '10.20.23.0',
    'TMA (103.199.6.0/24)': '10.20.24.0',
    'OFFICE (101.53.2.0/24)': '101.53.2.0',
    'ISHCMC (103.104.24.0/24)': '103.104.24.0',
    'GGC (101.53.58.0/24)': '101.53.58.0',
    '101.53.1.0/24': '101.53.1.0',  
    '101.53.3.0/24': '101.53.3.0',  
    '101.53.4.0/24': '101.53.4.0',
    '101.53.5.0/24': '101.53.5.0',
    '101.53.6.0/24': '101.53.6.0',
    '101.53.7.0/24': '101.53.7.0', 
    '101.53.8.0/24': '101.53.8.0', 
    '101.53.9.0/24': '101.53.9.0',
    '101.53.10.0/24': '101.53.10.0',
    '101.53.11.0/24': '101.53.11.0',
    '101.53.12.0/24': '101.53.12.0',
    '101.53.13.0/24': '101.53.13.0',
    '101.53.14.0/24': '101.53.14.0',
    '101.53.15.0/24': '101.53.15.0',
    '101.53.16.0/24': '101.53.16.0',
    '101.53.17.0/24': '101.53.17.0',
    '101.53.18.0/24': '101.53.18.0',
    '101.53.19.0/24': '101.53.19.0',
    '101.53.20.0/24': '101.53.20.0',
    '101.53.21.0/24': '101.53.21.0',
    '101.53.22.0/24': '101.53.22.0',
    '101.53.23.0/24': '101.53.23.0',
    '101.53.24.0/24': '101.53.24.0',
    '101.53.25.0/24': '101.53.25.0',
    '101.53.26.0/24': '101.53.26.0',
    '101.53.27.0/24': '101.53.27.0',
    '101.53.28.0/24': '101.53.28.0',
    '101.53.29.0/24': '101.53.29.0',
    '101.53.30.0/24': '101.53.30.0',
    '101.53.31.0/24': '101.53.31.0',
    '101.53.32.0/24': '101.53.32.0',
    '101.53.33.0/24': '101.53.33.0',
    '101.53.34.0/24': '101.53.34.0',
    '101.53.35.0/24': '101.53.35.0',
    '101.53.36.0/24': '101.53.36.0',
    '101.53.37.0/24': '101.53.37.0',
    '101.53.38.0/24': '101.53.38.0',
    '101.53.39.0/24': '101.53.39.0',
    '101.53.40.0/24': '101.53.40.0',
    '101.53.41.0/24': '101.53.41.0',
    '101.53.42.0/24': '101.53.42.0',
    '101.53.43.0/24': '101.53.43.0',
    '101.53.44.0/24': '101.53.44.0',
    '101.53.45.0/24': '101.53.45.0', 
    '101.53.47.0/24': '101.53.47.0',
    '101.53.49.0/24': '101.53.49.0',
    '101.53.51.0/24': '101.53.51.0',    
    '101.53.52.0/24': '101.53.52.0',
    '101.53.53.0/24': '101.53.53.0',
    '101.53.56.0/24': '101.53.56.0',
    '101.53.61.0/24': '101.53.61.0',
    '101.53.62.0/24': '101.53.62.0',
    '103.88.122.0/24': '103.88.122.0',
    '119.15.176.0/24': '119.15.176.0',
    '119.15.177.0/24': '119.15.177.0',
    '119.15.179.0/24': '119.15.179.0',
    '119.15.180.0/24': '119.15.180.0',
    '119.15.181.0/24': '119.15.181.0',
    '119.15.185.0/24': '119.15.185.0',
    '119.15.188.0/24': '119.15.188.0',
    '119.15.190.0/24': '119.15.190.0',
    '119.15.191.0/24': '119.15.191.0',
    '119.17.229.0/24': '119.17.229.0',
    '119.17.232.0/24': '119.17.232.0',
    '119.17.234.0/24': '119.17.234.0',
    '119.17.235.0/24': '119.17.235.0',
    '119.17.236.0/24': '119.17.236.0',
    '119.17.237.0/24': '119.17.237.0',
    '119.17.239.0/24': '119.17.239.0',
    '119.17.240.0/24': '119.17.240.0',
    '119.17.241.0/24': '119.17.241.0',
    '119.17.247.0/24': '119.17.247.0',
    '119.17.249.0/24': '119.17.249.0',
    '119.17.252.0/24': '119.17.252.0',
    '119.17.254.0/24': '119.17.254.0',
    '202.151.170.0/24': '202.151.170.0',
    '202.151.171.0/24': '202.151.171.0',
    '202.151.172.0/24': '202.151.172.0',
    '202.151.173.0/24': '202.151.173.0',
    '202.151.174.0/24': '202.151.174.0',
    '202.151.175.0/24': '202.151.175.0',
    '202.151.175.0/24': '202.151.175.0',
    '210.86.227.0/24': '210.86.227.0',
    '210.86.234.0/24': '210.86.234.0',
    '210.86.235.0/24': '210.86.235.0',
    '210.86.237.0/24': '210.86.237.0',
    '210.86.238.0/24': '210.86.238.0'
}

def get_key(source_ip):
    """
    Tìm và trả về TÊN upstream (key) tương ứng với một địa chỉ IP.
    Nếu không tìm thấy, trả về chính địa chỉ IP đó.
    """
    try:
        ip_obj = ipaddress.ip_address(source_ip)
        for name, subnet_str in dict_upstream.items():
            # Xử lý subnet để đảm bảo nó hợp lệ
            if '/' not in subnet_str:
                subnet_str += '/24'
            network = ipaddress.ip_network(subnet_str, strict=False)

            if ip_obj in network:
                return name # <-- CHỈ TRẢ VỀ TÊN (KEY)
    except ValueError:
        pass # Bỏ qua nếu IP không hợp lệ
    
    return source_ip

def get_row_labels(source_list):
    row_labels = [get_key(ip) for ip in source_list]
    return row_labels

def exce_test_result(cmd):
    try:
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf-8')
        (output, err) = result.communicate()
        if result.returncode == 0:
            return output.split('\n')
        else:
            # Gộp cả stderr vào output để debug
            return (output + err).split('\n')
    except Exception:
        return False

def generate_test_data(dict_cli_arg):
    """
    Hàm chính để chạy các bài test, xử lý đa luồng, phân tích kết quả,
    và trả về dữ liệu có cấu trúc JSON cho frontend.
    """
    # Lấy các tham số từ input
    option = dict_cli_arg.get('option')
    count = dict_cli_arg.get('count')
    interval = dict_cli_arg.get('interval')
    dest = dict_cli_arg.get('dest')
    source_list = dict_cli_arg.get('source')
    port = dict_cli_arg.get('port', '443') # Mặc định port 443 cho tcppping
    
    row_labels = get_row_labels(source_list)

    def run_single_test(task):
        """
        Hàm worker được chạy trong mỗi luồng (thread), thực hiện một bài test duy nhất.
        """
        source = task['source']
        cmd = ''
        
        # Xây dựng câu lệnh dựa trên loại test
        if task['option'] == 'ping':
            source_cmd_part = f"-I {source}" if source and source != 'default_route' else ""
            cmd = f"ping {task['dest']} {source_cmd_part} -c {task['count']} -i {task['interval']} -q"
        
        elif task['option'] == 'tcppping':
            source_cmd_part = f"-a {source}" if source and source != 'default_route' else ""
            # Dùng sudo hping3 với các tham số cần thiết
            cmd = f"sudo hping3 -S {task['dest']} -p {task['port']} -c {task['count']} {source_cmd_part}"

        elif task['option'] == 'mtr':
            source_cmd_part = f"-a {source}" if source and source != 'default_route' else ""
            cmd = f"mtr {task['dest']} {source_cmd_part} -c {task['count']} -i {task['interval']} -n -z --report"
        
        elif task['option'] == 'traceroute':
            source_cmd_part = f"-s {source}" if source and source != 'default_route' else ""
            cmd = f"traceroute {source_cmd_part} {task['dest']}"
        
        # Chạy lệnh và trả về kết quả thô
        raw_output = exce_test_result(cmd)
        # Gán nhãn vào kết quả để xử lý sau này
        return (task['row_label'], raw_output, cmd)

    # Tạo danh sách các tác vụ cần thực hiện
    tasks = []
    for source, label in zip(source_list, row_labels):
        tasks.append({
            'source': source, 'row_label': label,
            'dest': dest, 'option': option,
            'count': count, 'interval': interval,
            'port': port
        })
    
    # Chạy các tác vụ đồng thời
    with ThreadPoolExecutor(max_workers=len(tasks) or 1) as executor:
        results_from_threads = list(executor.map(run_single_test, tasks))

    headers = []
    rows = []

    # Xử lý kết quả trả về từ các luồng
    if option == 'ping':
        headers = ["Source", "TX/RX", "Loss", "Avg", "Min", "Max", "Mdev"]
        for row_label, result, _ in results_from_threads:
            # Khởi tạo giá trị mặc định
            row_data = {"Source": row_label, "TX/RX": "N/A", "Loss": 100.0, "Avg": "N/A", "Min": "N/A", "Max": "N/A", "Mdev": "N/A"}
            if result:
                for line in result:
                    if 'packets transmitted' in line:
                        stats = line.split(', ')
                        if len(stats) >= 3:
                            row_data["TX/RX"] = f"{stats[0].split(' ')[0]}/{stats[1].split(' ')[0]}"
                            row_data["Loss"] = float(stats[2].split(' ')[0].replace('%',''))
                    elif 'rtt min/avg/max/mdev' in line:
                        rtt_parts = line.split('=')[-1].strip().split(' ')[0].split('/')
                        if len(rtt_parts) == 4:
                            row_data["Min"] = float(rtt_parts[0])
                            row_data["Avg"] = float(rtt_parts[1])
                            row_data["Max"] = float(rtt_parts[2])
                            row_data["Mdev"] = float(rtt_parts[3])
            rows.append(row_data)

    elif option == 'tcppping':
        headers = ["Source", "Destination", "Port", "Status", "Avg RTT"]
        for row_label, result, _ in results_from_threads:
            status = "Filtered (No Reply)"
            avg_rtt = "N/A"
            if result:
                rtt_values = [float(rtt) for rtt in re.findall(r'rtt=([\d\.]+)', "".join(result))]
                if rtt_values:
                    avg_rtt = f"{sum(rtt_values) / len(rtt_values):.2f} ms"
                if "flags=SA" in "".join(result): status = "Open"
                elif "flags=RA" in "".join(result): status = "Closed (Refused)"
            rows.append({"Source": row_label, "Destination": dest, "Port": port, "Status": status, "Avg RTT": avg_rtt})
    
    elif option in ['mtr', 'traceroute']:
        headers = ["Source", "Output"]
        for row_label, result, _ in results_from_threads:
             rows.append({"Source": row_label, "Output": "\n".join(result) if result else "Test failed."})

    # Lấy câu lệnh đã thực thi để hiển thị trên UI
    executed_command = ""
    if len(results_from_threads) == 1:
        # Lấy câu lệnh từ kết quả trả về của luồng duy nhất
        _, _, executed_command = results_from_threads[0]
        
    return {"headers": headers, "rows": rows, "executed_command": executed_command}

def generate_comparison_data(dest, source_ips, count, interval):
    """
    Chạy ping, mtr, traceroute đồng thời từ 2 IP nguồn và trả về kết quả có cấu trúc.
    """
    tasks = []
    test_types = ['ping', 'mtr', 'traceroute']
    for ip in source_ips:
        for test_type in test_types:
            tasks.append({'option': test_type, 'dest': dest, 'source': ip, 'count': count, 'interval': interval})

    def run_single_test(task):
        """Worker function cho ThreadPool."""
        cmd = ''
        source = task['source']
        if task['option'] == 'ping':
            cmd = f"ping {task['dest']} -I {source} -c {task['count']} -i {task['interval']} -q"
        elif task['option'] == 'mtr':
            cmd = f"mtr {task['dest']} -a {source} -c {task['count']} -i {task['interval']} -n -z --report"
        elif task['option'] == 'traceroute':
            cmd = f"traceroute -I -s {source} -n {task['dest']}"
        
        raw_output = exce_test_result(cmd)
        return (task['source'], task['option'], raw_output)

    with ThreadPoolExecutor(max_workers=6) as executor:
        results_from_threads = list(executor.map(run_single_test, tasks))

    # Xử lý và cấu trúc lại kết quả
    temp_results = {}
    for source_ip, option, raw_output in results_from_threads:
        if source_ip not in temp_results:
            temp_results[source_ip] = {}
        
        if option == 'ping' and raw_output and len(raw_output) > 2 and raw_output[-2]:
            try:
                rtt = raw_output[-2].split('=')[-1].split(' ms')[0].strip().split('/')
                stats = raw_output[-3].split(', ')
                temp_results[source_ip]['ping'] = {
                    "loss": float(stats[2].split(' ')[0].replace('%','')),
                    "avg": float(rtt[1]), "min": float(rtt[0]), "max": float(rtt[2])
                }
            except (IndexError, ValueError):
                 temp_results[source_ip]['ping'] = None # Báo lỗi nếu không parse được
        else:
            temp_results[source_ip][option] = "\n".join(raw_output) if raw_output else "Test failed."
    
    # Tạo cấu trúc list cuối cùng với các nhãn
    final_results = [
        {
            "label": "Source IP 1",
            "ip": source_ips[0],
            "results": temp_results.get(source_ips[0], {})
        },
        {
            "label": "Source IP 2",
            "ip": source_ips[1],
            "results": temp_results.get(source_ips[1], {})
        }
    ]
    return final_results
