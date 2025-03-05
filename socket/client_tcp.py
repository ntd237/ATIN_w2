import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345)) # kết nối tới server

# gửi dữ liệu đến server
client_socket.sendall("Hello server!".encode())

# nhận phản hồi từ server 
data = client_socket.recv(1024).decode()
print(f"server trả lời: {data}")

client_socket.close()