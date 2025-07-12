from pydantic_ai import Agent, RunContext
from agents.pydantic_models import CurriculumDeps, CurriculumResult
from utils.setup import setup_gemini

setup_gemini()


curriculum_gen_agent = Agent(
    'google-gla:gemini-2.0-flash', #    'google-gla:learnlm-2.0-flash-experimental', #         
    deps_type=CurriculumDeps,
    result_type = CurriculumResult
)

@curriculum_gen_agent.system_prompt
def system_prompt(ctx: RunContext) -> str:
    return f"""
    Base on course objective {ctx.deps.objective} and table of content of book: {ctx.deps.table_content}.
    Select the appropriate content from this to create a detailed curriculum for the course.
    Only return the curriculum.
    """

table_content = """
2 Intelligent Agents
Agents and Environments
Good Behavior: The Concept of Rationality
The Nature of Environments.
The Structure of Agents
Summary
Bibliographical and Historical Notes
II Problem-solving
3 Solving Problems by Searching
Problem-Solving Agents.
Example Problems
Search Algorithms
Uninformed Search Strategies
Informed (Heuristic) Search Strategies
Heuristic Functions
Summary
Bibliographical and Historical Notes

7 Logical Agents
Knowledge-Based Agents
The Wumpus World
Logic .
Propositional Logic: A Very Simple Logic
Propositional Theorem Proving
Effective Propositional Model Checking
Agents Based on Propositional Logic
Summary
Bibliographical and Historical Notes
""" 
