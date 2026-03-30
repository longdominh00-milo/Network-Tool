# juniper_optimizer.py
import re
from netmiko import ConnectHandler
from config import JUNIPER_DEVICES, UPSTREAM_PREFIX_LISTS

def _get_device_connection_info(device_name, username, password):
    """Hàm nội bộ để lấy thông tin kết nối."""
    if device_name not in JUNIPER_DEVICES:
        return None
    device_config = JUNIPER_DEVICES[device_name].copy()
    device_config['username'] = username
    device_config['password'] = password
    return device_config

def get_current_upstream(net_connect, dest_ip):
    """
    Hàm mới: Kiểm tra cấu hình hiện tại để tìm xem dest_ip đang thuộc prefix-list nào.
    """
    try:
        # Command show prefix-list contain dest_ip
        command = f"show configuration policy-options | display set | match {dest_ip}"
        output = net_connect.send_command(command, expect_string=r'#|>')
        
        if output:
            # Regex to find prefix-list, ex: "set policy-options prefix-list VIETTEL-Dest ..."
            match = re.search(r'prefix-list\s+(\S+)', output)
            if match:
                current_prefix_list_name = match.group(1)
                # Find upstream from prefix-list
                for upstream_name, prefix_list_name in UPSTREAM_PREFIX_LISTS.items():
                    if prefix_list_name == current_prefix_list_name:
                        return upstream_name
    except Exception:
        pass
    return None

def _generate_commands(net_connect, dest_ip, new_upstream_name):

    # Get new prefix-list from config
    new_prefix_list = UPSTREAM_PREFIX_LISTS.get(new_upstream_name)
    if not new_prefix_list:
        return None, "Upstream is not defined"

    # Check which upstream that dest_ip was optimized
    current_upstream = get_current_upstream(net_connect, dest_ip)
    
    commands = []
    
    if current_upstream == new_upstream_name:
        # If new upstream = old upstream -> Do nothing
        return [], f"Destination {dest_ip} has been optimized via {new_upstream_name}."

    if current_upstream:
        # If it had config to old upstream -> delete
        old_prefix_list = UPSTREAM_PREFIX_LISTS.get(current_upstream)
        if old_prefix_list:
            commands.append(f"delete policy-options prefix-list {old_prefix_list} {dest_ip}")
    
    # set cmd for new optimization
    commands.append(f"set routing-options static route {dest_ip} discard")
    commands.append(f"set policy-options prefix-list {new_prefix_list} {dest_ip}")
    
    return commands, None


def run_juniper_compare(device_name, dest_ip, upstream_name, username, password):
    """Hàm compare được cập nhật để dùng logic mới."""
    device_config = _get_device_connection_info(device_name, username, password)
    if not device_config:
        return {"status": "error", "output": "Invalid device."}

    output_log = ""
    try:
        output_log += f"Connecting to {device_config['host']} to check and compare...\n"
        with ConnectHandler(**device_config) as net_connect:
            output_log += "Successfully connected.\n"
            
            final_commands, message = _generate_commands(net_connect, dest_ip, upstream_name)
            if message: #If nothing to do
                return {"status": "success", "output": message, "compare_result": ""}
            
            # Apply to candidate config and compare
            net_connect.config_mode(config_command='configure private')

            output_log += "Sending commands to candidate config...\n"
            for cmd in final_commands:
                net_connect.send_command_timing(cmd)
                output_log += f"> {cmd}\n"
    
            compare_output = net_connect.send_command_timing("show | compare")
            output_log += "\n--------------- COMPARE RESULT ---------------\n" + compare_output + "\n--------------- END COMPARE ---------------"

            #output_log += "\nDiscarding changes with 'rollback 0'..."
            net_connect.send_command_timing("rollback 0")
            net_connect.exit_config_mode()
            
            return {"status": "success", "output": output_log, "compare_result": compare_output}

    except Exception as e:
        return {"status": "error", "output": f"An error occurred during compare: {e}"}

def run_juniper_commit(device_name, dest_ip, upstream_name, username, password):
    """Hàm commit được cập nhật để dùng logic mới."""
    device_config = _get_device_connection_info(device_name, username, password)
    if not device_config:
        return {"status": "error", "output": "Invalid device."}

    output_log = ""
    try:
        output_log += f"Connecting to {device_config['host']} to commit...\n"
        with ConnectHandler(**device_config) as net_connect:
            final_commands, message = _generate_commands(net_connect, dest_ip, upstream_name)
            if message:
                return {"status": "success", "output": message}
            
            net_connect.config_mode(config_command='configure private')

            #output_log += "Re-sending commands...\n"
            for cmd in final_commands:
                net_connect.send_command_timing(cmd)
                #output_log += f"> {cmd}\n"
            
            #output_log += "\nCommitting changes...\n"
            commit_output = net_connect.commit(comment=f"NetTool: Optimize {dest_ip} via {upstream_name}")
            output_log += f"{commit_output}" + "\n ================================================================"

            if "commit complete" in commit_output.lower():
                return {"status": "success", "output": output_log}
            else:
                return {"status": "error", "output": output_log}

    except Exception as e:
        return {"status": "error", "output": f"An error occurred during commit: {e}"}


def run_juniper_delete(device_name, dest_ip, username, password):
    """Xóa tối ưu outbound: xóa static route discard và xóa dest khỏi prefix-list hiện tại."""
    device_config = _get_device_connection_info(device_name, username, password)
    if not device_config:
        return {"status": "error", "output": "Invalid device."}

    output_log = ""
    try:
        output_log += f"Connecting to {device_config['host']} to delete optimization...\n"
        with ConnectHandler(**device_config) as net_connect:
            output_log += "Successfully connected.\n"

            # Tìm upstream hiện tại của dest_ip
            current_upstream = get_current_upstream(net_connect, dest_ip)

            commands = []
            commands.append(f"delete routing-options static route {dest_ip} discard")

            if current_upstream:
                old_prefix_list = UPSTREAM_PREFIX_LISTS.get(current_upstream)
                if old_prefix_list:
                    commands.append(f"delete policy-options prefix-list {old_prefix_list} {dest_ip}")
                    output_log += f"Found existing optimization via {current_upstream} (prefix-list: {old_prefix_list}).\n"
            else:
                output_log += "No existing prefix-list optimization found for this destination.\n"

            # Vào configure private, show compare trước
            net_connect.config_mode(config_command='configure private')
            output_log += "Sending delete commands to candidate config...\n"
            for cmd in commands:
                net_connect.send_command_timing(cmd)
                output_log += f"> {cmd}\n"

            compare_output = net_connect.send_command_timing("show | compare")
            output_log += "\n--------------- COMPARE RESULT ---------------\n" + compare_output + "\n--------------- END COMPARE ---------------"

            net_connect.send_command_timing("rollback 0")
            net_connect.exit_config_mode()

            return {"status": "success", "output": output_log, "compare_result": compare_output, "commands": commands}

    except Exception as e:
        return {"status": "error", "output": f"An error occurred during delete compare: {e}"}


def run_juniper_delete_commit(device_name, dest_ip, username, password):
    """Commit lệnh xóa tối ưu outbound."""
    device_config = _get_device_connection_info(device_name, username, password)
    if not device_config:
        return {"status": "error", "output": "Invalid device."}

    output_log = ""
    try:
        output_log += f"Connecting to {device_config['host']} to commit delete...\n"
        with ConnectHandler(**device_config) as net_connect:
            current_upstream = get_current_upstream(net_connect, dest_ip)

            commands = []
            commands.append(f"delete routing-options static route {dest_ip} discard")
            if current_upstream:
                old_prefix_list = UPSTREAM_PREFIX_LISTS.get(current_upstream)
                if old_prefix_list:
                    commands.append(f"delete policy-options prefix-list {old_prefix_list} {dest_ip}")

            net_connect.config_mode(config_command='configure private')
            for cmd in commands:
                net_connect.send_command_timing(cmd)

            commit_output = net_connect.commit(comment=f"NetTool: Delete optimization for {dest_ip}")
            output_log += f"{commit_output}\n ================================================================"

            if "commit complete" in commit_output.lower():
                return {"status": "success", "output": output_log}
            else:
                return {"status": "error", "output": output_log}

    except Exception as e:
        return {"status": "error", "output": f"An error occurred during delete commit: {e}"}