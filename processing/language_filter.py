def filter_english(docs):
    return [d for d in docs if d["text"].isascii()]
