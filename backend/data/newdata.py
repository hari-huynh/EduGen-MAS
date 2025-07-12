from docling.document_converter import DocumentConverter

def split_markdown_by_title(filepath, heading_prefix="#"):
    converter = DocumentConverter()
    result = converter.convert(filepath)
    markdown_text=result.document.export_to_markdown()
    
    lines = markdown_text.splitlines()
    grouped = []
    current_group = ""
    for line in lines:
        if line.strip().startswith(heading_prefix):
            if current_group.strip():
                grouped.append(current_group.strip())
            current_group = line + "\n"
        else:
            current_group += line + "\n"
    if current_group.strip():
        grouped.append(current_group.strip())
    return grouped

if __name__ == "__main__":
    filepath = "https://bookmcs.s3.ap-southeast-1.amazonaws.com/SOMET_2025.pdf"  
    grouped_markdown = split_markdown_by_title(filepath)
    for idx, group in enumerate(grouped_markdown):
        print(f"Group {idx + 1}:\n{group}\n")
        break 