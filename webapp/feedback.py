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
    @ui.page('/feedback/{participant_id}/{request_id}')
    async def feedback_page(participant_id: str, request_id: str):
        def close_request():
            feedback = None
            
            if rate_request_satisfaction.value and most_useful_category.value and was_category_correct.value:
                if was_category_correct.value == 'No':
                    if form_category.value:
                        if form_category.value == 'Other':
                            if custom_category.value:
                                feedback = {'rate_satisfaction': rate_request_satisfaction.value, 'most_useful_category': most_useful_category.value, 'was_category_correct': was_category_correct.value, 'category': custom_category.value}
                        else:
                            feedback = {'rate_satisfaction': rate_request_satisfaction.value, 'most_useful_category': most_useful_category.value, 'was_category_correct': was_category_correct.value, 'category': form_category.value}
                else:
                    feedback = {'rate_satisfaction': rate_request_satisfaction.value, 'most_useful_category': most_useful_category.value, 'was_category_correct': was_category_correct.value}

            if feedback:
                database.close_request(participant_id, request_id, feedback)
                ui.open('/assistance/' + participant_id)
            else:
                ui.notify('Before proceeding, answer the questions in the feedback form.')


        ui.page_title('Survey')
        ui.query('body').style('background-color: #f2f2f2;')

        with ui.header().classes('place-content-center'):
            ui.html('Survey')

        with ui.row().classes('w-full place-content-center'):
            with ui.row().classes('w-6/12 p-12'):
                with ui.row().classes('w-full').style('font-size: 36px; font-weight: bold;'):
                    ui.html('Questions')

                with ui.row().classes('w-full'):
                    ui.html('Rate your satisfaction with the assistance given for this request:')

                with ui.row().classes('w-full'):
                    rate_request_satisfaction = ui.radio(['Very Dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very Satisfied'])

                with ui.row().classes('w-full'):
                    ui.html('What category of information was the most useful for this request?')

                with ui.row().classes('w-full'):
                    most_useful_category = ui.radio(['Chat', 'Read', 'Watch', 'None'])

                with ui.row().classes('w-full'):
                    ui.html('In this request, you described that: <i>" I don’t know what I want the robot to do…"</i>.<br>Was this statement correct? If not, we will ask you to assign another description.')

                with ui.row().classes('w-full'):
                    was_category_correct = ui.radio(['Yes', 'No'])

                with ui.row().classes('w-full').bind_visibility_from(was_category_correct, 'value', value='No'):
                    ui.html("Please pick one of the categories below:").classes('w-full')
                    form_category = ui.radio(form_categories)

                with ui.row().classes('w-full').bind_visibility_from(form_category, 'value', value='Other'):
                    custom_category = ui.input(label="Request title")

                with ui.row().classes('w-full place-content-center'):
                    with ui.row().classes('w-2/12'):
                        ui.button(text="Close request", color="red", on_click=lambda: close_request()).style('color: white;').classes('full-width')

                    with ui.row().classes('w-2/12'):
                        ui.button(text="Return to request", color="gray", on_click=lambda: ui.open('/resources/' + participant_id + '/' + request_id)).style('color: white;').classes('full-width')
