from urllib.parse import quote_plus
from pymongo.mongo_client import MongoClient
# from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo.server_api import ServerApi

db_password = quote_plus("Truong2003@")

uri = f"mongodb+srv://quangtruongairline:{db_password}@chatbotdb.pzsqjdr.mongodb.net/?retryWrites=true&w=majority&appName=chatbotdb"

# Create a new client and connect to the server
client = MongoClient(uri,tls=True, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.get_database('chatbotdb')
# mongo_memory = MongoDBSaver(db)

messages = [
    {
        "content": "Hello",
        "role": "user",
        "timestamp": "729384",
    },
    {
        "content": "Hello, how can I help you.",
        "role": "agent",
        "timestamp": "729384",
    },
    {
        "content": "Hello",
        "role": "user",
        "timestamp": "729384",
    },
    {
        "content": "Hello, how can I help you.",
        "role": "agent",
        "timestamp": "729384",
    },
]

mes = {
    'session_id': "12345",
    'messages': []
}

# db["chatbotdb"].insert_one(messages)
# mongo_memory.db["chatbotdb"].insert_one(chat_record)
for i in messages:    
    db["chatbotdb"].update_one(
        { "session_id": "12345" },
        {
            "$push": { 
                "messages": i,
            }
        },
        upsert=True
    )
