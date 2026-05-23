from jose import jwt, JWTError
from fastapi import Header, HTTPException

from app.auth import SECRET_KEY, ALGORITHM


def get_current_user(
    authorization: str = Header(None)
):

    if authorization is None:

        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    try:

        token = authorization.replace(
            "Bearer ",
            ""
        )

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )