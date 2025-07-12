from mas.state import State
from agents.pydantic_models import Objective
from agents.pydantic_models import CurriculumDeps, CurriculumResult
from agents.pydantic_models import SupervisorDeps, CollectDataDeps
from agents.pydantic_models import LectureNoteDeps, Content, QuizInput, EvaluationInput

from agents.clarify_agent import clarify_agent
from agents.curriculum_gen import table_content, curriculum_gen_agent
from agents.supervisor import supervisor_agent
from agents.collect_data import collect_data_agent
from agents.lecture_note_gen import lecture_note_gen_agent
from agents.quiz_gen import quiz_gen_agent
from agents.presentation_gen import presentation_gen_agent
from agents.evaluator import evaluator_agent

from presentation.drive_ops import create_folder, copy_presentation, move_file_to_folder, is_folder_exist
from presentation.google_slide_ops import delete_unnecessary_slide, copy_slide, move_slide, update_presentation_content

from typing import List, Literal, Dict
from langgraph.graph import StateGraph, START, END
import json
from datetime import datetime
from utils.setup import setup_gemini
from utils.stream import run_agent
from utils.Upfile import upload_markdown_to_s3, convert_to_markdown

import nest_asyncio
nest_asyncio.apply()
import uuid
import asyncio


async def clarify_agent_node(state: State):
    deps = Objective(
        session_id = state.get("session_id"),
        user_query = state.get("user_query"),
        subject = "",
        level = "",
        target_audience = "",
        entire_course = False,
        chapters = [],
        thinking = [],
        websocket = state.get("websocket")
    )

    result = await clarify_agent.run(
        "", deps=deps,
        model_settings={'temperature': 0.0}
    )

    # print(result)

    state["objective"] = result.data
    state["next_step"] = "curriculum_gen_agent"
    return state


async def curriculum_gen_agent_node(state: State):
    deps = CurriculumDeps(
        objective = state.get("objective"),
        table_content = table_content
    )

    result = await curriculum_gen_agent.run("", deps=deps)
    
    curriculum = {
        "title": result.data.title,
        "overview": result.data.overview,
        "modules": [
            {
                "title": module.title,
                "content": module.content
            } 
            for module in result.data.modules]
    }

    state["results"]["curriculum"] = curriculum
    state["next_step"] = "supervisor_agent"
    return state


async def supervisor_agent_node(state: State):
    deps = SupervisorDeps(
        curriculum = state.get("results").get("curriculum"),
        todo_list = state.get("todo_list")
    )

    result = await supervisor_agent.run("", deps=deps)
    # print(result.data)

    next_action = result.data.next_action
    state["next_action"] = next_action

    # Convert todo_list from list to dictionary
    if not state.get("todo_list"):
        state["todo_list"] = {}
        for task in result.data.todo_list.tasks:
            task_dict = {
                "task_id": task.task_id,
                "description": task.description,
                "status": task.status
            }

            state["todo_list"][str(task.task_id)] = task_dict

    # print(state.get("todo_list"))
    state["next_step"] = next_action.agent
    state["todo_list"][str(next_action.task_id)]["status"] = "done"

    return state


async def collect_data_agent_node(state: State):
    deps = CollectDataDeps(
        task = state["next_action"]
    )

    # result = await collect_data_agent.run("", deps=deps)
    # print(result.data)

    # ws = state.get("websocket")
    # await ws.send_json({
    #     "role": "agent",
    #     "content": result.data,
    #     "timestamp": str(datetime.now())
    # })

    result = asyncio.run(run_agent(collect_data_agent, state, deps))

    state["results"]["data"] = result

    return state


async def lecture_note_gen_node(state: State):
    print("LECTURE NOTE GEN NODE")
    task = state["next_action"]

    deps = LectureNoteDeps(
        task = task,
        data = state.get("results").get("data")
    )

    # result = await lecture_note_gen_agent.run("", deps=deps)
    # print(result.data, "\n\n\n")

    # ws = state.get("websocket")
    # await ws.send_json({
    #     "role": "agent",
    #     "content": result.data,
    #     "timestamp": str(datetime.now())
    # })
    
    result = asyncio.run(run_agent(lecture_note_gen_agent, state, deps))
    # print(result)

    state["lecture_notes"][task.task_id] = result
    # key = str(uuid.uuid4())
    
    # Get name of lecture note from curriculum
    idx = len(state.get("links_lecture"))
    name = state.get("results").get("curriculum").get("modules")[idx]
    print("=========================",name['title'] )

    link_up = f"{state.get('user_id')}/{state.get('project_id')}/{state.get('session_id')}/lecture_note/"

    print("LINK UP: ", link_up)
    
    link=upload_markdown_to_s3(result,'bookmcs',link_up+name['title']+"LECTURE.pdf")
    state["links_lecture"].append(link)
    return state


async def quiz_gen_node(state: State):
    print("_____QUIZZ_________")
    dep = QuizInput(
        data = state.get("results").get("data")
    )

    result = await quiz_gen_agent.run(" ", deps=dep)

    # saveMessage(result,'QuizzNode')
    state['results']["quiz"] = result.data.dict()
    print("QUIZ: ")
    print(result.data)

    mk=convert_to_markdown(result.data)
    
    next_action = state["next_action"]
    key = str(uuid.uuid4())
    # if key not in state['modules_result']:
    #   state['modules_result'][key] = []
    # state['modules_result'][key].append({
    #     'quiz': result.output
    #       })
    idx = len(state.get("links_quiz"))
    name= state.get("results").get("curriculum").get("modules")[idx]['title']
    link_up = f"{state.get('user_id')}/{state.get('project_id')}/{state.get('session_id')}/quiz/"
    
    link=upload_markdown_to_s3(mk,'bookmcs',link_up+name+"QUIZ.pdf")
    
    # print(link)
    state["links_quiz"].append(link)
    return state


templates = {
    "template_1": "1F5r1P4M0NbiBnssPzz1dvV7J8VYPkKGVyL3AhiCeagQ", 
    "template_2": "1JQzsjIl8nz8x3ane5k5RnKNvYESfTJ-85IxJjd-_GZU",
    "template_3": "1EdOv2fn3vsO1o6mKgwAN6FeWjhnYTwAgaagP5EMDulQ",
    "template_4": "1vF_ZTXWUGyH5Qt5KIMrOw6szJmBcBSbO2Oli0yNapKQ",
    "template_5": "1nNr9z41x-6IWVua7wuzmKMq9b299T8r10eNQ21qrVEg",
}

SELECTED_TEMPLATE = ""

async def presentation_gen_node(state: State):
    print("_____SLIDE_________")
    dep = Content(
        title = state.get("next_action").description,
        content = list(state.get("lecture_notes").values())[-1],
        images = [],
        language = "English"
    )

    result = await presentation_gen_agent.run("", deps=dep)
    
    state['results']["slide"] = result.data.dict()
    print("SLIDE: ")
    # print(result.data)

    # Send Websocket to choose template
    print(f"________________________{state.get('next_action').agent}________________________")
    if state.get("next_action").agent == "presentation_gen_agent" and state.get("presentation_template_url") == "":
        ws = state.get("websocket")
        print("Sending template selection request to WebSocket...")
        await ws.send_json({
            "messageId": "",
            "role": "agent",
            "content": "",
            "timestamp": str(datetime.now()),
            "type": "template"
        })
        print("Waiting for template selection from WebSocket...")
        
        data = await ws.receive_text()
        content = json.loads(data)
        template_id = content["template"]
        SELECTED_TEMPLATE = templates[template_id]

        state["presentation_template_url"] = SELECTED_TEMPLATE
        print(f"Selected template ID: {SELECTED_TEMPLATE}")

    # Work with Google Drive API to copy and edit slide content
    if not is_folder_exist("Presentation"):
        FOLDER_ID = create_folder("Presentation")
    else:
        FOLDER_ID = is_folder_exist("Presentation")

    presentation_name = result.data.slides[0].title
    SOURCE_PRESENTATION_ID = state.get("presentation_template_url")
    TARGET_PRESENTATION_ID = copy_presentation(SOURCE_PRESENTATION_ID, presentation_name)
    move_file_to_folder(TARGET_PRESENTATION_ID, FOLDER_ID)


    TARGET = [slide.layout for slide in result.data.slides]
    SOURCE_TEMPLATE = ["TITLE", "SECTION_HEADER", "TITLE_CONTENT", "CONTENT_IMAGE", "END"]

    CURR_TEMPLATE = delete_unnecessary_slide(TARGET_PRESENTATION_ID, TARGET, SOURCE_TEMPLATE)
    CURR_TEMPLATE = copy_slide(TARGET_PRESENTATION_ID, TARGET, CURR_TEMPLATE)
    CURR_TEMPLATE = move_slide(TARGET_PRESENTATION_ID, TARGET, CURR_TEMPLATE)
    assert CURR_TEMPLATE == TARGET

    update_presentation_content(TARGET_PRESENTATION_ID, slides=result.data.slides, template=TARGET)

    next_action = state["next_action"]
    # state["presentation_urls"].append(
    #     {
    #         "name": presentation_name,
    #         "url": TARGET_PRESENTATION_ID
    #     }
    # )
    
    return state


async def evaluator_node(state: State):
    print("_____EVALUATION_________")
    dep = EvaluationInput(
        lecture_note = state.get('results').get('lecture_note'),
        quiz = state.get('results').get('quizz'),
        slide = state.get('results').get('slide')
    )

    result = await evaluator_agent.run(" ", deps=dep)
    # saveMessage(result,'evaluation_agent_node')
    print("EVALUATION: ")
    # print(result.data)
    state['results']["evaluation"] = result.data.dict()

    next_action = state["next_action"]
    
    return state


def conditional_edges(state: State):
    return state.get("next_step")


graph_builder = StateGraph(State)

graph_builder.add_node("clarify_agent", clarify_agent_node)
graph_builder.add_node("curriculum_gen_agent", curriculum_gen_agent_node)
graph_builder.add_node("supervisor_agent", supervisor_agent_node)
graph_builder.add_node("collect_data_agent", collect_data_agent_node)
graph_builder.add_node("lecture_note_gen_agent", lecture_note_gen_node)
graph_builder.add_node("quiz_gen_agent", quiz_gen_node)
graph_builder.add_node("presentation_gen_agent", presentation_gen_node)
graph_builder.add_node("evaluator_agent", evaluator_node)


graph_builder.add_edge(START, "clarify_agent")
graph_builder.add_edge("clarify_agent", "curriculum_gen_agent")
graph_builder.add_edge("curriculum_gen_agent", "supervisor_agent")


graph_builder.add_conditional_edges(
    "supervisor_agent",
    conditional_edges,
    {
        "collect_data_agent": "collect_data_agent",
        "lecture_note_gen_agent": "lecture_note_gen_agent",
        "presentation_gen_agent": "presentation_gen_agent",
        "evaluator_agent": "evaluator_agent",
        "quiz_gen_agent": "quiz_gen_agent",
        "end": END
    }
)

graph_builder.add_edge("collect_data_agent", "supervisor_agent")
graph_builder.add_edge("lecture_note_gen_agent", "supervisor_agent")
graph_builder.add_edge("presentation_gen_agent", "supervisor_agent")
graph_builder.add_edge("quiz_gen_agent", "supervisor_agent")
graph_builder.add_edge("evaluator_agent", "supervisor_agent")

graph = graph_builder.compile()