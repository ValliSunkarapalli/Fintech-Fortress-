import socket
import time
import os
import platform

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def check_server(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def monitor_servers(interval=5):
    servers = [
        {"id": 0, "ip": "127.0.0.1", "port": 1069, "type": "Primary"},
        {"id": 1, "ip": "127.0.0.1", "port": 1070, "type": "Backup"}
    ]
    
    try:
        while True:
            clear_screen()
            print(f"\nMonitoring servers (updates every {interval} seconds)")
            print(f"Press Ctrl+C to stop")
            print("-" * 50)
            print("Server\t\tPort\t\tStatus")
            print("-" * 50)
            
            for server in servers:
                is_up = check_server(server["ip"], server["port"])
                status = "UP 🟢" if is_up else "DOWN 🔴"
                print(f"{server['type']}\t\t{server['port']}\t\t{status}")
            
            print("-" * 50)
            print(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\nStopping server monitor...")

if __name__ == "__main__":
    monitor_servers()
