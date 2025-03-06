from fastapi import FastAPI

app = FastAPI()

# Du lieu gia lap
users = [
    {"id": 1, "name": "Nguyễn Tiến Dũng", "email": "dung@example.com"},
    {"id": 2, "name": "Trần Văn An", "email": "an@example.com"},
]

# lay danh sach nguoi dung (GET)    
@app.get("/users")
def get_users():
    return {"users": users}

# lay thong tin nguoi dung theo (GET)
@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return {"user": user}
    return {"error": "User not found!"}

# them nguoi dung (POST)
@app.post("/users")
def add_user(user: dict):
    user["id"] = len(users) + 1
    users.append(user)
    return {"message": "User added", "user": user}

# cap nhat nguoi dung (PUT)
@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: dict):
    for user in users:
        if user["id"] == user_id:
            user.update(user_data)
            return {"message": "User updated", "user": user}
    return {"error": "User not found!"}


# xoa nguoi dung (DELETE)
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users
    users = [user for user in users if user["id"] != user_id]
    return {"message": "User deleted"}

# cd d:/Workspace/Project/ATIN/2025/3/3/RESTful API
# C:\Users\Lenovo\AppData\Roaming\Python\Python313\Scripts\uvicorn RESTful_API:app --reload