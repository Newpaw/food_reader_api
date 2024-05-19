from openai import OpenAI
from ..config import settings 

class OpenAIClient:
    def __init__(self):
        openai_api_key = settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=openai_api_key)

    def create_thread(self):
        return self.client.beta.threads.create()

    def create_message(self, thread_id, file_id):
        return self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=[
                {"type": "text", "text": "Get me the info."},
                {"type": "image_file", "image_file": {"file_id": file_id, "detail": "high"}}
            ]
        )

    def create_and_poll_run(self, thread_id, assistant_id):
        return self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

    def list_messages(self, thread_id):
        return self.client.beta.threads.messages.list(thread_id=thread_id)

    def upload_file(self, file_path):
        with open(file_path, "rb") as file:
            response = self.client.files.create(
                file=file,
                purpose="vision"
            )
            return response.id
