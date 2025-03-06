import uuid

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345
HEARTBEAT_INTERVAL = 5  # Client gửi heartbeat mỗi 5s
TIMEOUT = 10  # Server sẽ xóa client nếu không nhận heartbeat sau 10s
BUFFER_SIZE = 1024  # Kích thước buffer nhận/gửi dữ liệu

# Sinh UUID cho client
def generate_uuid():
    return str(uuid.uuid4())
