from pydantic_ai import Agent, RunContext
from agents.pydantic_models import LectureNoteDeps

lecture_note_gen_agent = Agent(
    'google-gla:learnlm-2.0-flash-experimental', #'google-gla:gemini-2.5-flash', #, 'google-gla:learnlm-2.0-flash-experimental', #
    deps_type = LectureNoteDeps,
    result_type = str
)

@lecture_note_gen_agent.system_prompt
def system_prompt(ctx: RunContext) -> str:
    return f"""
    Given data {ctx.deps.data}
    Create a lecture note for {ctx.deps.task.description}
    """