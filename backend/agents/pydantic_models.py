from dataclasses import dataclass
from typing import List, Literal, Dict, Any, Optional, Union
from typing_extensions import TypedDict
from pydantic import BaseModel, Field, ConfigDict
from fastapi import WebSocket


# Clarify Models
class Objective(BaseModel):
    session_id: str
    user_query: str
    subject: str
    level: str
    target_audience: str
    entire_course: bool
    chapters: List[str]
    thinking: List[str] = Field(description="Thinking steps of agent")
    websocket: WebSocket

    model_config = ConfigDict(arbitrary_types_allowed=True)


# Supervisor Models
class Task(BaseModel):
    task_id: int = Field(description="Task ID")
    agent: Literal["collect_data_agent", "lecture_note_gen_agent", "presentation_gen_agent", "quiz_gen_agent", "evaluator_agent", "end"]
    description: str = Field(description="Short description about task include: chapter, ...")
    status: Literal["pending", "done"]
    module_id: str = Field(description="ID or name of the module/topic that this task belongs to")

class TODOList(BaseModel):
    tasks: List[Task] = Field(description="List of tasks")

class RunTask(BaseModel):
    task_id: int = Field(description="Task ID")
    agent: Literal["collect_data_agent", "lecture_note_gen_agent", "presentation_gen_agent", "quiz_gen_agent", "evaluator_agent", "end"]
    description: str = Field(description="Short description about task include: chapter, ...")

@dataclass
class SupervisorDeps:
    curriculum: str
    todo_list: TODOList

class SupervisorResult(BaseModel):
    todo_list: TODOList = Field(description = "List of tasks")
    next_action: RunTask


# Curriculum Models
@dataclass
class CurriculumDeps:
    objective: str
    table_content: str

class Module(BaseModel):
    title: str = Field(description="Module name. For example: 1.1 Introduction to AI")
    content: str = Field(description="Submodules for example: 1.1 Introduction to AI: \n - What is AI? ,... and its description.")

class CurriculumResult(BaseModel):
    title: str = Field(description="Course title")
    overview: str = Field(description="Course description, target audience, prerequisite, course objectives,...")
    modules: List[Module] = Field(description="Course modules")


# Collect Data Models
@dataclass
class CollectDataDeps:
    task: RunTask


# Lecture Note Models
@dataclass
class LectureNoteDeps:
    task: RunTask
    data: str

# class LectureNoteResult(BaseModel):
#     title: str = Field(description="title of lecture note")
#     content: str = Field(description="Content of the lecture note")

# Presentation Models
class ImageData(BaseModel):
    image_url: str
    caption: str
    width: int
    height: int

@dataclass
class Content:
    title: str
    content: str
    images: List[ImageData]
    language: str

class BulletPoints(BaseModel):
    subject: str
    points: List[str]

class Description(BaseModel):
    text: str

class Slide(BaseModel):
    title: str = Field(description="title of slide")
    body_text: None | BulletPoints | Description = Field(description="If layout is TITLE_CONTENT or CONTENT_IMAGE, else None")
    reference: str | None = Field(description="Reference link of figures, cite, etc", default=None)
    layout: Literal["TITLE", "SECTION_HEADER", "TITLE_CONTENT", "CONTENT_IMAGE", "END"]
    image_urls: Optional[List[str]]
    page: int

class Presentation(BaseModel):
    title: str
    slides: List[Slide]


# Quiz Models
class Question(BaseModel):
    question: str = Field(description="Question of multichoice")
    option: List[str] = Field(description="List of multiple")
    answer: str = Field(description="Answer of question from option, not A/B/C/D")
    # explain: str = Field(description="Explain the correct answer")
    source: str = Field(description="Extract questions from database or web")

class QuizOutput(BaseModel):
    questions: List[Question]

class QuizInput(BaseModel):
    data: str


# Evaluator Models
class LectureNoteEvaluation(BaseModel):
    completeness: int = Field(ge=1, le=5, description="The completeness of the lecture content")
    logical_flow: int = Field(ge=1, le=5, description="The logical flow and structure of the lecture")
    scientific_accuracy: int = Field(ge=1, le=5, description="The scientific accuracy of the lecture content")
    clarity: int = Field(ge=1, le=5, description="The clarity and understandability of the lecture")
    reference_quality: int = Field(ge=1, le=5, description="The quality and validity of cited references")
    comment: Optional[str] = Field(description="General comments on the lecture note")

class QuizEvaluation(BaseModel):
    difficulty: int = Field(ge=1, le=5, description="The difficulty level of the quiz questions")
    question_clarity: int = Field(ge=1, le=5, description="The clarity and comprehensibility of the questions")
    answer_correctness: int = Field(ge=1, le=5, description="The correctness and appropriateness of the answers")
    explanation_quality: int = Field(ge=1, le=5, description="The quality and clarity of the answer explanations")
    topic_variety: int = Field(ge=1, le=5, description="The diversity of topics covered by the quiz")
    comment: Optional[str] = Field(description="General comments on the quiz")

class SlideEvaluation(BaseModel):
    layout_quality: int = Field(ge=1, le=5)
    aesthetic: int = Field(ge=1, le=5)
    visual_support: int = Field(ge=1, le=5)
    information_accuracy: int = Field(ge=1, le=5)
    readability: int = Field(ge=1, le=5)
    comment: Optional[str]

class EvaluationOutput(BaseModel):
    lecture_note_eval: Optional['LectureNoteEvaluation']
    quiz_eval: Optional['QuizEvaluation']
    slide_eval: Optional['SlideEvaluation']

class EvaluationInput(BaseModel):
    lecture_note: Optional[str]
    quiz: Optional[QuizOutput]
    slide: Optional[Presentation]


