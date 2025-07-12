from huggingFace_utils import *
# from model_smry import *
from unstructured_utils import *
from vectorDB import *

print("_______CHUNKING____________")
chunks= chunk_data('D:/KLTN2/AI004.pdf')
print("______Succcessec_chunking_____")


# print('________Saving Image_______')
json_img=save_image(chunks)
with open('data_image6.json', 'w') as json_file:
    json.dump(json_img, json_file, indent=4)


print("_________Text_______________")
text_chunk=chunk_text(chunks)
# with open("textFull.txt", "a", encoding="utf-8") as f:
#     # f.write(text_chunk)
#     for line in text_chunk:
#         f.write(line + "\n")

# print("______Summary________________")
# text_summary=summarize_text(text_chunk)


embedddings=embedding()

# print("______Vector DB__________")

setup_vector_store(text_chunk, embedddings)

# loaded_vector_store = Chroma(
#     collection_name="example_collection2",
#     embedding_function=embedddings,  # Phải sử dụng cùng embedding function
#     persist_directory="./chroma_langchain_db"
# )

# test=loaded_vector_store.similarity_search(
#     "  DEEP LEARNING FORNATURALLANGUAGE PROCESSING ? ",
#     k=2,
# )

# print(test)