import os

DOCS_PATH = "fastapi/docs/en"

def load_markdown_files(path):
    docs = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8") as f:
                    docs.append({
                        "text": f.read(),
                        "source": full_path
                    })
    return docs

documents = load_markdown_files(DOCS_PATH)

