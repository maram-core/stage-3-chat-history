import os
import uuid
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel
from sqlalchemy import text

from database import SessionLocal

load_dotenv()

app = FastAPI()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

CHAT_FOLDER = "chat_history"

os.makedirs(CHAT_FOLDER, exist_ok=True)


class CreateChatRequest(BaseModel):
    name: str


class ChatMessageRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Stage 3 Chat History API is running"
    }


@app.post("/chats")
def create_chat(request: CreateChatRequest):
    chat_id = str(uuid.uuid4())
    file_path = os.path.join(CHAT_FOLDER, f"{chat_id}.txt")

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("")

        db = SessionLocal()

        db.execute(
            text("""
                INSERT INTO chats (id, name, file_path, last_update)
                VALUES (:id, :name, :file_path, :last_update)
            """),
            {
                "id": chat_id,
                "name": request.name,
                "file_path": file_path,
                "last_update": datetime.now()
            }
        )

        db.commit()
        db.close()

        return {
            "id": chat_id,
            "name": request.name,
            "file_path": file_path
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/chats")
def get_chats():
    db = SessionLocal()

    try:
        result = db.execute(
            text("""
                SELECT id, name, file_path, last_update
                FROM chats
                ORDER BY last_update DESC
            """)
        )

        chats = []

        for row in result:
            chats.append({
                "id": row.id,
                "name": row.name,
                "file_path": row.file_path,
                "last_update": row.last_update
            })

        return chats

    finally:
        db.close()


@app.post("/chats/{chat_id}/message")
def send_message(chat_id: str, request: ChatMessageRequest):
    db = SessionLocal()

    try:
        result = db.execute(
            text("""
                SELECT file_path
                FROM chats
                WHERE id = :id
            """),
            {
                "id": chat_id
            }
        ).fetchone()

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Chat not found"
            )

        file_path = result.file_path

        history = ""

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                history = file.read()

        prompt = f"""
Previous conversation:
{history}

User: {request.message}
Assistant:
"""

        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )

        assistant_response = response.text

        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"User: {request.message}\n")
            file.write(f"Assistant: {assistant_response}\n\n")

        db.execute(
            text("""
                UPDATE chats
                SET last_update = :last_update
                WHERE id = :id
            """),
            {
                "last_update": datetime.now(),
                "id": chat_id
            }
        )

        db.commit()

        return {
            "response": assistant_response
        }

    finally:
        db.close()