import uuid
from datetime import datetime

## Data Base
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

mongodb = client.get_database('chatbotdb')


async def run_agent(agent, state, deps):
    # Create new UUID for message_id
    message_id = str(uuid.uuid4())

    # Store final message to save database
    message_content = ""

    # Get websocket from state
    websocket = state["websocket"]

    async with agent.run_stream("", deps=deps) as response:
        async for data in response.stream_text(delta=True):
            message_content += data

            # Send response message back to chat
            await websocket.send_json({
                "messageId": message_id,
                "role": "agent",
                "content": data,
                "timestamp": str(datetime.now()),
                "type": "message"
            })

    mongodb["chatbotdb"].update_one(
        { "session_id": state['session_id'] },
        {
            "$push": { 
                "messages": {
                    "content": message_content,
                    "role": 'agent', 
                    "timestamp": str(datetime.now())                                
                },                                
            }
        },
        upsert=True
    )

    return message_content