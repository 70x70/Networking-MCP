import os
import json
import datetime
from mcp.server.mcpserver import MCPServer
from netmiko import ConnectHandler

mcp = MCPServer("NetworkAutomationEngine")
INVENTORY_FILE = "inventory.json"

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def get_ssh_session(device_name: str):
    inventory = load_inventory()
    if device_name not in inventory:
        raise ValueError(f"Device '{device_name}' not found in inventory.")
    
    info = inventory[device_name]
    device_type = info.get("device_type")
    
    if not device_type:
        raise ValueError(f"Device '{device_name}' is missing a 'device_type' parameter in inventory.json.")

    return ConnectHandler(
        device_type=device_type,
        host=info["host"],
        username=info.get("username", "admin"),
        password=info.get("password", ""),
        port=info.get("port", 22)
    )

def backup_device_state(device_name: str, ssh, device_type: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if "huawei" in device_type:
        raw_config = ssh.send_command("display current-configuration")
        ext = "cfg"
    elif "cisco" in device_type or "ios" in device_type:
        raw_config = ssh.send_command("show running-config")
        ext = "cfg"
    else:
        raw_config = ssh.send_command("/export")
        ext = "rsc"
    
    os.makedirs("backups", exist_ok=True)
    backup_path = f"backups/{device_name}_{timestamp}.{ext}"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(raw_config)
    return backup_path

@mcp.tool()
def list_inventory() -> str:
    
    return json.dumps(load_inventory(), indent=2)

@mcp.tool()
def run_diagnostic(device_name: str, command: str) -> str:
    
    try:
        with get_ssh_session(device_name) as ssh:
            output = ssh.send_command(command)
            return f"[{device_name}] Output:\n{output}"
    except Exception as e:
        return f"[{device_name}] Connection error: {str(e)}"

@mcp.tool()
def deploy_config(device_name: str, commands_json: str) -> str:
    
    inventory = load_inventory()
    device_type = inventory.get(device_name, {}).get("device_type", "")
    cmds = json.loads(commands_json)
    
    try:
        with get_ssh_session(device_name) as ssh:
            backup_file = backup_device_state(device_name, ssh, device_type)
            
            output = ""
            for cmd in cmds:
                output += f"Running: {cmd}\n"
                output += ssh.send_command(cmd) + "\n"
                
            return f"[{device_name}] Deployment successful.\nBackup saved to: {backup_file}\n\nLog:\n{output}"
    except Exception as e:
        return f"[{device_name}] Deployment failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()