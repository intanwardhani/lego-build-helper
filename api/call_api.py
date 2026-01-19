import os
from groq import Groq
from dotenv import load_dotenv

from src.vars import SYSTEM_PROMPT

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def nl_to_sql(schema: str, question: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
                                Schema:
                                {schema}

                                Question:
                                {question}
                                """
            }
        ],
    )

    return response.choices[0].message.content.strip() # pyright: ignore[reportOptionalMemberAccess]
