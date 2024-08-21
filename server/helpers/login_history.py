from bson import ObjectId
from server.models.login_history import LoginHistory
from server.database.mongodb import client as mongodb


async def insert_login_history(userId: str):
    try:
        login_history = LoginHistory(userId=userId)
        login_history = login_history.dict(by_alias=True)
        await mongodb.db.login_history.insert_one(login_history)
    except Exception as e:
        raise e
