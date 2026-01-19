from api.safe_sql import answer_question

if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type 'exit'): ").strip()
        if question.lower() == "exit":
            break

        result = answer_question(question)

        print("\nSQL:")
        print(result["sql"] if result["sql"] else "N/A")

        print("\nAnswer:")
        print(result["answer"])

