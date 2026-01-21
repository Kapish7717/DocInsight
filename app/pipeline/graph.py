from langchain_core.runnables import RunnableWithMessageHistory
from app.pipeline.nodes import (
    standalone_node,
    multiquery_node,
    hybrid_node,
    rerank_node,
    context_node,
    answer_node,
)
from app.memory import get_history

pipeline = (
    standalone_node
    | multiquery_node
    | hybrid_node
    | rerank_node
    | context_node
    | answer_node
)

chatbot = RunnableWithMessageHistory(
    pipeline,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)