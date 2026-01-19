# What pieces would I need?
Do you like building Lego from your imagination? Do you sometimes wonder what pieces you might need to transfer your imagination into an actual Lego build? This conversational SQL might help you pick the pieces you need to build your Lego model!

## Limitation
The LLM could only inspect the given database using SQL queries. For a high-reasoning question, such as "What pieces would I need to build a cat of 15-cm high?", the LLM would give a predesignated error message. The person should reroute the questions to get a desired answer. For example, ask the following questions:
- How many sets are there with four-legged animals?
- What sets have a cat in there?
- What pieces does [this set] have? ([this set] has to be specified based on the previous answer)
- Give me the element numbers of [these pieces]
- Give me all the available colours of [these pieces] 

## Usage
Always run from the project root: `python -m api.run`. All Q&A's are recorded in `qnas.txt`. 

## Database and LLM
The database is built with data sourced from Rebrickable. The conversational SQL is powered by Groq. (With the **Q**, not the k.)