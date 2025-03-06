import time
import random
import paho.mqtt.client as mqtt
from PyQt5.QtCore import QThread, pyqtSignal

class MQTTPublisherThread(QThread):
    update_signal = pyqtSignal(str)  # tín hiệu gửi dữ liệu đến giao diện

    def __init__(self, broker="localhost", port=1883, topic="iot/temperature"):
        super().__init__()
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.running = False # biến kiểm soát trạng thái của tiến trình

    def run(self):
        while not self.running:
            try:
                self.client.connect(self.broker, self.port, 60)
                self.client.loop_start()
                self.update_signal.emit("✅ Đã kết nối MQTT Broker!")
                self.running = True
            except Exception as e:
                self.update_signal.emit(f"❌ Lỗi kết nối MQTT: {e}")
                time.sleep(5)  # Chờ 5 giây trước khi thử lại

        while self.running:
            temperature = random.uniform(15, 40)
            try:
                self.client.publish(self.topic, temperature, retain=True)
                self.update_signal.emit(f"📤 Gửi nhiệt độ: {temperature:.2f}°C")
            except Exception as e:
                self.update_signal.emit(f"❌ Lỗi gửi dữ liệu: {e}")
            time.sleep(2)  # Gửi dữ liệu mỗi 2s

    def stop(self):
        self.running = False
        self.client.loop_stop() 
        self.client.disconnect()
        self.quit()
        self.wait() 


"""
tóm tắt luồng hoạt động:
- khởi động thread (run())
    thử kết nối đến MQTT Broker 
    nếu thành công hiển thị thông báo kết nối thành công
    nếu thất bại hiển thị thông báo kết nối thất bại và thử lại sau 5s
- gửi dữ liệu nhiết độ
    gửi 1 giá trị nhiệt độ ngẫu nhiên từ 15 đến 40 độ C sau mỗi 2s
    nếu gửi thành công hiển thị thông báo gửi thành công
    nếu gửi thất bại hiển thị thông báo gửi thất bại
- dừng thread (stop())
    dừng vòng lặp gửi dữ liệu
    dừng vòng lặp MQTT và ngắt kết nối
    kết thúc tiến trình thread
"""