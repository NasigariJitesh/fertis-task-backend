from typing import Optional
from pydantic import BaseModel, Field

from server.models._common import ObjectId, PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(
        default_factory=PyObjectId, description="User ID", alias="_id"
    )
    name: str = Field(description="Name of the user")
    bio: str = Field(default="", description="Name of the user")
    email: str = Field(description="Email of the user")
    image: str = Field(default="", description="Image of the user")


class UserWithPassword(User):
    password: str = Field(description="Password of the user")


class UserInToken(BaseModel):
    id: PyObjectId = Field(
        default_factory=PyObjectId, description="User ID", alias="_id"
    )
    name: str = Field(description="Name of the user")

    email: str = Field(description="Email of the user")


class UpdateUserInput(BaseModel):
    name: Optional[str] = Field(description="Name of the user")
    bio: Optional[str] = Field(description="Name of the user")
    image: Optional[str] = Field(description="Image of the user")


class SignupInput(BaseModel):
    name: str = Field(description="Name of the user")
    email: str = Field(description="Email of the user")
    password: str = Field(description="Password of the user")


class SigninInput(BaseModel):
    email: str = Field(description="Email of the user")
    password: str = Field(description="Password of the user")


class SigninResponse(BaseModel):
    token: str = Field(description="JWT token for the user")
    refresh_token: str = Field(description="Refresh token for the user")


class RefreshTokenInput(BaseModel):
    token: str = Field(description="Refresh token of the user")
