import asyncio
from openai import OpenAI
from app.config.constants import SECRETS
import json

client = OpenAI(api_key=SECRETS.OPEN_API_KEY)

def extract_dict_from_string(string):
    """Extracts a dictionary from a string."""
    try:
        cleaned_string = string.replace('\n', '')
        extracted_dict = json.loads(cleaned_string)
        return extracted_dict
    except json.JSONDecodeError as e:
        # Log or handle JSON decoding error
        print(f"Error decoding JSON: {e}")
        return None

class OpenAIService:
    """Service class for interacting with OpenAI APIs."""

    def __init__(self):
        self._client = client

    async def append_to_thread(self, thread, message, role="user"):
        """Appends a message to a thread."""
        try:
            loop = asyncio.get_running_loop()
            thread_message = await loop.run_in_executor(None, self._append_to_thread, thread, message, role)
            return thread_message
        except Exception as e:
            # Log or handle error
            print(f"Error appending to thread: {e}")
            return None

    def _append_to_thread(self, thread, message, role="user"):
        """Synchronous method to append a message to a thread."""
        try:
            thread_message = self._client.beta.threads.messages.create(thread_id=thread, role=role, content=message)
            return thread_message
        except Exception as e:
            # Log or handle error
            print(f"Error appending to thread (sync): {e}")
            return None

    async def run_thread(self, thread, assistant):
        """Runs a thread."""
        try:
            loop = asyncio.get_running_loop()
            run = await loop.run_in_executor(None, self._run_thread, thread, assistant)
            if run is not None and run.status == "completed":
                messages = self._client.beta.threads.messages.list(thread_id=thread)
                return messages
        except Exception as e:
            # Log or handle error
            print(f"Error running thread: {e}")
        return None

    def _run_thread(self, thread, assistant):
        """Synchronous method to run a thread."""
        try:
            run = self._client.beta.threads.runs.create_and_poll(thread_id=thread, assistant_id=assistant)
            return run
        except Exception as e:
            # Log or handle error
            print(f"Error running thread (sync): {e}")
            return None

    async def interact_bot(self, message: str, threadId: str = None):
        """Interacts with the OpenAI bot."""
        try:
            my_assistant = self._client.beta.assistants.retrieve("asst_gr55Ttqa0X6WaSOWlTJAItdg")
            thread_id = threadId if threadId else self._client.beta.threads.create().id
            thread_message = await self.append_to_thread(thread_id, message)
            if not thread_message:
                return {"response": {"error": "Failed to append message to the thread"}, "thread_id": thread_id}
            messages = await self.run_thread(thread_id, my_assistant.id)
            if messages:
                messages_dict = messages.to_dict()
                response = messages_dict['data'][0]['content'][0]['text']['value']
                response = extract_dict_from_string(response)
                if response:
                    response["id"] = messages_dict['data'][0]['id']
                    response["createdAt"] = messages_dict['data'][0]['created_at']
                else:
                    return {"response": {"error": "Failed to parse response from OpenAI"}, "thread_id": thread_id}
                return {"response": response, "thread_id": thread_id}
            else:
                return {"response": {"error": "No response from the thread"}, "thread_id": thread_id}
        except Exception as e:
            # Log or handle error
            print(f"Error interacting with bot: {e}")
            return {"response": {"error": "An unexpected error occurred"}, "thread_id": None}

    def get_thread_messages(self, threadId: str):
        try:
            messages = self._client.beta.threads.messages.list(thread_id=threadId)
            return messages.to_dict()
        except Exception as e:
            # Log or handle error
            print(f"Error getting thread messages: {e}")
            return {"error": f"Failed to retrieve messages for thread {threadId}"}