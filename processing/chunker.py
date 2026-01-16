from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

MAX_CHUNK_SIZE = 500
OVERLAP = 50
MIN_CHUNK_SIZE = 200

splitter = RecursiveCharacterTextSplitter(
    chunk_size=MAX_CHUNK_SIZE,
    chunk_overlap=OVERLAP
)

def split_by_headers(text):
    sections = []
    current_section = ""

    for line in text.split("\n"):
        if re.match(r"^#{1,6} ", line):
            if current_section:
                sections.append(current_section.strip())
            current_section = line + "\n"
        else:
            current_section += line + "\n"

    if current_section:
        sections.append(current_section.strip())

    return sections


def chunk_docs(docs):
    chunks = []

    for d in docs:
        sections = split_by_headers(d["text"])
        buffer = ""  

        for section in sections:
            if len(buffer) < MIN_CHUNK_SIZE:
                buffer += "\n" + section if buffer else section
                continue

            text_to_chunk = buffer
            buffer = section

            if len(text_to_chunk) <= MAX_CHUNK_SIZE:
                chunks.append({
                    "text": text_to_chunk.strip(),
                    "source": d["source"]
                })
            else:
                sub_chunks = splitter.split_text(text_to_chunk)
                for sub in sub_chunks:
                    chunks.append({
                        "text": sub.strip(),
                        "source": d["source"]
                    })

        if buffer:
            if len(buffer) <= MAX_CHUNK_SIZE:
                chunks.append({
                    "text": buffer.strip(),
                    "source": d["source"]
                })
            else:
                sub_chunks = splitter.split_text(buffer)
                for sub in sub_chunks:
                    chunks.append({
                        "text": sub.strip(),
                        "source": d["source"]
                    })

    return chunks
