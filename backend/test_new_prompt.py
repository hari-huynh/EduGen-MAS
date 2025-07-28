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
from agents.pydantic_models import RunTask

from typing import List, Literal, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
import json
from datetime import datetime
from utils.setup import setup_gemini


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


def clarify_agent_node(state: State):
    deps = Objective(
        user_query = state.get("user_query"),
        subject = "",
        level = "",
        target_audience = "",
        entire_course = False,
        chapters = [],
        thinking = [],
    )

    result = clarify_agent.run(
        "", deps=deps,
        model_settings={'temperature': 0.0}
    )

    # print(result)

    state["objective"] = result.data
    state["next_step"] = "curriculum_gen_agent"
    return state


def curriculum_gen_agent_node(state: State):
    deps = CurriculumDeps(
        objective = state.get("objective"),
        table_content = table_content
    )

    result = curriculum_gen_agent.run("", deps=deps)
    
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


def supervisor_agent_node(state: State):
    deps = SupervisorDeps(
        curriculum = state.get("results").get("curriculum"),
        todo_list = state.get("todo_list")
    )

    result = supervisor_agent.run("", deps=deps)
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


def collect_data_agent_node(state: State):
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

    result = collect_data_agent.run("", deps=deps)

    state["results"]["data"] = result

    return state


def lecture_note_gen_node(state: State):
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
    
    result = lecture_note_gen_agent.run("", deps=deps)
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


def quiz_gen_node(state: State):
    print("_____QUIZZ_________")
    dep = QuizInput(
        data = state.get("results").get("data")
    )

    result = quiz_gen_agent.run(" ", deps=dep)

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
    #       }
    
    return state


def presentation_gen_node(state: State):
    print("_____SLIDE_________")
    dep = Content(
        title = state.get("next_action").description,
        content = list(state.get("lecture_notes").values())[-1],
        images = [],
        language = "English"
    )

    result = presentation_gen_agent.run("", deps=dep)
    
    state['results']["slide"] = result.data.dict()
    print("SLIDE: ")
    # print(result.data)

    return state


def evaluator_node(state: State):
    print("_____EVALUATION_________")
    dep = EvaluationInput(
        lecture_note = state.get('results').get('lecture_note'),
        quiz = state.get('results').get('quizz'),
        slide = state.get('results').get('slide')
    )

    result = evaluator_agent.run(" ", deps=dep)
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


if __name__ == "__main__":
    user_query = input("Enter your query:")

    

