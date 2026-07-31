import json
import os
import time

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from rag import ask_rag
from sql_agent import ask_sql, execute_sql

load_dotenv(override=True)


def get_groq_api_key():
    api_key = os.getenv("GROQ_API_KEY", "").strip().strip('"').strip("'")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set")
    return api_key


llm = ChatGroq(
    groq_api_key=get_groq_api_key(),
    model="llama-3.1-8b-instant",
    temperature=0
)


def create_plan(question):

    planner_prompt = f"""
You are an AI planner.

Available tools:

RAG
- company policies
- HR
- leave
- refund
- return
- shipping
- FAQs

SQL
- orders
- customers
- products
- revenue
- amount
- dates
- status

Rules:
- Return only JSON.
- Use RAG if documents are needed.
- Use SQL if database is needed.
- Use both if both are required.
- If unrelated, return empty steps.

Format:

{{
  "reason":"",
  "steps":[
    {{
      "tool":"RAG",
      "goal":"..."
    }}
  ]
}}

Question:
{question}
"""
    response = llm.invoke(planner_prompt).content
    response = response.replace("```json", "").replace("```", "").strip()

    return json.loads(response)


def ask_agent(question):
    question_original = question
    question = question.strip().lower()

    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "heyy",
        "good morning",
        "good afternoon",
        "good evening",
    }

    thanks = {"thanks", "thank you", "thankyou"}

    if question in greetings:
        return {
            "tool": "NONE",
            "answer": "Hello! How can I help you today?",
        }

    if question in thanks:
        return {
            "tool": "NONE",
            "answer": "You're welcome! Let me know if you need anything else.",
        }

    t = time.time()
    plan = create_plan(question_original)
    print("Planner:", time.time() - t)

    print("\n========== AGENT PLAN ==========")
    print("Reason:", plan.get("reason", ""))

    if not plan.get("steps"):
        return {"tool": "NONE", "answer": "I don't have that information."}

    rag_context = ""
    sql_query = None
    sql_result = None
    steps = []

    for i, step in enumerate(plan["steps"], start=1):
        tool = step.get("tool")
        goal = step.get("goal")

        print(f"\nStep {i}")
        print("Tool :", tool)
        print("Goal :", goal)

        if tool == "RAG":
            t = time.time()
            rag = ask_rag(goal)
            print("RAG:", time.time() - t)
            rag_context = rag.get("context", "")
            steps.append(
                {
                    "tool": "RAG",
                    "goal": goal,
                    "documents": rag.get("documents", []),
                }
            )

        elif tool == "SQL":
            t = time.time()
            sql = ask_sql(goal)
            print("SQL:", time.time() - t)
            sql_query = sql.get("sql")
            sql_result = sql.get("result")
            steps.append({"tool": "SQL", "goal": goal, "sql": sql_query})

    print("\n========== EXECUTION COMPLETE ==========")

    final_prompt = f"""
You are a helpful company assistant.

Today's date is 15 June 2026.

Answer ONLY using the information below.

If the information is insufficient, reply exactly:

I don't have that information.

------------------------------------

User Question:

{question_original}

------------------------------------

Retrieved Documents:

{rag_context}

------------------------------------

Generated SQL:

{sql_query}

------------------------------------

SQL Result:

{sql_result}

------------------------------------

Rules:

- Answer naturally like a helpful company assistant.
- Use the retrieved documents ONLY for company policies and documentation.
- Use the SQL results ONLY for order and database information.
- If both document context and SQL results are available, combine them into a single coherent answer.
- Never invent or assume information that is not present in the retrieved documents or SQL results.
- If SQL returns no matching records, clearly state that no matching records were found.
- If the retrieved document context is empty, do not generate or assume any policy information.
- Do NOT expose the raw SQL result or document context.
- Do NOT display data as a large markdown table unless the user explicitly requests it.
- When multiple records are returned, summarize them naturally. Mention the total number of records and highlight the most relevant or recent ones instead of listing everything.
- If all available information is insufficient to answer the user's question, reply exactly:
  I don't have that information.
- Return a clear, concise, conversational response.
"""

    t = time.time()
    answer = llm.invoke(final_prompt).content
    print("Final:", time.time() - t)

    tools_used = list(dict.fromkeys(step["tool"] for step in steps))

    return {
     "tool": tools_used if len(tools_used) > 1 else tools_used[0],
     "answer": answer,
     "sql": sql_query if sql_query else None,
     "documents": rag_context if rag_context else None,
     "steps": steps if len(tools_used) > 1 else None,
     }