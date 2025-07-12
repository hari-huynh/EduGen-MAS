from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

from typing import List, Literal, Dict, Any
from typing_extensions import TypedDict
from agents.pydantic_models import Task, RunTask, Objective
from fastapi import WebSocket

class State(TypedDict):
    user_query: str
    objective: Objective
    history: str
    thinking: str
    todo_list: Dict[str, Any]
    data: str
    next_action: RunTask
    next_step: Literal["supervisor", "get_user_query", "collect_data_agent", "curriculum_agent", \
                       "lecture_note_gen_agent", "presentation_gen_agent", "quiz_gen_agent", "evaluator_agent", "end"]
    results: Dict[str, Any]
    lecture_notes: Dict[str, str]
    websocket: WebSocket
    presentation_template_url: str
    presentation_folder_url: str
    presentation_urls: List[Dict[str, str]]

    session_id: str
    project_id: str
    user_id: str
    links_quiz: List[str]
    links_lecture: List[str]
    title: str