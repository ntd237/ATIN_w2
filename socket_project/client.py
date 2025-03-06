import socket
import threading
import time
from config import SERVER_HOST, SERVER_PORT, HEARTBEAT_INTERVAL

class Client:
    def __init__(self, client_id, log_callback=None, message_callback=None):
        self.client_id = client_id
        self.client_socket = None
        self.running = True
        self.log_callback = log_callback
        self.message_callback = message_callback

    def log(self, message):
        print(message)
        if self.log_callback:
            self.log_callback(message)

    def connect(self):
        while self.running:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((SERVER_HOST, SERVER_PORT))
                self.log(f"✅ Kết nối với server ({self.client_id})")

                threading.Thread(target=self.send_heartbeat, daemon=True).start()
                threading.Thread(target=self.receive_messages, daemon=True).start()
                break
            except:
                self.log("🔄 Đang thử kết nối lại...")
                time.sleep(3)

    def send_heartbeat(self):
        while self.running:
            try:
                time.sleep(HEARTBEAT_INTERVAL)
                self.client_socket.sendall(f"HEARTBEAT:{self.client_id}".encode())
            except:
                self.log("⚠️ Mất kết nối, thử kết nối lại...")
                self.connect()

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    self.log(message)
                    if self.message_callback:
                        self.message_callback(message)
            except:
                self.log(f"❌ Mất kết nối với server. Thử kết nối lại...")
                self.connect()
                break

    def send_message(self, target_id, message):
        try:
            formatted_message = f"{target_id}:{message}"
            self.client_socket.sendall(formatted_message.encode())
            self.log(f"📤 Gửi đến {target_id}: {message}")
        except:
            self.log(f"❌ Lỗi gửi tin nhắn, kiểm tra kết nối!")

    def close(self):
        self.running = False
        self.client_socket.close()