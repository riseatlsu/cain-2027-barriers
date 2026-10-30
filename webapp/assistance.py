import database
from nicegui import ui

form_categories = ["I don’t know what I want the robot to do…",\
              "I think I know what I want the robot to do, but I don’t know what to use…",\
              "I think I know what things to use, but I don't know how to make them work together…",\
              "I think I know what to use, but I don't know how to use it…",\
              "I thought I knew how to use this, but it didn’t do what I expected…",\
              "I think I know why it didn’t do what I expected, but I don’t know how to check…",\
              "Other"]

def create():
    @ui.page('/assistance/{participant_id}')
    async def assistance_page(participant_id: str):
        ui.page_title('Assistance')
        ui.query('body').style('background-color: #f2f2f2;')

        def request_assistance(description, category, custom_category):
            if description and category:
                if category == 'Other':
                    request_id = database.create_request(participant_id, description, custom_category)
                else:
                    request_id = database.create_request(participant_id, description, category)
                ui.open('/resources/' + participant_id + '/' + request_id)
            else:
                ui.notify('Before proceeding, select the type of assistance you need and describe your request in detail.')

        with ui.header().classes('place-content-center'):
            ui.html('Assistance')

        with ui.row().classes('w-full place-content-center'):
            with ui.row().classes('w-6/12 p-12'):
                with ui.row().classes('w-full').style('font-size: 36px; font-weight: bold;'):
                    ui.html('Request Form')

                with ui.row().classes('w-full'):
                    ui.html('Use the form below to define what type of assistance you are looking for:')

                with ui.row().classes('w-full'):
                    form_category = ui.radio(form_categories)
                    
                    with ui.row().classes('w-full').bind_visibility_from(form_category, 'value', value='Other'):
                        custom_category = ui.input(label="Request title")

                    with ui.row().classes('w-full'):
                        form_description = ui.textarea(label='Describe your request in detail').props('rounded outlined clearable').classes('w-full')
                    with ui.row().classes('w-full place-content-center'):
                        ui.button(text="Request Assistance", color="blue", on_click=lambda: request_assistance(form_description.value, form_category.value, custom_category.value)).style('font-size: 16px;')