import socket
import threading
import time
from config import SERVER_HOST, SERVER_PORT, TIMEOUT

clients = {} # lưu thông tin của client dưới dạng {addr: last_heartbeat}

def handle_client(client_socket, addr):
    # xử lý từng client
    print(f"[+] {addr} connected")
    clients[addr] = time.time() # cập nhật thời gian kết nối

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if data == "heartbeat":
                clients[addr] = time.time() # cập nhật thời gian nhật heartbeat
    except:
        pass
    finally:
        print(f"[-] {addr} disconnected")
        del clients[addr]
        client_socket.close()
    
def remove_inactive_clients():
    # xóa client không gửi heartbeat sau TIMEOUT giây
    while True:
        time.sleep(1)
        current_time = time.time()
        for addr in list(clients.keys()):
            if current_time - clients[addr] > TIMEOUT:
                print(f"[!] removing inactive client {addr}")
                del clients[addr]

def start_server():
    # khởi động server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"[*] server is listening on {SERVER_HOST}:{SERVER_PORT}")

    threading.Thread(target=remove_inactive_clients, daemon=True).start()

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()


"""
Tóm tắt luồng hoạt động
- khi server khởi động
    tạo 1 socket TCP, bind vào IP và cổng
    lắng nghe các kết nối từ client
    chạy 1 luồng riêng để kiểm tra và xóa các client không phản hồi
- khi client kết nối
    server chấp nhận kết nối
    tạo 1 luồng mới để xử lý client
    lưu client vào danh sách theo dõi
- khi client gửi dữ liệu
    nếu nhận được heartbeat, cập nhật thời gian cuối cùng client hoạt động
    nếu client không phản hồi trong TIMEOUT giây, server xóa client khỏi danh sách
- khi client ngắt kết nối
    xóa client khỏi danh sách
    đóng kết nối
"""