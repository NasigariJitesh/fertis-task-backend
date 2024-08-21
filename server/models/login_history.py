from time import time
from pydantic import BaseModel, Field

from server.models._common import PyObjectId, ObjectId
from server.models.user import User


def get_current_time_in_ms():
    return int(time() * 1000)


class LoginHistory(BaseModel):
    id: PyObjectId = Field(
        default_factory=PyObjectId, description="User ID", alias="_id"
    )
    timestamp: float = Field(
        default_factory=get_current_time_in_ms, description="Name of the user"
    )
    userId: str = Field(description="Id of the user")


class LoginHistoryWithUser(LoginHistory):
    user: User
