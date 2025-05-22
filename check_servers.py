import socket
import time

def check_server(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 2 seconds timeout
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def check_all_servers():
    servers = [
        {"id": 0, "ip": "127.0.0.1", "port": 1069, "type": "Primary"},
        {"id": 1, "ip": "127.0.0.1", "port": 1070, "type": "Backup"}
    ]
    
    print("\nChecking server status...")
    print("-" * 50)
    print("Server\t\tPort\t\tStatus")
    print("-" * 50)
    
    for server in servers:
        is_up = check_server(server["ip"], server["port"])
        status = "UP 🟢" if is_up else "DOWN 🔴"
        print(f"{server['type']}\t\t{server['port']}\t\t{status}")
    print("-" * 50)

if __name__ == "__main__":
    check_all_servers()
