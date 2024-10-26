import os
from dotenv import load_dotenv
from enum import Enum

if os.path.exists("config.env"):
    TESTING = True
    load_dotenv("config.env")
else:
    TESTING = False
    load_dotenv()


class Config(object):
    # Mandatory configurations
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Optional configurations
    DATABASE_NAME = os.getenv("DATABASE_NAME", "upi_transactions")
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", False)


class TransactionType(Enum):
    CREDITED = "credited"
    DEBITED = "debited"
    SENT = "sent"
    RECEIVED = "received"