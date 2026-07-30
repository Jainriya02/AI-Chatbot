#  AI Chatbot

An intelligent customer support chatbot built using FastAPI, LangChain, ChromaDB, SQLite, Groq LLM, and Next.js.

The chatbot demonstrates an Agentic AI architecture where an AI Planner first decides which tool(s) are required to answer a user's question.

Depending on the query, the agent can:

- Search company documents using Retrieval-Augmented Generation (RAG)
- Query structured business data using Text-to-SQL
- Combine information from both sources to generate a final response

---

# Features

- Agent-based routing
- Retrieval-Augmented Generation
- Text-to-SQL
- Multi-tool reasoning
- FastAPI backend
- Next.js frontend
- ChromaDB vector database
- SQLite database
- Automatic PDF ingestion
- Automatic CSV ingestion

---

# Tech Stack

## Backend

- Python
- FastAPI
- LangChain
- Groq API
- ChromaDB
- SQLite

## Frontend

- Next.js
- React
- TypeScript

## Embedding Model

sentence-transformers/all-MiniLM-L6-v2

## LLM

Llama-3.1-8B-Instant (Groq)

---

# Architecture

```
                User
                  │
                  ▼
         Next.js Frontend
                  │
                  ▼
          FastAPI Backend
                  │
                  ▼
            Planner Agent
                  │
       ┌──────────┴──────────┐
       │                     │
       ▼                     ▼
     RAG Tool            SQL Tool
       │                     │
       ▼                     ▼
   ChromaDB             SQLite DB
       │                     │
       └──────────┬──────────┘
                  ▼
             Final LLM
                  │
                  ▼
             Final Answer
```

---

# Project Structure

```
backend/
│
├── agent.py
├── rag.py
├── sql_agent.py
├── ingest.py
├── main.py
├── utils.py
├── database.db
├── chromadb/
├── documents/
├── datasets/
└── requirements.txt

frontend/
│
├── app/
│   ├── page.tsx
│   ├── layout.tsx
│   └── globals.css
│
├── components/
│   ├── Chat.tsx
│   └── Message.tsx
│
├── package.json
└── tsconfig.json

README.md
```

---

# How the Agent Works

Unlike a traditional chatbot that always queries every data source, this project uses an AI Planner Agent.

The planner first analyzes the user's question and creates an execution plan.

Examples:

### Example 1

User:

```
What is the company's return policy?
```

Plan:

```
RAG
```

---

### Example 2

User:

```
Show my orders.
```

Plan:

```
SQL
```

---

### Example 3

User:

```
Can order ORD-1001 be returned?
```

Plan:

```
RAG
↓

SQL
↓

Combine Results
↓

Final Answer
```

This reduces unnecessary tool usage and demonstrates agentic reasoning.

---

# RAG Pipeline

The Retrieval-Augmented Generation pipeline performs the following steps:

1. Load PDF documents
2. Split documents into chunks
3. Generate embeddings
4. Store embeddings in ChromaDB
5. Retrieve the most relevant chunks
6. Provide retrieved context to the LLM

---

# Text-to-SQL Pipeline

For structured business data:

1. Read database schema
2. LLM generates a SQLite SELECT query
3. Execute the query
4. Retrieve matching rows
5. Send SQL results to the final LLM for response generation

Only **SELECT** queries are allowed.

---

# Document Ingestion

New PDF documents can be added by placing them inside:

```
documents/
```

Run:

```bash
python ingest.py
```

The ingestion script:

- Detects new PDFs
- Splits them into chunks
- Creates embeddings
- Stores them in ChromaDB

Previously indexed documents are skipped.

---

# Dataset Ingestion

CSV datasets can be added inside:

```
datasets/
```

Running

```bash
python ingest.py
```

automatically loads CSV files into the SQLite database.

---

# API

## POST /chat

Request

```json
{
  "question": "Can order ORD-1001 be returned?"
}
```

Example Response

```json
{
  "tool": "MULTI_TOOL",
  "answer": "...",
  "sql": "SELECT ..."
}
```

---

# Installation

## Backend

```bash
cd backend

pip install -r requirements.txt
```

Create a `.env` file

```
GROQ_API_KEY=your_api_key
```

Run ingestion

```bash
python ingest.py
```

Start server

```bash
uvicorn main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Design Decisions

### Why FastAPI?

FastAPI provides a lightweight, high-performance backend with automatic API documentation and asynchronous request handling.

---

### Why ChromaDB?

ChromaDB is an open-source vector database that integrates seamlessly with LangChain and is well suited for local RAG applications.

---

### Why SQLite?

SQLite is lightweight, requires no external database server, and is sufficient for demonstrating Text-to-SQL capabilities.

---

### Why Groq?

Groq provides low-latency inference for open-source LLMs, making it suitable for interactive chatbot applications.

---


# Future Improvements

- Streaming responses
- Conversation memory
- Query caching
- Parallel tool execution
- SQL validation layer
- Hybrid retrieval (semantic + keyword search)
- Support for additional tools and APIs

---

