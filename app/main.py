from fastapi import FastAPI
from starlette.responses import RedirectResponse  # Correct import
from fastapi.middleware.cors import CORSMiddleware
from app.config.AppConfig import config
from app.services.OpenAi import OpenAIService

app = FastAPI(title=config.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_root():
    return {"Health": "OK"}

@app.get("/test")
async def checkOpenAI(message: str = "", thread_id: str = None):
    openAi =  OpenAIService()
    print(message, thread_id)
    response = openAi.interact_bot(message=message, threadId=thread_id)
    print(response)
    return response

#enables automated documentation
@app.get("/redoc")
async def get_redoc():
    return RedirectResponse(url="/redoc")

