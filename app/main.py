from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config.AppConfig import config
from .routers import auth, threads
from app.services.OpenAi import OpenAIService

app = FastAPI(title=config.app_name)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/v1/api/auth")
app.include_router(threads.router, prefix="/v1/api/threads")

# Health check endpoint
@app.get("/")
async def get_root():
    return {"Health": "OK"}

# Test endpoint for interacting with OpenAI
@app.get("/test")
async def check_openai(message: str = "", thread_id: str = None, openai_service: OpenAIService = Depends()):
    print(message, thread_id)
    response = openai_service.interact_bot(message=message, threadId=thread_id)
    return response

# Endpoint for API documentation using ReDoc
@app.get("/redoc")
async def get_redoc():
    return RedirectResponse(url="/redoc")