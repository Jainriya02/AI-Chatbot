import os
import sqlite3
import pandas as pd

from rag import (
    load_documents,
    split_documents,
    create_vector_db
)

DOCUMENTS_DIR = "documents"
DATASETS_DIR = "datasets"
DB_NAME = "database.db"


def ingest_documents():

    vectorstore = create_vector_db()

    existing = vectorstore.get()

    indexed_files = set()

    if existing["metadatas"]:
        for metadata in existing["metadatas"]:
            if metadata and "source" in metadata:
                indexed_files.add(metadata["source"])

    pdf_files = [
        file
        for file in os.listdir(DOCUMENTS_DIR)
        if file.lower().endswith(".pdf")
    ]

    for pdf in pdf_files:

        if pdf in indexed_files:
            print(f"✓ {pdf} already indexed")
            continue

        print(f"Embedding {pdf}")

        pdf_path = os.path.join(DOCUMENTS_DIR, pdf)

        documents = load_documents(pdf_path)

        chunks = split_documents(documents)

        for chunk in chunks:
            chunk.metadata["source"] = pdf

        vectorstore.add_documents(chunks)

    print("PDF ingestion completed.")


def ingest_datasets():

    csv_files = [
        file
        for file in os.listdir(DATASETS_DIR)
        if file.lower().endswith(".csv")
    ]

    if not csv_files:
        return

    conn = sqlite3.connect(DB_NAME)

    for csv in csv_files:

        table_name = os.path.splitext(csv)[0]

        print(f"Loading {csv} → {table_name}")

        df = pd.read_csv(
            os.path.join(DATASETS_DIR, csv)
        )

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

    conn.close()

    print("Database updated.")


def ingest():

    print("\n========== INGESTION STARTED ==========\n")

    ingest_documents()

    ingest_datasets()

    print("\n========== INGESTION COMPLETED ==========\n")