from langchain_core.runnables import RunnableLambda
from app.prompts import CONDENSE_PROMPT, ANSWER_PROMPT
from app.models import chat_model, llm_with_tools   
from app.retrieval import hybrid_retrieve, manual_hybrid_retrieval, rerank_documents, build_context

model = chat_model()

def query_expand(query):
    prompt = f"""Generate 3 different variations of this query that would help retrieve relevant documents:

    Original query: {query}

    Return 3 alternative queries that rephrase or approach the same question from different angles."""
    return prompt


# SMALL_TALK = {
#     "hi", "hello", "hey", "thanks", "thank you",
#     "bye", "goodbye", "how are you", "what's up", "ok", "okay"
# }

# router_node = RunnableLambda(
#     lambda x: (
#         # STOP PIPELINE → direct LLM response
#         model.invoke(x["input"])
#         if any(phrase in x["input"].lower() for phrase in SMALL_TALK)
#         # CONTINUE PIPELINE → pass data forward
#         else x
#     )
# )


standalone_node = RunnableLambda(
    lambda x: {
        "standalone": model.invoke(
            CONDENSE_PROMPT.format(
                chat_history=x["history"],
                question=x["input"]
            )
        ).content,
        "history": x["history"],
        "input": x["input"]
    }
)


multiquery_node = RunnableLambda(
    lambda x: {
        "queries": llm_with_tools.invoke(
            query_expand(x["standalone"])
        ).queries,
        "history": x["history"],
        "input": x["input"],
        "standalone": x["standalone"]
    }
)

hybrid_node = RunnableLambda(
    lambda x: {
        "docs": list({
            d.page_content: d
            for d in (
                hybrid_retrieve(x["queries"]) +
                manual_hybrid_retrieval(x["standalone"])
            )
        }.values()),
        "history": x["history"],
        "input": x["input"],
        "standalone": x["standalone"]
    }
)

rerank_node = RunnableLambda(
    lambda x: {
        "docs": rerank_documents(
            x["standalone"],
            x["docs"]
        )[0],
        "history": x["history"],
        "input": x["input"],
        "standalone": x["standalone"]
    }
)


context_node = RunnableLambda(
    lambda x: {
        "context": build_context(x["docs"]),
        "history": x["history"],
        "input": x["input"],
        "standalone": x["standalone"]
    }
)

def answer_with_fallback(x):
    context = x["context"].strip()
    question = x["input"]
    history = x["history"]

    # --- Case 1: No relevant docs found ---
    if not context or len(context) < 100:
        fallback_prompt = f"""
You are a friendly assistant.

The user asked:
{question}

Start your answer with:
"This is not present in the documents, but based on my general knowledge:"

Then answer naturally.
"""
        return model.invoke(fallback_prompt)

    # --- Case 2: Docs found → normal RAG ---
    return model.invoke(
        ANSWER_PROMPT.format(
            context=context,
            chat_history=history,
            question=question
        )
    )



answer_node = RunnableLambda(answer_with_fallback)

