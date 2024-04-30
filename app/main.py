from fastapi import FastAPI
from starlette.responses import RedirectResponse  # Correct import
from fastapi.middleware.cors import CORSMiddleware
from app.config.AppConfig import config
from app.services.OpenAi import OpenAIService
from app.services.EngineersQuery import EngineersQuery
from app.services.Amplifier import Amplifier


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
    # print(response)
    return response



@app.get("/message")
async def sendMessage(message: str = "", thread_id: str = None):
    openAi =  OpenAIService()
    print("CHECK 1",message, thread_id)
    response = openAi.interact_bot(message=message, threadId=thread_id)
    print("CHECK 2", response)
    engineers = []
    engineersDb = EngineersQuery()
    if response:
        amplifier = Amplifier()
        ampQuery = amplifier.amplify(message, response["response"]["keywords"])
        print("Amplified Query: ", ampQuery)
        engineers = engineersDb.get_engineers(ampQuery, response["response"], mode="0")

    engineersDetails = engineersDb.get_engineer_details(engineers)
    return {"botResponse":response, "engineers": engineersDetails}


#enables automated documentation
@app.get("/redoc")
async def get_redoc():
    return RedirectResponse(url="/redoc")

