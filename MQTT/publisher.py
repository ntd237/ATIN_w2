import paho.mqtt.client as mqtt
import random
import time

broker = "localhost"
topic  = "iot/temperature"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker, 1883, 60) # kết nối broker trên cổng 1883 với timeout là 60s

while True:
    temperature = random.uniform(20, 40) # giả lập nhiệt độ từ 20 - 40 độ C
    print(f"Gửi nhiệt độ: {temperature} độ C")
    client.publish(topic, temperature) # gửi nhiệt độ lên topic
    time.sleep(2) # gửi dữ liệu mỗi 2s