from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from backend.utils.replier import answer
from typing import List,Dict,Any
from pathlib import Path

class ChatRequest(BaseModel):
    query: str = Field(...,description="User's Query")
    role: str = Field(...,description="Role of the Assistant")
    chat_history: List[Dict[str,Any]] = Field(...,description="Chat history of the Assistant")

class ChatResponse(BaseModel):
    response: str

app = FastAPI(
    title="InvestiSense AI",
    description="Financial chatbot powered by LLMs and RAG",
    version="1.0.0"
)
@app.on_event("startup")
async def startup():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    db_path = BASE_DIR / 'database' / 'numeric_db' / 'analyst_data.db'
    print("This file path:", Path(__file__).resolve())
    print("BASE_DIR:", BASE_DIR)
    print("Expected DB path:", db_path)
    print("Exists?", db_path.exists())
@app.get("/")
async def root():
    return {"message": "InvestiSense AI backend is running"}

@app.post("/chat",response_model=ChatResponse)
async def get_response(chat_request : ChatRequest):
    try:
        result = await answer(chat_request.query,chat_request.role,chat_request.chat_history)
        return ChatResponse(response = result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))