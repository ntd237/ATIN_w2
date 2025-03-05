import subprocess
import time

NUM_CLIENTS = 5  # Số client muốn chạy

processes = []

# Khởi chạy nhiều client
for i in range(NUM_CLIENTS):
    print(f"Starting client {i+1}...")
    p = subprocess.Popen(["python", "./client.py"], shell=True)
    processes.append(p)
    time.sleep(1)  # Chờ 1 giây giữa các lần khởi động

# Giữ chương trình chạy để xem output
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down clients...")
    for p in processes:
        p.terminate()

"""
luồng hoạt động
- Xác định số lượng client cần chạy (NUM_CLIENTS)
- Tạo danh sách processes để lưu tiến trình
- Dùng vòng lặp khởi động nhiều client (client.py) bằng subprocess.Popen()
- Giữ chương trình chạy để quan sát các client hoạt động
- Khi nhấn Ctrl + C, chương trình sẽ tự động tắt tất cả client bằng terminate()
"""
