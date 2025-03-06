import socket
import threading
import time
from config import SERVER_HOST, SERVER_PORT, TIMEOUT

class Server:
    def __init__(self, log_callback=None):
        self.clients = {}  # {client_id: (socket, last_heartbeat)}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((SERVER_HOST, SERVER_PORT))
        self.server.listen(5)
        self.log_callback = log_callback
        self.log("🚀 Server started...")

    def log(self, message):
        print(message)
        if self.log_callback:
            self.log_callback(message)

    def handle_client(self, client_socket, client_id):
        self.log(f"🔗 Client {client_id} connected")
        self.clients[client_id] = (client_socket, time.time())

        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                self.clients[client_id] = (client_socket, time.time())  # Cập nhật heartbeat

                if data.startswith("HEARTBEAT"):
                    self.log(f"💓 Heartbeat từ {client_id}")
                elif ":" in data:
                    target_id, message = data.split(":", 1)
                    target_id = target_id.strip()
                    message = message.strip()

                    if target_id in self.clients:
                        target_socket, _ = self.clients[target_id]
                        target_socket.send(f"{client_id} → {target_id}: {message}".encode())
                        self.log(f"📩 {client_id} → {target_id}: {message}")
                    else:
                        self.log(f"⚠️ Client {target_id} không tồn tại!")
                else:
                    self.log(f"❓ Dữ liệu không hợp lệ: {data}")
        except Exception as e:
            self.log(f"❌ Lỗi client {client_id}: {e}")
        finally:
            self.log(f"❌ Client {client_id} bị ngắt kết nối")
            del self.clients[client_id]
            client_socket.close()

    def remove_inactive_clients(self):
        while True:
            time.sleep(5)
            current_time = time.time()
            for client_id in list(self.clients.keys()):
                _, last_heartbeat = self.clients[client_id]
                if current_time - last_heartbeat > TIMEOUT:
                    self.log(f"⏳ Removing inactive client {client_id}")
                    del self.clients[client_id]

    def start(self):
        threading.Thread(target=self.remove_inactive_clients, daemon=True).start()

        while True:
            client_socket, _ = self.server.accept()
            client_id = f"client{len(self.clients) + 1}"
            threading.Thread(target=self.handle_client, args=(client_socket, client_id), daemon=True).start()