import re
from netmiko import ConnectHandler
from config import JUNIPER_DEVICES, BGP_COMMUNITIES

def _get_device_connection_info(device_name, username, password):
    if device_name not in JUNIPER_DEVICES:
        return None
    device_config = JUNIPER_DEVICES[device_name].copy()
    device_config.update({'username': username, 'password': password})
    return device_config

def get_current_communities(net_connect, dest_prefix):
    try:
        command = f"show configuration routing-options static route {dest_prefix} | display set"
        output = net_connect.send_command(command, expect_string=r'#|>')
        communities = re.findall(r'community\s+(\S+)', output)
        return set(communities)
    except Exception as e:
        print(f"Could not get current communities for {dest_prefix}: {e}")
        return set()

def generate_inbound_commands(net_connect, dest_prefix, upstream_name, action):
    current_communities = get_current_communities(net_connect, dest_prefix)
    all_communities_for_upstream = {v['community'] for v in BGP_COMMUNITIES.get(upstream_name, {}).values()}
    target_community = BGP_COMMUNITIES.get(upstream_name, {}).get(action, {}).get('community')
    
    if not target_community:
        return None, f"Action '{action}' for upstream '{upstream_name}' is not defined in config."

    commands = []
    
    # 1. Delete old community in interactive upstream
    for comm in current_communities:
        if comm in all_communities_for_upstream and comm != target_community:
            commands.append(f"delete routing-options static route {dest_prefix} community {comm}")

    # 2. Logic
    if action == "announce":
        prepend_comm = BGP_COMMUNITIES[upstream_name]['prepend']['community']
        no_announce_comm = BGP_COMMUNITIES[upstream_name]['do_not_announce']['community']
        if prepend_comm in current_communities:
            commands.append(f"delete routing-options static route {dest_prefix} community {prepend_comm}")
        if no_announce_comm in current_communities:
             commands.append(f"delete routing-options static route {dest_prefix} community {no_announce_comm}")

    elif action == "prepend":
        no_announce_comm = BGP_COMMUNITIES[upstream_name]['do_not_announce']['community']
        if no_announce_comm in current_communities:
            commands.append(f"delete routing-options static route {dest_prefix} community {no_announce_comm}")
    elif action == "do_not_announce":
        announce_comm = BGP_COMMUNITIES[upstream_name]['announce']['community']
        if announce_comm in current_communities:
            commands.append(f"rollback")

    # 3. Add new community
    if target_community not in current_communities:
        commands.append(f"set routing-options static route {dest_prefix} community {target_community}")
        # Static route discard
        commands.append(f"set routing-options static route {dest_prefix} discard")

    if not commands:
        return [], f"Destination {dest_prefix} is already configured for this action."
        
    return commands, f"Generated commands to apply '{action}' on '{upstream_name}' for '{dest_prefix}'."


def run_inbound_compare(device_name, dest_prefix, upstream_name, action, username, password):
    device_config = _get_device_connection_info(device_name, username, password)
    if not device_config: return {"status": "error", "output": "Invalid device."}
    
    output_log = ""
    try:
        with ConnectHandler(**device_config) as net_connect:
            final_commands, message = generate_inbound_commands(net_connect, dest_prefix, upstream_name, action)
            if not final_commands:
                return {"status": "success", "output": message, "compare_result": ""}
            
            output_log += f"Connecting to {device_config['host']} for compare...\n"
            output_log += "Entering 'configure private' mode...\n"
            net_connect.config_mode(config_command='configure private')

            output_log += "Sending commands to candidate config...\n"
            for cmd in final_commands:
                net_connect.send_command_timing(cmd)
                output_log += f"> {cmd}\n"
            
            output_log += "\nRunning 'show | compare'...\n\n"
            compare_output = net_connect.send_command_timing("show | compare")
            output_log += "--- COMPARE RESULT ---\n" + compare_output + "\n--- END COMPARE ---\n"

            output_log += "\nDiscarding changes with 'rollback 0'..."
            net_connect.send_command_timing("rollback 0")
            net_connect.exit_config_mode()
            
            return {"status": "success", "output": output_log, "compare_result": compare_output}
    except Exception as e:
        return {"status": "error", "output": f"An error occurred during compare: {e}"}

def run_inbound_commit(device_name, dest_prefix, upstream_name, action, username, password):
    device_config = _get_device_connection_info(device_name, username, password)
    if not device_config: return {"status": "error", "output": "Invalid device."}
    
    output_log = ""
    try:
        with ConnectHandler(**device_config) as net_connect:
            final_commands, message = generate_inbound_commands(net_connect, dest_prefix, upstream_name, action)
            if not final_commands:
                return {"status": "success", "output": message}

            output_log += f"Connecting to {device_config['host']} to commit...\n"
            output_log += "Entering 'configure private' mode...\n"
            net_connect.config_mode(config_command='configure private')

            output_log += "Re-sending commands...\n"
            for cmd in final_commands:
                net_connect.send_command_timing(cmd)
                output_log += f"> {cmd}\n"
            
            output_log += "\nCommitting changes...\n"
            commit_output = net_connect.commit(comment=f"NetTool: Set BGP community for {dest_prefix}")
            output_log += f"Commit output:\n{commit_output}"

            if "commit complete" in commit_output.lower():
                return {"status": "success", "output": output_log}
            else:
                return {"status": "error", "output": output_log}
    except Exception as e:
        return {"status": "error", "output": f"An error occurred during commit: {e}"}