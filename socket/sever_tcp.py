import socket

# tạo socket
# socket.socket() tạo 1 socket mới
# socket.AF_INET: chỉ định họ địa chỉ là họ IPv4
# socket.SOCK_STREAM: chỉ định kiểu socket là TCP (giao thức hướng kết nối, đáng tin cậy)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# lắng nghe trên địa chỉ và cổng cụ thể
# bind() gán địa chỉ cho IP và cộng cho serverserver
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(5) # cho phép tối đa 5 kết nối chờ

print("server đang chờ kết nối...")

while True:
    client_socket, addr = server_socket.accept() # chấp nhận kết nối từ client
    print(f"Kết nối từ {addr}")

    # nhận dữ liệu từ client
    # recv(1024) nhận tối đa 1024 byte dữ liệu từ client
    # .decode() chuyển dữ liệu nhận được từ dạng bytes sang dạng string
    data = client_socket.recv(1024).decode()
    print(f"Dữ liệu nhận được: {data}")

    # gửi phản hồi lại client
    # sendall() gửi phản hồi lại cho client
    # .encode() chuyển chuỗi "Hello from server!" sang dạng bytes trước khi gửigửi
    client_socket.sendall("Hello from server!".encode())

    # đóng kết nối
    client_socket.close()

'''
tóm tắt luồng hoạt động
- tạo socket server
- gán địa chỉ ip và cổng (bind())
- bật chết độ lắng nghe kết nối từ client (listen())
- khi có client kết nối, server chấp nhận kết nối (accept())
- nhận dữ liệu từ client (recv())
- gửi phản hồi lại client (sendall())
- đóng kết nối (close()), nhưng server vẫn tiếp tục chạy
'''
