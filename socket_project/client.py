import socket
import time
from config import SERVER_HOST, SERVER_PORT, HEARTBEAT_INTERVAL

def start_client(): 
    # kết nối  đến server và gửi heartbeat định kỳ
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    print("[+] connected to server")

    try:
        while True:
            time.sleep(HEARTBEAT_INTERVAL)
            client.send("heartbeat".encode()) # gửi tín hiệu sống
    except:
        print("[-] connection lost")
        client.close()

if __name__ == "__main__":
    start_client()

"""
tóm tắt luồng hoạt động:
- client khởi động: 
    tạo socket TCP
    kết nối đến server
    in ra thông báo kết nối thành công
- gửi heartbeat định kỳ
    mỗi HEARTBEAT_INTERVAL giây, client gửi heartbeat đến server để đảm bảo nó vẫn hoạt động
- nếu mất kết nối
    nếu server đóng kết nối hoặc mất kết nối, client in ra connection lost và đóng socket
"""