
from langchain_core.prompts import PromptTemplate

CONDENSE_PROMPT = PromptTemplate.from_template("""
Given the following conversation and a follow up question,
rewrite the follow up question to be a standalone question.

Chat History:
{chat_history}

Follow Up Question:
{question}

Standalone question:
""")


ANSWER_PROMPT = PromptTemplate.from_template("""
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Chat History:
{chat_history}

Question:
{question}

Answer:
""")