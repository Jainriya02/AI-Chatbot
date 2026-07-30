import os
import sqlite3

DB_NAME = "database.db"
DOCUMENT_FOLDER = "documents"


def get_schema():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    tables = cursor.fetchall()

    schema = ""

    for table in tables:

        table_name = table[0]

        schema += f"\nTable: {table_name}\nColumns:\n"

        cursor.execute(f"PRAGMA table_info({table_name})")

        columns = cursor.fetchall()

        for column in columns:
            schema += f"- {column[1]}\n"

    conn.close()

    return schema


def get_document_list():

    docs = []

    for file in os.listdir(DOCUMENT_FOLDER):

        if file.lower().endswith(".pdf"):
            docs.append(file)

    return "\n".join(f"- {doc}" for doc in docs)