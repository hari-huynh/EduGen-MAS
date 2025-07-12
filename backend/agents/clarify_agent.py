from datetime import datetime
from pydantic_ai import Agent, RunContext
from agents.pydantic_models import Objective
import dotenv
import json
import os
from utils.setup import setup_gemini

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

setup_gemini()

clarify_agent = Agent(
    'google-gla:gemini-2.0-flash', #'google-gla:learnlm-2.0-flash-experimental', #
    deps_type=Objective,
    result_type = str
)

@clarify_agent.system_prompt
def system_prompt(ctx: RunContext) -> str:
     return f"""
        You are in charge of understanding the user query and extracting information from: "{ctx.deps.user_query}".
        Given the current course objective details:
        - Subject: {ctx.deps.subject}
        - Level: {ctx.deps.level}
        - Target Audience: {ctx.deps.target_audience}
        - Entire Course: {ctx.deps.entire_course}
        - Chapters (if applicable): {ctx.deps.chapters}

        Your goal is to identify any missing or unclear information required to fully understand the user's intent.
        If you are unsure about any aspect of the objective based on the initial user query, use the 'get_user_query' tool to ask the user for a clear and concise clarification question.

        Focus on asking ONE specific question at a time to avoid overwhelming the user.
        Make sure the question directly addresses the ambiguity or missing detail.
        Avoid vague or open-ended questions. Be precise about what information you need.
        Do not assume information. Always ask for clarification if there's any doubt.
        Return user's objective clear and concise.
        """

@clarify_agent.tool
async def get_user_query(ctx: RunContext, question: str) -> str:
    websocket = ctx.deps.websocket

    await websocket.send_json(
        {
            "role": "agent",
            "content": question,
            "timestamp": str(datetime.now())
        }
    )

    mongodb["chatbotdb"].update_one(
                { "session_id": ctx.deps.session_id },
                {
                    "$push": { 
                        "messages": {
                            "content": question,
                            "role": "agent",                                
                            "timestamp": str(datetime.now())
                        },
                    }
                },
                
                upsert=True
            )

    data = await websocket.receive_text()
    answer = json.loads(data)

    mongodb["chatbotdb"].update_one(
                { "session_id": ctx.deps.session_id },
                {
                    "$push": { 
                        "messages": {
                            "content": answer["content"],
                            "role": "user",                                
                            "timestamp": str(datetime.now())
                        },
                    }
                },
                
                upsert=True
            )

    return f"User answer: {answer['content']}"

# if __name__ == "__main__":
#     deps = Objective(
#         user_query = "Can you help me create a learning material for Introduction to Artificial Intelligence course",
#         subject = "",
#         level = "",
#         target_audience = "",
#         entire_course = False,
#         chapters = []
#     )

#     result = clarify_agent.run_sync(
#         "", deps=deps, 
#         model_settings={'temperature': 0.0}
#     )

#     print(result)