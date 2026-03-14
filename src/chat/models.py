from pydantic import BaseModel
from typing import List,Dict

class ChatRequest(BaseModel):
    query: str
    chat_history: List[Dict[str,str]]

class ChatResponse(BaseModel):
    chat_history: List[Dict[str,str]]
    response : str

