from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QComboBox
)
import sys
import threading
from server import Server
from client import Client

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.clients = {}  
        self.client_count = 0
        self.initUI()
        self.start_server()

    def initUI(self):
        self.setWindowTitle("Chat giữa các Client qua Server")
        self.setGeometry(100, 100, 900, 600)

        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        self.server_log = QTextEdit()
        self.server_log.setReadOnly(True)
        self.server_log.setPlaceholderText("📌 Server Logs")
        grid_layout.addWidget(self.server_log, 0, 0)

        self.client_log = QTextEdit()
        self.client_log.setReadOnly(True)
        self.client_log.setPlaceholderText("💬 Client Logs")
        grid_layout.addWidget(self.client_log, 0, 1)

        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.chat_log.setPlaceholderText("🗨️ Chat giữa Client")
        grid_layout.addWidget(self.chat_log, 0, 2)

        main_layout.addLayout(grid_layout)

        # Dòng nhập tin nhắn thứ 1
        form_layout1 = QHBoxLayout()
        self.client_select1 = QComboBox()
        self.client_select1.addItem("Chọn Client gửi...")
        form_layout1.addWidget(self.client_select1)

        self.message_input1 = QLineEdit()
        form_layout1.addWidget(self.message_input1)

        self.send_button1 = QPushButton("📤 Gửi")
        self.send_button1.clicked.connect(lambda: self.send_message(self.client_select1, self.message_input1))
        form_layout1.addWidget(self.send_button1)

        main_layout.addLayout(form_layout1)

        # Dòng nhập tin nhắn thứ 2
        form_layout2 = QHBoxLayout()
        self.client_select2 = QComboBox()
        self.client_select2.addItem("Chọn Client gửi...")
        form_layout2.addWidget(self.client_select2)

        self.message_input2 = QLineEdit()
        form_layout2.addWidget(self.message_input2)

        self.send_button2 = QPushButton("📤 Gửi")
        self.send_button2.clicked.connect(lambda: self.send_message(self.client_select2, self.message_input2))
        form_layout2.addWidget(self.send_button2)

        main_layout.addLayout(form_layout2)

        self.new_client_btn = QPushButton("➕ Tạo Client mới")
        self.new_client_btn.clicked.connect(self.create_client)
        main_layout.addWidget(self.new_client_btn)

        self.setLayout(main_layout)

    def start_server(self):
        self.server = Server(log_callback=self.server_log.append)
        threading.Thread(target=self.server.start, daemon=True).start()

    def create_client(self):
        self.client_count += 1
        client_id = f"client{self.client_count}"
        client = Client(client_id, self.client_log.append, self.chat_log.append)
        threading.Thread(target=client.connect, daemon=True).start()
        self.clients[client_id] = client
        self.client_select1.addItem(client_id)
        self.client_select2.addItem(client_id)

    def send_message(self, client_select, message_input):
        sender_id = client_select.currentText()
        message = message_input.text()
        if sender_id and message:
            # Lấy danh sách client hiện có, trừ sender
            receiver_ids = [client_id for client_id in self.clients.keys() if client_id != sender_id]

            if not receiver_ids:
                self.chat_log.append("⚠️ Không có client nào để gửi!")
                return
            
            # Chọn client nhận tin nhắn từ combobox còn lại
            receiver_id = self.client_select2.currentText() if client_select == self.client_select1 else self.client_select1.currentText()

            # Kiểm tra client nhận có hợp lệ không
            if receiver_id and receiver_id in self.clients:
                self.clients[sender_id].send_message(receiver_id, message)
                # self.chat_log.append(f"{sender_id} → {receiver_id}: {message}")
            else:
                self.chat_log.append(f"⚠️ Không thể gửi tin nhắn đến {receiver_id}!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())