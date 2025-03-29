from fastapi import FastAPI, Response, Cookie, HTTPException
from pydantic import BaseModel

app = FastAPI()

users_bd = {
    "username": "user123",
    "password": "password123"
}

class UserLogin(BaseModel):
    username: str
    password: str

session_token_value = "abc123xyz456"


@app.post("/login")
async def login(data: UserLogin):
    if data.username == users_bd["username"] and data.password == users_bd["password"]:
        response = Response(content='{"message": "Успешный вход в систему"}', media_type="application/json")
        response.set_cookie(
            key="session_token",
            value=session_token_value,
            httponly=True,
            secure=True,
            samesite="lax"
        )
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/user")
async def get_user(session_token: str = Cookie(None)):
    if session_token is None or session_token != session_token_value:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"username": "user123", "email": "user123@example.com"}
