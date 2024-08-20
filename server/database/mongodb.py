import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

import config


class MongoDB:
    def __init__(
        self, mongo_url: Optional[str] = None, mongodb_name: Optional[str] = None
    ):
        self.url = mongo_url or config.mongodb_url
        self.name = mongodb_name or config.mongodb_name

        self.client: AsyncIOMotorClient = AsyncIOMotorClient(self.url)
        self.db = self.client.get_database(self.name)
        print("Connected to MongoDB client")

    def connect(self):
        if self.client is not None:
            return
        self.client = AsyncIOMotorClient(self.url)
        self.db = self.client.get_database(self.name)
        logging.info("MongoDB connection established")

    def disconnect(self):
        if self.client is None:
            logging.warning("Connection is None, nothing to close")
            return
        self.client.close()
        self.client = None  # type: ignore
        logging.info("MongoDB connection closed")

    def __del__(self):
        self.disconnect()


client = MongoDB()
