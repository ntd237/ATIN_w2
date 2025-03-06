import numpy as np
import time
import paho.mqtt.client as mqtt
from PyQt5.QtCore import QThread, pyqtSignal
from sklearn.linear_model import LinearRegression

class MQTTSubscriberThread(QThread):
    update_signal = pyqtSignal(str)  # Gửi dữ liệu đến giao diện

    def __init__(self, broker="localhost", port=1883, topic="iot/temperature"):
        super().__init__()
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) 
        self.client.on_message = self.on_message # Gán hàm xử lý khi nhận được tin nhắn
        self.client.on_disconnect = self.on_disconnect # Gán hàm xử lý khi mất kết nối
        self.temperature_data = [] # Dữ liệu nhiệt độ

    def run(self):
        while True:
            try:
                self.client.connect(self.broker, self.port, 60)
                self.update_signal.emit("✅ Đã kết nối MQTT Broker!")
                self.client.subscribe(self.topic)
                self.client.loop_forever()
            except Exception as e:
                self.update_signal.emit(f"❌ Lỗi kết nối MQTT: {e}")
                time.sleep(5)  # Thử lại sau 5 giây

    def on_disconnect(self):
        self.update_signal.emit("⚠️ Mất kết nối MQTT. Đang thử kết nối lại...")
        self.try_reconnect()

    def try_reconnect(self):
        while True:
            try:
                self.client.reconnect()
                self.update_signal.emit("✅ Đã kết nối lại MQTT Broker!")
                self.client.subscribe(self.topic)
                break
            except Exception as e:
                self.update_signal.emit(f"🔄 Đang thử kết nối lại... {e}")
                time.sleep(5)  # Thử lại sau 5 giây

    def on_message(self, client, userdata, message):
        try:
            temperature = float(message.payload.decode())
            self.temperature_data.append(temperature)
            if len(self.temperature_data) > 10:
                self.temperature_data.pop(0)
            analysis = self.analyze_temperature()
            self.update_signal.emit(f"📥 Nhận nhiệt độ: {temperature:.2f}°C")
            self.update_signal.emit(analysis)
        except Exception as e:
            self.update_signal.emit(f"❌ Lỗi xử lý dữ liệu: {e}")

    def analyze_temperature(self):
        if len(self.temperature_data) < 5:
            return "📊 Đang thu thập dữ liệu ..."

        X = np.array(range(len(self.temperature_data))).reshape(-1, 1)
        y = np.array(self.temperature_data)
        model = LinearRegression()
        model.fit(X, y)
        future_temp = model.predict([[len(self.temperature_data) + 1]])[0]

        if future_temp > 35:
            return f"🚨 Cảnh báo: Nhiệt độ dự đoán quá cao ({future_temp:.2f}°C)"
        elif future_temp < 20:
            return f"🚨 Cảnh báo: Nhiệt độ dự đoán quá thấp ({future_temp:.2f}°C)"
        else:
            return f"✅ Dự đoán: Nhiệt độ ổn định ({future_temp:.2f}°C)"

'''
tóm tắt luồng hoạt động
- kết nối với MQTT Broker (run())
    nếu thành công thì in ra thông báo kết nối thành công
    nếu thất bại thì in ra thông báo lỗi kết nối và thử lại sau 5 giây
- đăng ký nhận dữ liệu từ iot/temperature
- xử lý khi mất kết nối và tự động kết nối lại với MQTT Broker
- lắng nghe dữ liệu qua on_message()
    in ra thông báo nhận được dữ liệu nhiệt độ
    gọi hàm analyze_temperature() để phân tích dữ liệu
    nếu bị lỗi thì in ra lỗi xử lý dữ liệu
- phân tích dữ liệu analyze_temperature()
    nếu chưa đủ dữ liệu thì in ra thông báo đang thu thập dữ liệu
    dự đoán nhiệt độ tiếp theo
    nếu nhiệt độ dự đoán quá cao thì in ra cảnh báo quá cao
    nếu nhiệt độ dự đoán quá thấp thì in ra cảnh báo quá thấp
    nếu nhiệt độ dự đoán ổn định thì in ra dự đoán ổn định
'''