from app.pipeline.graph import chatbot
from dotenv import load_dotenv
load_dotenv()


SESSION_ID = "local-user"

def run_cli():
    print("🤖 Conversational RAG System")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break

        response = chatbot.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": SESSION_ID}}
        )

        print("\nAI:", response.content, "\n")


if __name__ == "__main__":
    run_cli()