import logging
from fastapi import APIRouter, HTTPException

from server.database.mongodb import client as mongodb

router = APIRouter()

logger = logging.getLogger(__name__)


class TestModel:
    name: str


@router.post("/user")
async def create_user(model: TestModel):
    """
    Create a new API key for a given project ID.

    Args:
        projectID (str): The ID of the project.

    Returns:
        dict: The dictionary representation of the new API key.

    Raises:
        HTTPException: If the maximum number of API keys for the project has been reached.
    """
    try:
        # Return the dictionary representation of the new API key
        return f"hi {model.name}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
