import re

def clean_docs(docs):
    cleaned = []
    for d in docs:
        text = d["text"]

        # Remove FastAPI callout blocks (/// tip, /// note, etc.)
        text = re.sub(r"///.*?\n", "", text)

        # Remove image tags
        text = re.sub(r"<img.*?>", "", text)

        # Remove HTML links but keep text
        text = re.sub(r"<a.*?>(.*?)</a>", r"\1", text)

        # Remove multiple blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Strip whitespace
        text = text.strip()

        cleaned.append({
            "text": text,
            "source": d["source"]
        })

    return cleaned
