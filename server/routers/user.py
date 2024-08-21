import logging
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pymongo import ReturnDocument
from server.database.mongodb import client as mongodb
from server.helpers.login_history import insert_login_history
from server.helpers.user import (
    authorize,
    check_password,
    get_jwt_token,
    get_hashed_password,
    refresh_jwt_token,
)
from server.models.user import (
    RefreshTokenInput,
    SigninInput,
    SigninResponse,
    SignupInput,
    UpdateUserInput,
    User,
    UserWithPassword,
)

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/signup", response_model=str)
async def signup(input: SignupInput):
    try:
        password = input.password
        # hash the password using the encryption to store in db
        input.password = get_hashed_password(password)
        user = UserWithPassword(**input.dict()).dict(by_alias=True)

        response = await mongodb.db.users.insert_one(user)
        if response.inserted_id:
            return "User created successfully"
        else:
            raise HTTPException(status_code=500, detail="User creation failed")
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signin", response_model=SigninResponse)
async def signin(input: SigninInput):
    try:
        user = await mongodb.db.users.find_one({"email": input.email})

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user = UserWithPassword(**user)

        # hash the password using the encryption to store in db
        password_match = check_password(
            plain_text_password=input.password, hashed_password=user.password
        )

        if not password_match:
            raise HTTPException(
                status_code=404, detail="Incorrect email and password match"
            )

        await insert_login_history(str(user.id))

        user_for_token = {
            "_id": str(user.id),
            "name": user.name,
            "email": user.email,
        }

        # create jwt token
        response = get_jwt_token(user_for_token)

        response = SigninResponse(**response)

        return response

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refresh-token", response_model=SigninResponse)
async def refresh_token(input: RefreshTokenInput, authorized_user=Depends(authorize)):
    try:
        if not authorized_user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # create jwt token
        response = refresh_jwt_token(input.token)

        response = SigninResponse(**response)

        return response

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{userId}")
async def get_user(userId: str, authorized_user=Depends(authorize)):
    try:
        if not authorized_user or str(authorized_user.id) != userId:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = await mongodb.db.users.find_one({"_id": ObjectId(userId)})

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user = User(**user).dict(by_alias=True)
        user["_id"] = str(user["_id"])

        return user

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/user/{userId}")
async def update_user(
    userId: str, input: UpdateUserInput, authorized_user=Depends(authorize)
):
    try:
        if not authorized_user or str(authorized_user.id) != userId:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = await mongodb.db.users.find_one({"_id": ObjectId(userId)})

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        input = input.dict(exclude_unset=True)

        response = await mongodb.db.users.find_one_and_update(
            {"_id": ObjectId(userId)},
            {"$set": input},
            return_document=ReturnDocument.AFTER,
        )

        if not response:
            raise HTTPException(status_code=404, detail="User not found")

        user = User(**response).dict(by_alias=True)
        user["_id"] = str(user["_id"])
        return user

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
