from fastapi import APIRouter, Depends
from src.chat.models import ChatRequest,ChatResponse
from src.chat.utils import format_history
from fastapi import Request
from src.auth.dependency import AccessTokenBearer

access_token_bearer = AccessTokenBearer()


chat_router = APIRouter()

@chat_router.get("/", response_model=ChatResponse)
async def get_response(request : Request,chat_request : ChatRequest,token_details : dict = Depends(access_token_bearer)) -> ChatResponse:

    chat_history = chat_request.chat_history
    query = chat_request.query
    formatted_history = format_history(chat_history)
    graph = request.app.state.graph

    try :
        response = graph.invoke(query=query,formatted_history=formatted_history,chat_history=chat_history)
    
    except Exception as e :
        response = f"Oops! Something went wrong while processing your request."

    chat_history.append({"role":"investisense","content":response})
    return ChatResponse(chat_history=chat_history,response=response)