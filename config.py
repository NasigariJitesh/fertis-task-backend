import os
from pathlib import Path

from dotenv import load_dotenv

ENVIRONMENT = os.getenv("ENVIRONMENT", default="development")

env_path = Path(f".env.{ENVIRONMENT}")


load_dotenv(dotenv_path=env_path)


mongodb_url = os.getenv("MONGODB_URL", "")
mongodb_name = os.getenv("MONGODB_NAME", "")
