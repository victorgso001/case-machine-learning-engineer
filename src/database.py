"""
    Database functions
"""
from dotenv import load_dotenv
from pymongo import MongoClient
# from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()


def db_client():
    """
        Initialize db client
    """
    client = MongoClient("mongodb://mongo_db:27017/")
    return client['mle_case_db']
