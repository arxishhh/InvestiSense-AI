from fastapi import FastAPI
from src.exceptions import register_all_errors
from src.auth.routes import auth_router
from src.chat.routes import chat_router
import logging
from src.agents.graph_executor import graph

version = "v3"

investisense_app = FastAPI(
    title="InvestiSense AI",
    description="Financial chatbot powered by LLMs and RAG",
    version=version
)

@investisense_app.on_event("startup")
async def startup():
    logging.info("Starting InvestiSense AI backend...")
    investisense_app.state.graph = graph
    logging.info("Graph Initialized and stored in app state")

register_all_errors(investisense_app)

investisense_app.include_router(auth_router, f"/api/{version}/auths",tags=['auth'])
investisense_app.include_router(chat_router, f"/api/{version}/chat",tags=['chat'])


