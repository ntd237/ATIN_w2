# AI phân tích dữ liệu IoT

import paho.mqtt.client as mqtt # thư viện Paho MQTT để nhận dữ liệu từ BrokerBroker
import numpy as np
from sklearn.linear_model import LinearRegression # mô hình hồi quy tuyến tính dự đoán nhiệt độđộ

# dữ liệu lịch sử nhiệt độ
temperature_data = []

def analyze_temperature():
    if len(temperature_data) < 5:
        return "Đang thu thập dữ liệu ..."
    
    # range(len(temperature_data)) tạo mảng [0, 1, 2, ..., len(temperature_data) - 1] tướng ứng với số lần ghi nhận nhiệt độ
    # reshape(-1, 1) chuyển mảng 1 chiều thành mảng 2 chiều với 1 cột
    X = np.array(range(len(temperature_data))).reshape(-1, 1)
    y = np.array(temperature_data) # biến y chứa nhiệt độ thực tế

    model = LinearRegression() # tạo mô hình hồi quy tuyến tính
    model.fit(X, y) # huấn luyện mô hình với dữ liệu thu thập được

    future_temp = model.predict([[len(temperature_data) + 1]])[0]

    if future_temp > 35:
        return f"Cảnh báo: Nhiệt độ dự đoán quá cao ({future_temp:.2f} độ C)"
    elif future_temp < 22:
        return f"Cảnh báo: Nhiệt độ dự đoán quá thấp ({future_temp:.2f} độ C)"
    else:
        return f"Dự đoán: Nhiệt độ ổn định {future_temp:.2f} độ C"
    
def on_message(client, userdata, message):
    # message.payload.decode() giải mã tin nhắn nhận được tự mqtt thành chuỗi
    # float() chuyển đổi chuỗi thành số thựcthực
    temperature = float(message.payload.decode())
    print(f"Nhận nhiệt độ: {temperature} độ C")

    temperature_data.append(temperature)
    if len(temperature_data) > 10:
        temperature_data.pop(0)

    analysis = analyze_temperature()
    print(analysis)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1883, 60)
client.subscribe("iot/temperature")
client.on_message = on_message
client.loop_forever()

'''
tóm tắt luồng hoạt động
- Kết nối tới broker MQTT trên localhost cổng 1883
- Đăng ký nhận dữ liệu từ topic iot/temperature
- Mỗi khi nhận được dữ liệu, AI lưu vào danh sách temperature_data
- Huấn luyện mô hình Linear Regression để dự đoán nhiệt độ tiếp theo
- Nếu nhiệt độ dự đoán vượt giới hạn thì hệ thống sẽ cảnh báo
- Chạy liên tục để cập nhật dữ liệu theo thời gian thực
'''