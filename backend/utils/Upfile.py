
from agents.pydantic_models import QuizOutput
import io
import boto3
import markdown
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from dotenv import load_dotenv

load_dotenv()

def convert_to_markdown(data: QuizOutput) -> str:
    md = "# **Data Mining Quiz Questions**\n\n"

    for idx, item in enumerate(data.questions, 1):
        question = item.question.strip()
        options = item.option
        answer = item.answer.strip()
        # explanation = item.explain.strip()
        source = item.source.strip()

        md += f"## **Question {idx}**: {question}\n\n"
        for opt in options:
            opt_clean = opt.strip()
            if opt_clean == answer:
                md += f"- **{opt_clean}**\n"
            else:
                md += f"- {opt_clean}\n"

        # if explanation:
        #     md += f"\n> **Explanation**: {explanation}\n"

        md += f"> **Answer**: {answer}\n"
        md += f"> **Source**: {source}\n"
        md += "\n---\n"

    return md



def upload_markdown_to_s3(markdown_text: str, s3_bucket: str, s3_key: str):
    # Convert markdown to HTML (only basic text)
    html = markdown.markdown(markdown_text)

    # Prepare PDF buffer
    pdf_io = io.BytesIO()
    doc = SimpleDocTemplate(pdf_io)
    styles = getSampleStyleSheet()
    story = []

    # Split HTML into paragraphs (⚠ only simple <p> and <h1>/<h2>)
    for line in html.split('\n'):
        line = line.strip()
        if not line:
            continue
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 12))

    doc.build(story)
    pdf_io.seek(0)

    # Upload to S3
    s3 = boto3.client(
        "s3",
        aws_access_key_id= os.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key= os.get('AWS_SECRET_ACCESS_KEY'),
        region_name="ap-southeast-1"
    )

    s3.upload_fileobj(pdf_io, s3_bucket, s3_key, ExtraArgs={"ContentType": "application/pdf"})

    return f"https://{s3_bucket}.s3.ap-southeast-1.amazonaws.com/{s3_key}"