# Stage 3 - AI Chatbot with Chat History

An AI chatbot application built with Streamlit, FastAPI, Gemini API, and PostgreSQL.

This stage extends the previous chatbot architecture by adding persistent chat management and conversation history.

## Architecture

```text
User
  ↓
Streamlit Frontend
  ↓
FastAPI Backend
  ├── Gemini API
  ├── PostgreSQL
  │     └── Chat metadata
  └── Local Chat Files
        └── Conversation history
```

## Features

- AI-powered chatbot using Gemini
- Streamlit web interface
- FastAPI backend
- PostgreSQL database integration
- Create and manage multiple chats
- Persistent chat history
- Continue previous conversations
- Chat metadata stored in PostgreSQL
- Conversation messages stored locally
- Automatic last-update tracking

## Technologies

- Python
- Streamlit
- FastAPI
- Google Gemini API
- PostgreSQL
- SQLAlchemy
- Psycopg2
- REST API

## Project Structure

```text
stage-3-chat-history/
├── backend.py
├── chatbot.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── chat_history/
```

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS chats (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Environment Variables

Create a `.env` file using `.env.example` as a template:

```env
GEMINI_API_KEY=your_api_key_here

DB_NAME=chatbot_db
DB_USER=chatbot_user
DB_PASSWORD=your_database_password_here
DB_HOST=127.0.0.1
DB_PORT=5432
```

Never commit the `.env` file to GitHub.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the FastAPI backend:

```bash
uvicorn backend:app --reload
```

Then start the Streamlit frontend in another terminal:

```bash
streamlit run chatbot.py
```

FastAPI documentation is available locally at:

```text
http://127.0.0.1:8000/docs
```

## Stage Progression

- Stage 1: Basic Streamlit + Gemini chatbot
- Stage 2: Streamlit + FastAPI + Gemini architecture
- Stage 3: PostgreSQL + persistent chat history