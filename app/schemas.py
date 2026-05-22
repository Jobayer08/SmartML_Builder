from pydantic import BaseModel


# ======================================================
# REGISTER
# ======================================================

class RegisterRequest(BaseModel):

    username: str
    email: str
    password: str


# ======================================================
# LOGIN
# ======================================================

class LoginRequest(BaseModel):

    email: str
    password: str