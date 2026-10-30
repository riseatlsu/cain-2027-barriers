import database
from nicegui import ui

def create():
    @ui.page('/resources/{participant_id}/{request_id}')
    async def resources(participant_id: str, request_id: str):
        ui.page_title('Resources')
        ui.query('body').style('background-color: #f2f2f2;')

        def close_assistance():
            ui.open('/feedback/' + participant_id + '/' + request_id)

        def register_interaction(type, content):
            if type == 'text':
                interaction_id = database.create_interaction(participant_id, request_id, type, content)
                ui.open('/document/' + participant_id + '/' + request_id + '/' + interaction_id + '?document_url=' + content['url'])
            elif type == 'video':
                interaction_id = database.create_interaction(participant_id, request_id, type, content)
                ui.open('/video/' + participant_id + '/' + request_id + '/' + interaction_id + '?video_url=' + content['url'])
            elif type == 'chat':
                interaction_id = database.create_interaction(participant_id, request_id, type, content)
                ui.open('/chat/' + participant_id + '/' + request_id + '/' + interaction_id)
            elif type =='website':
                interaction_id = database.create_interaction(participant_id, request_id, type, content)
                ui.open(content['url'])

        with ui.header().classes('place-content-center'):
            ui.html('Resources')

        with ui.row().classes('w-full place-content-center'):
            with ui.row().classes('w-6/12 p-5').style('background-color: #e8e8e8; border-radius: 16px;'):
                with ui.row().classes('w-full place-content-center'):
                    with ui.row().classes('w-5/12'):
                        with ui.row().classes('w-full p-2 rounded items-center place-content-center').style('background-color: #dbdbdb;').on('click', lambda: register_interaction('text', {'title': 'Experiment Guidelines', 'url': '/root/robot/webapp/files/experiment_guidelines.pdf'})):
                            ui.markdown('Experiment Guidelines')

                    with ui.row().classes('w-5/12'):
                        with ui.row().classes('w-full p-2 rounded items-center place-content-center').style('background-color: #dbdbdb;').on('click', lambda: register_interaction('text', {'title': 'Workspace Map', 'url': '/root/robot/webapp/files/workspace_map.pdf'})):
                            ui.markdown('Workspace Map')

                with ui.row().classes('w-full place-content-center'):
                    ui.html('Use the resources below to complete your request. Once you are done with your request, hit the close request button below:')
                with ui.row().classes('w-full place-content-center'):
                    ui.button('Close request', on_click=lambda: close_assistance(), color='red').style('font-size: 16px;')

        with ui.row().classes('w-full place-content-center'):
            # Read
            with ui.row().classes('w-3/12 p-5').style('background-color: #e8e8e8; border-radius: 16px;'):
                with ui.row().classes('w-full').style('font-size: 36px; font-weight: bold;'):
                    ui.html('Read')

                ui.html('On the teaching pendant, click on the Help (?) button and select the Manual option to access the documentation:')
                ui.image('/root/robot/webapp/files/pendant.jpg').classes('rounded')
                ui.html('Or refer to the documents below:')

                with ui.row().classes('w-full p-2 rounded items-center place-content-center').style('background-color: #dbdbdb;').on('click', lambda: register_interaction('text', {'title': 'Application Manual of the Wizard Easy Programming Tool', 'url': '/root/robot/webapp/files/wizard_manual.pdf'})):
                    ui.markdown('Application Manual of the Wizard Easy Programming Tool')

                with ui.row().classes('w-full p-2 rounded items-center place-content-center').style('background-color: #dbdbdb;').on('click', lambda: register_interaction('text', {'title': 'Quickstart Guide for the Wizard Easy Programming Tool', 'url': '/root/robot/webapp/files/wizard_easy_programming_quickstart_guide.pdf'})):
                    ui.markdown('Quickstart Guide for the Wizard Easy Programming Tool')

            # Watch
            with ui.row().classes('w-3/12 p-5').style('background-color: #e8e8e8; border-radius: 16px;'):
                with ui.row().classes('w-full').style('font-size: 36px; font-weight: bold;'):
                    ui.html('Watch')

                ui.html('Click in one of the videos below to start watching:')

                with ui.scroll_area().style('min-height: 640px;'):
                    with ui.row().classes('w-full p-2 rounded items-center').style('background-color: #dbdbdb;').on('click', lambda: register_interaction('video', {'title': 'Wizard Easy Programming – For everyone and all new robots', 'url': 'Kmv5jUI3WF0?si=PfrOJy_FwGxIjnm4'})):
                        with ui.row().classes('w-5/12'):
                            ui.image('https://img.youtube.com/vi/Kmv5jUI3WF0/0.jpg').classes('w-64 h-32 rounded')
                        with ui.row().classes('w-6/12'):
                            ui.html('Wizard Easy Programming – For everyone and all new robots')

                    with ui.row().classes('w-full p-2 rounded items-center').style('background-color: #dbdbdb;').on('click', lambda: register_interaction('video', {'title': 'Quickstart Guide: Wizard Easy Programming', 'url': '2y1DmG-57JA?si=jl2-mcvFi36F9aO0'})):
                        with ui.row().classes('w-5/12'):
                            ui.image('https://img.youtube.com/vi/2y1DmG-57JA/0.jpg').classes('w-64 h-32 rounded')
                        with ui.row().classes('w-6/12'):
                            ui.html('Quickstart Guide: Wizard Easy Programming')

                    with ui.row().classes('w-full p-2 rounded items-center').style('background-color: #dbdbdb;').on('click', lambda: register_interaction('video', {'title': 'How to program collaborative robot GoFa with Wizard Easy Programming - Tutorial for beginners', 'url': 'zPnEOQX4jUA?si=PfrOJy_FwGxIjnm4'})):
                        with ui.row().classes('w-5/12'):
                            ui.image('https://img.youtube.com/vi/zPnEOQX4jUA/0.jpg').classes('w-64 h-32 rounded')
                        with ui.row().classes('w-6/12'):
                            ui.markdown('How to program collaborative robot GoFa with Wizard Easy Programming - Tutorial for beginners')

                    with ui.row().classes('w-full p-2 rounded items-center').style('background-color: #dbdbdb;').on('click', lambda: register_interaction('video', {'title': 'Step-by-step guide on pick and place application with Wizard Easy Programming tool', 'url': 'eUgqXsWMmwI?si=HcWE9LMjM'})):
                        with ui.row().classes('w-5/12'):
                            ui.image('https://img.youtube.com/vi/eUgqXsWMmwI/0.jpg').classes('w-64 h-32 rounded')
                        with ui.row().classes('w-6/12'):
                            ui.markdown('Step-by-step guide on pick and place application with Wizard Easy Programming tool')

                    with ui.row().classes('w-full p-2 rounded items-center').style('background-color: #dbdbdb;').on('click', lambda: register_interaction('video', {'title': 'Wizard Easy Programming – Advanced Application Overview', 'url': 'CVfQJoM8KsY?si=-VV6kv1weIZ3USNJ'})):
                        with ui.row().classes('w-5/12'):
                            ui.image('https://img.youtube.com/vi/CVfQJoM8KsY/0.jpg').classes('w-64 h-32 rounded')
                        with ui.row().classes('w-6/12'):
                            ui.markdown('Wizard Easy Programming – Advanced Application Overview')

                    with ui.row().classes('w-full p-2 rounded items-center').style('background-color: #dbdbdb;').on('click', lambda: register_interaction('video', {'title': 'Webinar | ABB Wizard easy programming for single arm YuMi', 'url': 'OKlcUcLMHQM?si=yFjYTOL1DkZdBHBq'})):
                        with ui.row().classes('w-5/12'):
                            ui.image('https://img.youtube.com/vi/OKlcUcLMHQM/3.jpg').classes('w-64 h-32 rounded')
                        with ui.row().classes('w-6/12'):
                            ui.markdown('Webinar | ABB Wizard easy programming for single arm YuMi')

                    with ui.row().classes('w-full p-2 rounded items-center').style('background-color: #dbdbdb;').on('click', lambda: register_interaction('video', {'title': 'Using Wizard to create a PCB assembly application in minutes', 'url': 'nj0X8fLj1SE?si=zy6EUfKFbhIJOa_6'})):
                        with ui.row().classes('w-5/12'):
                            ui.image('https://img.youtube.com/vi/nj0X8fLj1SE/2.jpg').classes('w-64 h-32 rounded')
                        with ui.row().classes('w-6/12'):
                            ui.markdown('Using Wizard to create a PCB assembly application in minutes')

            # Chat
            with ui.row().classes('w-3/12 p-5').style('background-color: #e8e8e8; border-radius: 16px;'):
                with ui.row().classes('w-full').style('font-size: 36px; font-weight: bold;'):
                    ui.html('Chat')

                with ui.row().classes('w-full'):
                    ui.chat_message("Hi, my name is Isaac! I am here to help you.")
                    ui.html('Start a conversation with the expert by clicking the button below:')

                with ui.row().classes('w-full'):
                    ui.button('Start conversation', on_click=lambda: register_interaction('chat', {'messages': []}), color='gray').classes('full-width').style('font-size: 16px; color: white;')
