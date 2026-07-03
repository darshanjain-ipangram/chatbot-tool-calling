from fastapi import FastAPI
from pydantic import BaseModel
from app.services.chatbot import chat_with_bot

app = FastAPI(title="Chatbot")

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    response_text = chat_with_bot(request.session_id, request.message)
    return ChatResponse(response=response_text)
