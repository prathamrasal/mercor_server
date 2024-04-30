from openai import OpenAI
from app.config.constants import SECRETS
import json

client = OpenAI(api_key=SECRETS.OPEN_API_KEY)

def extract_dict_from_string(string):
    # Remove newline characters and whitespace
    cleaned_string = string.replace('\n', '')
    
    # Parse the string into a dictionary
    extracted_dict = json.loads(cleaned_string)
    
    return extracted_dict

def append_to_thread(thread, message, role = "user"):
    thread_message = client.beta.threads.messages.create(thread_id=thread, role=role, content=message)
    return thread_message

def run_thread(thread, assistant):
    run = client.beta.threads.runs.create_and_poll(thread_id=thread, assistant_id=assistant)
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread)
    return messages


class OpenAIService:
    def __init__(self):
        pass

    def interact_bot(self, message: str, threadId:str = None):
        my_assistant = client.beta.assistants.retrieve("asst_gr55Ttqa0X6WaSOWlTJAItdg")
        # print('Assistant: ', my_assistant)
        thread_id = ""
        if threadId is None or threadId=="":
            thread_id = client.beta.threads.create().id
        else:
            thread_id = threadId
        # print('ThreadId: ', thread_id)
        thread_message = append_to_thread(thread_id, message)
        # print('Message: ', thread_message)
        messages = run_thread(thread_id, my_assistant.id)
        # print(messages.to_dict())
        messages_dict = messages.to_dict()
        response = messages_dict['data'][0]['content'][0]['text']['value']
        response = extract_dict_from_string(response)
        return {
            "response": response,
            "thread_id": thread_id
        }
    
    def get_thread_messages(self, threadId:str):
        messages = client.beta.threads.messages.list(thread_id=threadId)
        return messages.to_dict()

    def get_user_messages(self, threadId:str):
        messages = client.beta.threads.messages.list(thread_id=threadId, role="user")
        return messages.to_dict()