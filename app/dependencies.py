from jose import jwt, JWTError
from fastapi import Request, HTTPException

from app.auth import SECRET_KEY, ALGORITHM
from mlops.db import get_user_by_id


def get_user_from_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")
        if not user_id:
            return None

        return get_user_by_id(user_id)

    except JWTError:
        return None


def get_current_user(
    request: Request
):

    authorization = request.headers.get("authorization")
    token = None

    if authorization:
        token = authorization.replace("Bearer ", "")
    elif "token" in request.query_params:
        token = request.query_params["token"]

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    user = get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return user


async def resolve_user_from_request(
    request: Request
):

    authorization = request.headers.get("authorization")
    token = None

    if authorization:
        token = authorization.replace("Bearer ", "")
    elif "token" in request.query_params:
        token = request.query_params["token"]

    if not token:
        return None

    return get_user_from_token(token)
