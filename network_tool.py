import ipaddress
import subprocess
from exec_data import dict_upstream
import re
#Remove .py then symbolic or soft link
def validate_ip_address(address):
    #Check valid IP address
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def get_srv_ips():
    #Funtion get all ip addresses from server linux.

    try:
        # Chạy lệnh 'ip -4 addr' để chỉ lấy thông tin IPv4
        cmd_output = subprocess.check_output(['ip', '-4', 'addr'], encoding='utf-8')
        
        # Dùng regex để tìm tất cả các chuỗi IP (ví dụ: "inet 192.168.1.5/24")
        # và chỉ lấy phần địa chỉ IP
        ip_list = re.findall(r'inet\s+([\d\.]+)', cmd_output)
        
        # Lọc bỏ địa chỉ loopback (127.0.0.1)
        return [ip for ip in ip_list if ip != '127.0.0.1']

    except (subprocess.CalledProcessError, FileNotFoundError):
        # Trả về một danh sách rỗng nếu lệnh thất bại
        print("Warning: Could not execute 'ip addr' command to get server IPs.")
        return []

#def get_prefix _description(list_check):
#    list_result = []
#    for key, value in dict_upstream.items():
#        pass

def get_ipaddrs_from_cli(list_ipaddrs, dict_cli_arg):
    list_source_input = []
    source_request = dict_cli_arg.get('source', [])

    list_to_resolve = []
    # Xử lý các trường hợp input
    if isinstance(source_request, str):
        if source_request == 'all':
            return list_ipaddrs
        elif source_request == 'upstream':
            # --- LOGIC MỚI CHO 'ALL UPSTREAMS' ---
            # Chỉ lấy những entry có key không chứa '/' (tức là có tên riêng)
            list_to_resolve = [value for key, value in dict_upstream.items() if '/' not in key]
        else:
            list_to_resolve = [source_request]
    else:
        # Nếu là list (trường hợp chọn source cụ thể)
        list_to_resolve = source_request

    # Vòng lặp để giải quyết tên/subnet thành IP thực tế
    for item in list_to_resolve:
        # Lấy value từ dict, nếu không có key thì dùng chính item đó (cho trường hợp ad-hoc subnet)
        ip_to_check = dict_upstream.get(item, item)
        
        try:
            # Xử lý để chuỗi luôn là một subnet hợp lệ
            if '/' not in ip_to_check:
                 ip_to_check += '/24'
            network = ipaddress.ip_network(ip_to_check, strict=False)

            found_match = False
            for server_ip in list_ipaddrs:
                if ipaddress.ip_address(server_ip) in network:
                    if server_ip not in list_source_input:
                        list_source_input.append(server_ip)
                    found_match = True
                    # Nếu là upstream có tên (key không chứa '/'), chỉ lấy IP đầu tiên tìm thấy
                    if item in dict_upstream and'/' not in item:
                        break 
            
            if not found_match:
                 print(f"Warning: No matching IP found on server for {item}")

        except ValueError:
            print(f"Warning: Invalid subnet format for {item}")
            
    return list_source_input

def check_network_mapping(declared_networks: dict):
    """
    Kiểm tra một dictionary các lớp mạng khai báo và đối chiếu với IP thực tế trên server.

    Args:
        declared_networks: Một dictionary với key là tên và value là chuỗi subnet (ví dụ: {'cmc-ipt': '101.53.50.0'}).

    Returns:
        Một dictionary chứa kết quả kiểm tra.
    """
    print("--- Bắt đầu kiểm tra lớp mạng ---")
    
    server_ips = get_srv_ips()
    if not server_ips:
        print("Lỗi: Không tìm thấy IP nào trên server.")
        return {}

    print(f"IPs tìm thấy trên server: {server_ips}\n")
    
    results = {}
    for name, subnet_str in declared_networks.items():
        try:
            # Xử lý chuỗi để đảm bảo có CIDR, mặc định là /24 nếu không có
            if '/' not in subnet_str:
                subnet_str += '/24'
            
            # Tạo đối tượng network từ chuỗi
            network = ipaddress.ip_network(subnet_str, strict=False)
            
            matching_ip = None
            for ip in server_ips:
                if ipaddress.ip_address(ip) in network:
                    matching_ip = ip
                    break # Tìm thấy một IP khớp là đủ
            
            results[name] = {
                'declared_subnet': str(network),
                'matching_ip': matching_ip,
                'status': 'OK' if matching_ip else 'ERROR'
            }

        except ValueError as e:
            results[name] = {
                'declared_subnet': subnet_str,
                'matching_ip': None,
                'status': f'INVALID_SUBNET ({e})'
            }
            
    return results

def print_check_results(results: dict):
    """In kết quả kiểm tra ra màn hình một cách dễ đọc."""
    print("--- Kết quả kiểm tra ---")
    for name, result in results.items():
        if result['status'] == 'OK':
            print(f"✅ {name:<15} ({result['declared_subnet']}) -> OK, khớp với IP: {result['matching_ip']}")
        else:
            print(f"❌ {name:<15} ({result['declared_subnet']}) -> LỖI: {result['status']}")

# --- VÍ DỤ CÁCH SỬ DỤNG ---
if __name__ == '__main__':
    # Giả lập dict_upstream từ file exec_data.py
    sample_declared_networks = {
        'cmc-ipt': '101.53.50.0',       # Giả sử IP 101.53.50.10 có trên server
        'viettel-ipt': '101.53.60.0',   # Giả sử không có IP nào của Viettel trên server
        'vnpt-hcm': '119.15.178.254/32',# Giả sử IP này có trên server
        'invalid-net': '999.999.9.9'     # Một subnet không hợp lệ
    }

    # Chạy kiểm tra
    check_results = check_network_mapping(sample_declared_networks)
    
    # In kết quả
    print_check_results(check_results)

if __name__ == "__main__":
    list_ipaddrs = get_srv_ips()    #Get all ip address from server Linux
    from cli_argparse import cli_arguments
    dict_cli_arg = cli_arguments()  #Get input argument from cli whhen run script cli_argprase.py
    dist_source_cli_update = get_ipaddrs_from_cli(list_ipaddrs, dict_cli_arg) #Compare ip from server and cli argument
    dict_cli_arg['source'] = dist_source_cli_update #updated source IP when matching ip server and cli arhument

    from exec_data import display_result_table, display_result_text
    if dict_cli_arg['display'] == 'raw':
        display_result_text(dict_cli_arg)
    else:
        display_result_table(dict_cli_arg)

