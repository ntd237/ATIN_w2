import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello UDP server!"
client_socket.sendto(message.encode(), ('127.0.0.1', 12345))

# nhận phản hồi từ server
data, server = client_socket.recvfrom(1024)
print(f"server trả lời: {data.decode()}")

client_socket.close()