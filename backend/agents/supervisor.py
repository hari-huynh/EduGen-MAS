from pydantic_ai import Agent, RunContext
from agents.pydantic_models import SupervisorDeps, SupervisorResult
from utils.setup import setup_gemini

setup_gemini()

supervisor_agent = Agent(
    'google-gla:gemini-2.0-flash', #'google-gla:learnlm-2.0-flash-experimental', # 
    deps_type = SupervisorDeps,
    result_type = SupervisorResult
)

@supervisor_agent.system_prompt
def system_prompt(ctx: RunContext) -> str:
    return f"""
    Given the following information:
    * Curriculum:
    {ctx.deps.curriculum}

    * TODO List include tasks need to act to create learning material:
    {ctx.deps.todo_list}

    * Agents Missions:
    - 'collect_data_agent': Retrieve data from database and search information from the internet.
    - 'lecture_note_gen_agent': Create lecture note for course.
    - 'quiz_gen_agent': Create multi-choice question for course.
    - 'presentation_gen_agent': Create slides for presentation.
    - 'evaluator_agent': Evaluate generated content from agents.
    - 'end': Terminate when created course successfully.


    If TODO List is empty: Planning, create tasks for each curriculum module and return todo_list
    Else, base on TODO list in order to instruct the others agent to complete tasks by select next_action from TODO List.
    If all task from TODO List is done, return next_action = 'end'
    """