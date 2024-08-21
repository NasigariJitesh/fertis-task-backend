import datetime
from typing import Dict
import bcrypt
from fastapi import HTTPException, Request
import jwt

from server.models.user import UserInToken
from config import jwt_secret


def get_hashed_password(plain_text_password: str):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt()).decode()


def check_password(plain_text_password: str, hashed_password: str):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())


def get_jwt_token(payload: Dict):
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    refresh_payload = {
        **payload,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=3),
    }

    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, jwt_secret, algorithm="HS256")

    return {
        "token": token,
        "refresh_token": refresh_token,
    }


def refresh_jwt_token(token: str):
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])

        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        refresh_payload = {
            **payload,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=3),
        }

        token = jwt.encode(payload, jwt_secret, algorithm="HS256")
        refresh_token = jwt.encode(refresh_payload, jwt_secret, algorithm="HS256")

        return {
            "token": token,
            "refresh_token": refresh_token,
        }

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(detail="Token expired", status_code=401)

    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(detail="Invalid token", status_code=401)

    except Exception as e:
        raise HTTPException(detail=str(e), status_code=401)


async def authorize(request: Request) -> UserInToken:
    try:
        auth_header = request.headers.get("Authorization", "")

        # If no Authorization header is present, deny access
        if not auth_header:
            raise HTTPException(
                detail="Please provide an authorization token", status_code=401
            )

        token = auth_header.split(" ")[1]

        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return UserInToken(**payload)

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(detail="Token expired", status_code=401)

    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(detail="Invalid token", status_code=401)

    except Exception as e:
        raise HTTPException(detail=str(e), status_code=401)
