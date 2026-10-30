import database
import asyncio
import concurrent.futures
import custom_chatgpt
from nicegui import run, ui
from datetime import datetime

def create():
    rag_generator = custom_chatgpt.load_chatgpt_settings()
    executor = concurrent.futures.ThreadPoolExecutor()

    @ui.page('/chat/{participant_id}/{request_id}/{interaction_id}/')
    async def chat_page(participant_id: str, request_id: str, interaction_id: str):
        interaction_data = database.read_interaction(participant_id, request_id, interaction_id)
        request_data = database.read_request(participant_id, request_id)

        ui.page_title(request_data['description'])
        ui.timer(1.0, lambda: chat_message_area.refresh())

        def close_chat():
            database.close_interaction(participant_id, request_id, interaction_id)
            ui.open('/resources/' + participant_id + '/' + request_id)

        def record_participant_message(question: str):
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            interaction_data['content']['messages'].append({'user_type': 'participant', 'text': question, 'timestamp': timestamp})
            database.update_interaction(**interaction_data)
            chat_message_area.refresh()

        def request_chatgpt_response(question: str) -> str:
            return rag_generator.generate_response(question)

        async def record_chatgpt_message(question: str):
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(executor, lambda: request_chatgpt_response(question))
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            interaction_data['content']['messages'].append({'user_type': 'bot', 'text': response, 'timestamp': timestamp})
            database.update_interaction(**interaction_data)
            chat_message_area.refresh()

        @ui.refreshable
        def chat_message_area():
            messages_section = ui.row().classes('w-full p-10').style('background-color: #f2f2f2; border-radius: 16px;')

            with messages_section:
                ui.chat_message(name='Request System', text='Please wait a moment while the expert review your request...<br><br><b>Request category:</b> ' + request_data['category'] + '<br><b>Request description:</b> ' + request_data['description'], sent=False, text_html=True).classes('w-full')

                interaction_data = database.read_interaction(participant_id, request_id, interaction_id)

                if interaction_data['content']['messages']:
                    for message in interaction_data['content']['messages']:
                        message_on_left = True if message['user_type'] == 'participant' else False
                        ui.chat_message(name=message['user_type'].capitalize(), text=message['text'], stamp=message['timestamp'], sent=message_on_left).classes('w-full')

        def chat_input_area():
            with ui.row().classes('w-full'):
                chat_field = ui.textarea(label='Write a message...').props('rounded outlined clearable').classes(' w-full')

            with ui.row().classes('w-full place-content-center p-5'):
                with ui.row().classes('w-2/12'):
                    send_button = ui.button(text="Send message", color="blue", on_click=lambda: record_participant_message(chat_field.value)).classes('full-width')
                    send_button.on('click', lambda: record_chatgpt_message(chat_field.value))
                    send_button.on('click', lambda: chat_field.set_value(''))

                with ui.row().classes('w-2/12'):
                    ui.button(text="Return to resources", color="gray", on_click=lambda: close_chat()).style('color: white;').classes('full-width')

        with ui.header().classes('place-content-center'):
            ui.html('Chat').style('font-size: 36px; font-weight: 400; color: white;')

        ui.html("Warning: You are connected with Isaac, an expert hired to assist you with the Wizard Easy Programming Tool. He will reply to your messages in seconds.\
                If he does not reply after a few seconds, ask a proctor for clarification.")
        chat_message_area()
        chat_input_area()
        await record_chatgpt_message('First, introduce yourself. Second, help me with the request:' + request_data['description'])
