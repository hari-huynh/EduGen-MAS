import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import BaseModel
from typing import Literal

from presentation.google_slide_auth import google_slide_auth 

class ClassroomMaterial(BaseModel):
    title: str
    url: str

creds = google_slide_auth()

service = build("classroom", "v1", credentials=creds)

def classroom_create_course(name, description, section="", description_heading=""):
    try:
        course = {
            "name": name,
            "section": section,
            "descriptionHeading": description_heading,
            "description": description,
            "ownerId": "me",
            "courseState": "PROVISIONED", #
        }

        course = service.courses().create(body=course).execute()

        return course.get("id")

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def classroom_get_course(course_id):
    course = None
    try:
        course = service.courses().get(id=course_id).execute()
        print(f"Course found : {course.get('name')}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        print(f"Course not found: {course_id}")
        return error
    return course


def classroom_list_courses():
    try:
        courses = []
        page_token = None

        while True:
            response = (
                service.courses().list(pageToken=page_token, pageSize=100).execute()
            )
            courses.extend(response.get("courses", []))
            page_token = response.get("nextPageToken", None)

            if not page_token:
                break

        if not courses:
            print("No courses found.")
            return

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def classroom_create_coursework(course_id, title, description, materials):
    try:
        coursework = {
            "title": title,
            "description": description,
            "materials": [
                [{"link": {"url": url}} for url in materials]
            ],
            "workType": "ASSIGNMENT",
            "state": "PUBLISHED",
        }

        coursework = (
            service.courses().courseWork()
                    .create(courseId=course_id, body=coursework).execute()
            )

        print(f"Assignment created with ID {coursework.get('id')}")
        return coursework

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def classroom_create_topic(course_id, name):
    topic = {
        "name": name
    }

    try:
        response = service.courses().topics().create(
            courseId= course_id,
            body=topic
        ).execute()

        return response.get("topicId")
    except HttpError as err:
        return err


# {
#                 "driveFile": {  # Drive file that is used as material for course work. # Google Drive file material.
#                     "driveFile": {  # Representation of a Google Drive file. # Drive file details.
#                         "id": "1EdOv2fn3vsO1o6mKgwAN6FeWjhnYTwAgaagP5EMDulQ",  # Drive API resource ID.
#                     },
#                     "shareMode": "VIEW",  # Mechanism by which students access the Drive item.
#                 },
#             }

def classroom_create_coursework_material(course_id, title, description, materials, topic_id):
    coursework_material = {
        "title": title,
        "description": description,
        "materials": [
            { "link": { "url": mat.url, "title": mat.title } } for mat in materials
        ],
        "topicId": topic_id
    }

    response = service.courses().courseWorkMaterials().create(courseId=course_id, body=coursework_material).execute()


if __name__ == "__main__":
    # Create a new course
    course_id = classroom_create_course("Introduction to AI", "Period 1", "AI course", "An intermediate Introduction to AI course for undergraduate students")
    topic_id = classroom_create_topic(course_id, "Intelligent Agents")

    materials = [
        ClassroomMaterial(url="https://bookmcs.s3.ap-southeast-1.amazonaws.com/test.pdf", title="Intelligent Agent Lecture Note", type="lecture_note"),
        ClassroomMaterial(url="https://bookmcs.s3.ap-southeast-1.amazonaws.com/user_2ynz9fynHRdacvtVPpQmcF3pgXT/c73ef01c-8bba-47b0-8c3a-30a8f9cbae5d/e40bbd61-7fc0-473b-be39-30157e64e841/quiz/9d09c3ed-cf51-4627-9408-b05cda29497d.pdf", title="Intelligent Agent Lecture Note", type="lecture_note"),
    ]

    classroom_create_coursework_material(course_id, "Intelligent Agents Lecture Notes", "", materials, topic_id)