import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.database.mongodb import client as mongodb
from server.routers import user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


app.add_event_handler("startup", mongodb.connect)
app.add_event_handler("shutdown", mongodb.disconnect)


# Add middleware for CORS handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow any method
    allow_headers=["*"],
)


app.include_router(user.router)


if __name__ == "__main__":
    uvicorn.run(
        "server.main:app",
        host="0.0.0.0",
        port=4000,
        reload=True,
        limit_max_requests=None,
        workers=1,
        timeout_keep_alive=600,
    )
