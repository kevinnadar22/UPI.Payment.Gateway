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
    SERVER_URL = os.getenv("SERVER_URL")
    UPI_ID = os.getenv("UPI_ID")
    DOWNLOADS_DIR = os.getenv("DOWNLOADS_DIR", "downloads")