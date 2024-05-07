from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.config.mongo_connection import get_motor_client
from app.config.mongo_connection import get_db_instance
from app.services.OpenAi import OpenAIService
from app.services.EngineersQuery import EngineersQuery
from app.services.Amplifier import Amplifier
from app.utils.Validators import AuthTokenData
from typing import Optional
from app.services.oauth import get_current_user
import json

router = APIRouter()
openAi = OpenAIService()
engineersDb = EngineersQuery()
amplifier = Amplifier()

class CreateThreadPayload(BaseModel):
    message: str
    thread_id: Optional[str] = None
    queryMode: Optional[str]

def extract_dict_from_string(string):
    return json.loads(string.replace('\n', ''))

@router.post("/message")
async def send_message(payload: CreateThreadPayload, auth: AuthTokenData = Depends(get_current_user), db=Depends(get_db_instance)):
    try:
        response = await openAi.interact_bot(message=payload.message, threadId=payload.thread_id)
        if not payload.thread_id:
            threads_collection = db["threads"]
            existing_thread = await threads_collection.find_one({"userId": auth['id']})
            if existing_thread:
                await threads_collection.update_one(
                    {"_id": existing_thread["_id"]},
                    {"$push": {"threads": {"thread_id": response.get("thread_id"), "last_message": payload.message}}},
                )
            else:
                new_thread = {
                    "userId": auth['id'],
                    "threads": [{"thread_id": response.get("thread_id"), "last_message": payload.message}],
                }
                await threads_collection.insert_one(new_thread)
        engineers = []
        if response:
            amp_query = amplifier.amplify(payload.message, response.get("response", {}).get("keywords", []))
            engineers = engineersDb.get_engineers(amp_query, response.get("response", {}), mode="0")
        engineers_details = engineersDb.get_engineer_details(engineers)
        return {"botResponse": response, "engineers": engineers_details}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.get("/")
async def get_all_threads(auth: AuthTokenData = Depends(get_current_user), db=Depends(get_db_instance)):
    try:
        threads_collection = db["threads"]
        existing_thread = await threads_collection.find_one({"userId": auth['id']})
        return {"threads": existing_thread.get("threads", []) if existing_thread else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.get("/{threadId}")
async def get_thread_messages(threadId: str, db=Depends(get_db_instance)):
    try:
        response = openAi.get_thread_messages(threadId)
        messages = []
        for item in response.get("data", []):
            message = item.get('content', [{}])[0].get('text', {}).get('value', '')
            message_id = item.get('id')
            role = item.get('role')
            created_at = item.get('created_at')
            if role == "assistant":
                message = extract_dict_from_string(message).get("reply", "")
            messages.append({"reply": message, "role": role, "id": message_id, "createdAt": created_at})

        return {"botresponse": {"response": {"messages": messages}}, "thread_id": threadId}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")