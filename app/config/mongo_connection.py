import motor.motor_asyncio
from .AppConfig import config

def get_motor_client():
    connection_uri = config.database_url
    return motor.motor_asyncio.AsyncIOMotorClient(connection_uri)

def get_db_instance():
    connection_uri = config.database_url
    client = motor.motor_asyncio.AsyncIOMotorClient(connection_uri)
    return client.get_database('mercorChatDb')
