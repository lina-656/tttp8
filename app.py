from fastapi import FastAPI, Form, Response, Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
import secrets

app = FastAPI()

# Для работы с CORS, если потребуется
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Предположим, у нас есть простая база пользователей
fake_db = {
    "user123": "password123"
}

# Словарь для хранения токенов
active_sessions = {}

# Маршрут входа в систему
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), response: Response = None):
    if username in fake_db and fake_db[username] == password:
        # Генерируем уникальный токен для сессии пользователя
        session_token = secrets.token_hex(16)
        active_sessions[session_token] = username  # Сохраняем токен и имя пользователя
        response.set_cookie(key="session_token", value=session_token, httponly=True)
        return JSONResponse(content={"message": "Login successful"}, status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Защищенный маршрут
@app.get("/user")
async def get_user(session_token: str = Cookie(None)):
    if session_token is None or session_token not in active_sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    username = active_sessions[session_token]
    user_info = {
        "username": username,
        "message": "Welcome to the protected route!"
    }
    return user_info

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
