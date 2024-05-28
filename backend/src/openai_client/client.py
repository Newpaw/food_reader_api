from openai import OpenAI
from ..config import settings
from ..response_processor import ResponseProcessor
from fastapi import HTTPException
from ..logger import setup_logger

logger = setup_logger(__name__)


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

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

    def process_image(self, file_path):
        try:
            thread = self.create_thread()
            logger.debug(f"Created thread with thread_id: {thread.id}")

            file_id = self.upload_file(file_path)
            logger.debug(f"Uploaded file with file_id: {file_id}")

            self.create_message(thread.id, file_id)

            run = self.create_and_poll_run(thread.id, settings.ASSISTANT_ID)
            logger.debug(f"Created and polled run with run_id: {run.id}")

            if run.status == "completed":
                messages = self.list_messages(thread.id)
                content = messages.data[0].content[0].text.value
                logger.debug(f"Content: {content}")

                # Process the response
                food_info = ResponseProcessor.process_response(content)
                return food_info
            else:
                logger.error("Processing failed")
                raise HTTPException(
                    status_code=500, detail="Processing failed with no additional info"
                )
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
