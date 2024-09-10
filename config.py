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
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", 5000))
    DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "upi_transactions")


class TransactionType(Enum):
    CREDITED = "credited"
    DEBITED = "debited"