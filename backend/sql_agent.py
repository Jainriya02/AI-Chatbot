import os
import sqlite3

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from utils import get_schema

load_dotenv(override=True)


def get_groq_api_key():
    api_key = os.getenv("GROQ_API_KEY", "").strip().strip('"').strip("'")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set")
    return api_key

DB_NAME = "database.db"

llm = ChatGroq(
    groq_api_key=get_groq_api_key(),
    model="llama-3.1-8b-instant",
    temperature=0
)


def execute_sql(sql):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(sql)

    result = cursor.fetchall()

    conn.close()

    return result

def ask_sql(question):

    schema = get_schema()

    sql_prompt = f"""
You are an expert SQLite query generator.

Today's date is 15 June 2026.

Database schema:

{schema}

Generate ONLY ONE SQLite SELECT statement.

Rules:

- Database engine is SQLite.
- Return ONLY SQL.
- Never explain anything.
- Never use markdown.
- Never assume any other year.
- Never use DATEDIFF.
- Never use CURDATE.
- Never use GETDATE.
- Never use NOW().
- Never use DATEADD.

If the question mentions:

- order id -> WHERE order_id = ...
- customer -> WHERE customer = ...
- status -> SELECT status
- product -> SELECT product
- return all details -> SELECT *

Do NOT calculate business logic.

Do NOT calculate return eligibility.

Only fetch data.

Question:

{question}

SQL:
"""


    sql = llm.invoke(sql_prompt).content.strip()

    # remove markdown if model returns ```sql
    sql = sql.replace("```sql", "").replace("```", "").strip()

    if not sql.lower().startswith("select"):
        raise Exception("Only SELECT queries are allowed.")

    result = execute_sql(sql)

    return {
        "sql": sql,
        "result":result
    }