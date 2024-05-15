from .openai_client import OpenAIClient
from .response_processor import ResponseProcessor
from .config import settings

def main():
    assistant_id = settings.ASSISTANT_ID
    client = OpenAIClient()

    thread = client.create_thread()
    file_id = client.upload_file("docs/hranolky.jpg")
    client.create_message(thread.id, file_id)

    run = client.create_and_poll_run(thread.id, assistant_id)

    if run.status == 'completed': 
        messages = client.list_messages(thread.id)
        content = messages.data[0].content[0].text.value
        
        food_info = ResponseProcessor.process_response(content)
        print(food_info)
    else:
        print(run.status)

if __name__ == "__main__":
    main()
