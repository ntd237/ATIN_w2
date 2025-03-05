import socket

# tạo socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('127.0.0.1', 12345))

print("server udp đang chờ dữ liệu...")

while True:
    data, addr = server_socket.recvfrom(1024)
    print(f"dữ liệu nhận từ {addr}: {data.decode()}")

    # gửi phản hồi
    server_socket.sendto("received!".encode(), addr)

'''
tóm tắt luồng hoạt động
- Tạo socket UDP
- Gán địa chỉ IP và cổng (bind())
- Server lắng nghe dữ liệu từ client (recvfrom())
- Khi nhận được dữ liệu, in ra màn hình
- Gửi phản hồi lại client (sendto())
- Server tiếp tục chạy, sẵn sàng nhận dữ liệu tiếp theo
'''


