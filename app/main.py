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


#enables automated documentation
@app.get("/redoc")
async def get_redoc():
    return RedirectResponse(url="/redoc")

