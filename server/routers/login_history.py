import logging
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from server.database.mongodb import client as mongodb
from server.helpers.user import (
    authorize,
)
from server.models.login_history import LoginHistoryWithUser
from server.models.user import User

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/user/{userId}/loginHistory")
async def get_user_login_history(userId: str, authorized_user=Depends(authorize)):
    try:
        if not authorized_user or str(authorized_user.id) != userId:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = await mongodb.db.users.find_one({"_id": ObjectId(userId)})

        if not user:
            raise HTTPException(status_code=404, detail="Unauthorized")

        user = User(**user).dict(by_alias=True)
        user["_id"] = str(user["_id"])

        query = {"userId": userId}

        login_history = (
            await mongodb.db.login_history.find(query)
            .sort("_id", -1)
            .limit(100)
            .to_list(100)
        )

        for item in login_history:
            item["_id"] = str(item["_id"])
            item["user"] = user
            item = LoginHistoryWithUser(**item).dict(by_alias=True)
            item["_id"] = str(item["_id"])

        return login_history

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
