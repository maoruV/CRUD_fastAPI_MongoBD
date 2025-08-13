import motor.motor_asyncio
from config.settings import settings



client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.mongo_db]