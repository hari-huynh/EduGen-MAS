from vectorDB import setup_vector_store
from huggingFace_utils import embedding

with open("D:/PROJECT/EduGen-MAS/backend/data/textFull.txt", "r", encoding="utf-8") as f:
    text = f.read()
    
lines = text.splitlines()
grouped = []
current_group = ""
for line in lines:
    if line.strip().startswith('[Title'):
        if current_group.strip():
            grouped.append(current_group.strip())
        current_group = line + "\n"
    else:
        current_group += line + "\n"
if current_group.strip():
    grouped.append(current_group.strip())

embedddings=embedding()

print("Stratup vector store...")
setup_vector_store(grouped, embedddings)
