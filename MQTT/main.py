import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QGroupBox
from PyQt5.QtCore import pyqtSignal
from publisher import MQTTPublisherThread
from subscriber import MQTTSubscriberThread

class MQTTGuiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.publisher_thread = None
        self.subscriber_thread = None

    def initUI(self):
        self.setWindowTitle("MQTT Temperature Monitor")
        self.setGeometry(100, 100, 800, 400)

        # ================= Tab Gửi Dữ liệu =================
        self.send_group = QGroupBox("📤 Gửi Dữ liệu")
        self.send_layout = QVBoxLayout()
        self.send_status = QTextEdit()
        self.send_status.setReadOnly(True)
        self.send_button = QPushButton("Bắt đầu gửi dữ liệu")
        self.send_button.clicked.connect(self.toggle_publisher)
        self.send_layout.addWidget(self.send_status)
        self.send_layout.addWidget(self.send_button)
        self.send_group.setLayout(self.send_layout)

        # ================= Tab Nhận Dữ liệu =================
        self.receive_group = QGroupBox("📥 Nhận Dữ liệu")
        self.receive_layout = QVBoxLayout()
        self.receive_status = QTextEdit()
        self.receive_status.setReadOnly(True)
        self.receive_button = QPushButton("Bắt đầu nhận dữ liệu")
        self.receive_button.clicked.connect(self.toggle_subscriber)
        self.receive_layout.addWidget(self.receive_status)
        self.receive_layout.addWidget(self.receive_button)
        self.receive_group.setLayout(self.receive_layout)

        # ================= Layout chính =================
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.send_group)
        main_layout.addWidget(self.receive_group)
        self.setLayout(main_layout)

    def toggle_publisher(self):
        if self.publisher_thread and self.publisher_thread.isRunning():
            self.publisher_thread.stop()
            self.publisher_thread = None
            self.send_button.setText("Bắt đầu gửi dữ liệu")
            self.send_status.append("⏹ <b>Dừng gửi dữ liệu</b>")
        else:
            self.publisher_thread = MQTTPublisherThread()
            self.publisher_thread.update_signal.connect(self.send_status.append)
            self.publisher_thread.start()
            self.send_button.setText("Dừng gửi dữ liệu")

    def toggle_subscriber(self):
        if self.subscriber_thread and self.subscriber_thread.isRunning():
            self.subscriber_thread.terminate()
            self.subscriber_thread = None
            self.receive_button.setText("Bắt đầu nhận dữ liệu")
            self.receive_status.append("⏹ <b>Dừng nhận dữ liệu</b>")
        else:
            self.subscriber_thread = MQTTSubscriberThread()
            self.subscriber_thread.update_signal.connect(self.update_receive_status)
            self.subscriber_thread.start()
            self.receive_button.setText("Dừng nhận dữ liệu")

    def update_receive_status(self, message):
        """ Cập nhật status với màu phù hợp """
        if "quá cao" in message:
            color = "red"
        elif "quá thấp" in message:
            color = "blue"
        elif "ổn định" in message:
            color = "green"
        else:
            color = "black"  # Các thông báo khác giữ màu đen

        formatted_message = f'<span style="color: {color};">{message}</span>'
        self.receive_status.append(formatted_message)

# ============================ Run App ============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MQTTGuiApp()
    gui.show()
    sys.exit(app.exec_())
