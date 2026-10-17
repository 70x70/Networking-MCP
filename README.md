> ⚠️ **Important Note:** This tool interacts with all network devices via **SSH only**. Make sure SSH is enabled and accessible on your target gear before testing commands.
# Multi-Vendor Network Automation MCP Server

Manage, configure, and automate multi-vendor networks (**Cisco**, **MikroTik**, **Huawei**, **Juniper**) using natural language. Connect this Python MCP server to **Claude Desktop** or **Cursor** (any MCP client works great, but I have included the most popular ones) to execute bulk tasks and complex configurations across dozens of routers and switches at once.

## 1. Prerequisites

First, ensure you have Python installed along with the required libraries:

```
pip install mcp netmiko fastmcp

```

## 2. Inventory & Server Setup

## Define `inventory.json`
Remember all Roles Are Not Required  This is Only an Example , you can more routers & switches 


```
{
  "cisco-access-sw": {
    "host": "192.168.1.10",
    "device_type": "cisco_ios",
    "username": "admin",
    "password": "your_cisco_password",
    "role": "access-switch"
  },
  "cisco-core-router": {
    "host": "192.168.1.1",
    "device_type": "cisco_xe",
    "username": "admin",
    "password": "your_cisco_password",
    "role": "core-router"
  },
  "cisco-nexus-switch": {
    "host": "192.168.1.20",
    "device_type": "cisco_nxos",
    "username": "admin",
    "password": "your_cisco_password",
    "role": "data-center"
  },
  "mikrotik-edge": {
    "host": "192.168.2.1",
    "device_type": "mikrotik_routeros",
    "username": "admin",
    "password": "your_mikrotik_password"
  },
  "huawei-sw-01": {
    "host": "192.168.3.5",
    "device_type": "huawei_vrp",
    "username": "admin",
    "password": "your_huawei_password"
  },
  "juniper-core": {
    "host": "192.168.4.1",
    "device_type": "juniper_junos",
    "username": "admin",
    "password": "your_juniper_password"
  }
}

```

#### Supported Netmiko `device_type` strings:

* **Cisco Catalyst / Access Switches / IOS:** `cisco_ios` Cisco Catalyst 2960, 3750, and ISR 2900 series.
* **Cisco IOS-XE / Enterprise Routers:** `cisco_xe` Cisco ISR 4000, ASR 1000, and Catalyst 9300 series.
* **Cisco Nexus Switches:** `cisco_nxos` Cisco Nexus switches (e.g., Nexus 3000, 5000, 7000, 9000 series).
* **Cisco IOS-XR / Core Routers:** `cisco_xr` Cisco ASR 9000 and NCS 5500 series.
* **MikroTik RouterOS:** `mikrotik_routeros` MikroTik hEX, RouterBoards, Cloud Router Switches (CRS), and Cloud Core Routers (CCR).
* **Huawei VRP:** `huawei_vrp` Huawei CloudEngine switches (e.g., S5700, S6700 series) and AR series enterprise routers.
* **Juniper Junos:** `juniper_junos` Juniper EX series Ethernet switches, SRX series services gateways/firewalls, and MX series edge routers.


## 3. Connecting to Claude Desktop

Claude Desktop connects to local MCP servers by launching the script via stdio.

### Step 1: Open the Claude Desktop Configuration

File ==> Settings ===> Developer ===> Edit config

### Step 2: Add Your MCP Server Configuration

Edit the file to add `Networking-MCP` under `mcpServers`. Make sure to provide the **full absolute path** to your Python executable and `server.py`:

#### **Windows Example (`claude_desktop_config.json`):**  

```
{
  "mcpServers": {
    "NetworkAutomationEngine": {
      "command": "python",
      "args": [
        "C:/Users/YourUsername/Networking-MCP/server.py"
      ]
    }
  }
}

```

#### **macOS / Linux Example (`claude_desktop_config.json`):**

```
{
  "mcpServers": {
    "NetworkAutomationEngine": {
      "command": "python3",
      "args": [
        "/Users/yourusername/Networking-MCP/server.py"
      ]
    }
  }
}

```

> **Note:** If you are using a virtual environment (e.g., `venv`), point `"command"` directly to the virtual environment's Python binary (e.g., `"C:/Users/YourUsername/NetworkAutomation/venv/Scripts/python.exe"` or `"/Users/yourusername/NetworkAutomation/venv/bin/python"`).



## 4. Connecting to Cursor 

If you use Cursor alongside Claude Desktop, you can configure Cursor to run the server as well.

Locate your Cursor MCP config file:



```
{
  "mcpServers": {
    "NetworkAutomationEngine": {
      "command": "python",
      "args": ["C:/Users/YourUsername/Networking-MCP/server.py"]
    }
  }
}

```

## 5. Usage Examples

Once connected, ask Claude or Cursor in natural language:

* **Show inventory:**

  > *"Show me all the devices in my network inventory."*

* **Check interface statuses:**

  > *"Run `show ip interface brief` on cisco-access-sw."*

* **Inspect routing details:**

  > *"Execute `show ip route` on cisco-core-router."*
