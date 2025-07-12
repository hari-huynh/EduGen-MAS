import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from presentation.google_slide_auth import google_slide_auth
from presentation.google_slide_ops import SlideOps


def create_folder(filename: str):
  creds = google_slide_auth()

  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)
    file_metadata = {
        "name": filename,
        "mimeType": "application/vnd.google-apps.folder",
    }

    # pylint: disable=maybe-no-member
    file = service.files().create(body=file_metadata, fields="id").execute()
    print(f'Folder ID: "{file.get("id")}".')
    return file.get("id")

  except HttpError as error:
    print(f"An error occurred: {error}")
    return None


def copy_presentation(presentation_id, copy_title):
  creds = google_slide_auth()

  try:
    drive_service = build("drive", "v3", credentials=creds)
    body = {"name": copy_title}
    drive_response = (
        drive_service.files().copy(fileId=presentation_id, body=body).execute()
    )
    presentation_copy_id = drive_response.get("id")

  except HttpError as error:
    print(f"An error occurred: {error}")
    print("Presentations not copied")
    return error

  return presentation_copy_id


def move_file_to_folder(file_id, folder_id):
  creds = google_slide_auth()

  try:
    # call drive api client
    service = build("drive", "v3", credentials=creds)

    # pylint: disable=maybe-no-member
    # Retrieve the existing parents to remove
    file = service.files().get(fileId=file_id, fields="parents").execute()
    previous_parents = ",".join(file.get("parents"))
    # Move the file to the new folder
    file = (
        service.files()
        .update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields="id, parents",
        )
        .execute()
    )
    return file.get("parents")

  except HttpError as error:
    print(f"An error occurred: {error}")
    return None

def is_folder_exist(folder_name):
  creds = google_slide_auth()

  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)
    
    while True:
      response = (
          service.files()
          .list(
              q="mimeType='application/vnd.google-apps.folder'",
              spaces="drive",
          )
          .execute()
      )

      folders = { file["name"]: file["id"] for file in response["files"] }
      return folders.get(folder_name)

  except HttpError as error:
    print(f"An error occurred: {error}")
    folders = None