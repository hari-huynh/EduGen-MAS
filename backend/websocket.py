from fastapi import FastAPI, Response, Request,WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, uvicorn
from asyncio import sleep
from pydantic import BaseModel, Field, ConfigDict
import time
from fastapi import WebSocket
from fastapi.responses import HTMLResponse
import os
from pydantic_ai import Agent, RunContext
import nest_asyncio
import asyncio
import uuid
import requests

nest_asyncio.apply()

import json
from datetime import datetime
from mas.workflow import graph
from api import LearningMaterial

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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = Agent('google-gla:gemini-2.0-flash')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept() 

    try:
        while True:
            data = await websocket.receive_text()
            user_query = json.loads(data)
            
            session_id = user_query["session_id"]

            mongodb["chatbotdb"].update_one(
                { "session_id": session_id },
                {
                    "$push": { 
                        "messages": {
                            "content": user_query['content'],
                            "role": user_query['role'],                                
                            "timestamp": user_query['timestamp']
                        },
                    }
                },
                
                upsert=True
            )
                
            init_state = {
                "session_id": session_id,
                "project_id": user_query["project_id"],
                "user_id": user_query["user_id"],
                "title": "",
                "user_query": user_query["content"],
                "websocket": websocket, 
                "results": {},
                "todo_list": {},
                "lecture_notes": {},
                "presentation_template_url": "",
                "presentation_folder_url": "",
                "presentation_urls": [],                
                "links_lecture": [],
                "links_quiz" : [],
            }

            current_state = {}
            async for chunk in graph.astream(init_state, stream_mode="values", config={"recursion_limit": 1000}):
                current_state = dict(chunk) 
                
                await websocket.send_json({
                    "messageId": str(uuid.uuid4()),
                    "role": "agent",
                    "content": f"{str(current_state)}",                
                    "timestamp": str(datetime.now())
                })   
                
                

                if current_state.get("results").get("quiz"):
                    quiz_data = [{
                        "question": quiz['question'],
                        "option": quiz['option'],
                        "answer": quiz['answer'],
                        # "explain": quiz['explain'],
                        "source": quiz['source']
                    } for quiz in current_state.get("results").get("quiz")['questions']]
                else:
                    quiz_data = []
                # current_state['title'] = current_state.get("results").get("curriculum")['title']
                send_data = {
                    "todoList": list(current_state.get("todo_list").values()),
                    "curriculum": current_state.get("results").get("curriculum"),
                    "lectureNotes": [{"content": note} for note in list(current_state.get("lecture_notes").values())],
                    "quizzes": quiz_data,
                    "presentationURL": current_state.get("presentation_urls"),
                    "links_lecture": current_state.get("links_lecture"),
                    "links_quiz": current_state.get("links_quiz")
                }

                if current_state.get("results").get("curriculum"):
                    curriculum = current_state.get("results").get("curriculum")
                    # print(curriculum)
                    current_state["title"] = curriculum["title"]

                if current_state.get("links_quiz"):
                    send_data["event"] = "quiz_created"
                
                ##==============
              
                # "messages": {
                #             "content": user_query['content'],
                #             "role": user_query['role'],                                
                #             "timestamp": user_query['timestamp']
                #         },
                
                mongodb["chatbotdb"].update_one(
                { "session_id": session_id },
                {
                    "$push": { 
                        "state": {
                            "project_id": current_state["project_id"],
                            "user_id": current_state["user_id"],
                            "results": current_state.get("results"),
                            "todo_list": current_state.get("todo_list"),
                            "lecture_notes": [{"content": note} for note in list(current_state.get("lecture_notes").values())],
                            "presentation_template_url": current_state.get("presentation_template_url"),
                            "presentation_folder_url": current_state.get("presentation_folder_url"),
                            "presentation_urls": current_state.get("presentation_urls"),
                            "links_lecture": current_state.get("links_lecture"),
                            "links_quiz" : current_state.get("links_quiz")
                        }
                    }
                },
                
                upsert=True
            )
                
                await websocket.send_json(send_data)

            await websocket.send_json({
                "messageId": "",
                "role": "agent",
                "content": "",
                "timestamp": str(datetime.now()),
                "type": "export"
            })

            data = await websocket.receive_text()
            is_export = json.loads(data)

            if is_export["export"]:
                materials = LearningMaterial(
                    curriculum = current_state.get("results").get("curriculum"),
                    lecture_urls = current_state.get("links_lecture"),
                    presentation_urls = [],
                    quiz_urls = current_state.get("links_quiz")
                )

                url = "http://localhost:8000/export/classroom"
                payload = materials.model_dump()

                response = requests.post(url, json=payload)

                # Handle response
                if response.ok:
                    print(response.json())
                else:
                    print("Error:", response.status_code)


    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print("Error:", e)
        await websocket.close()



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)