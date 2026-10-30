import chat
import database
import feedback
import resources
import assistance
import render_video
import render_document
import render_website
from nicegui import ui

ui.header.default_style('background-color: #080808; color: white; font-size: 36px; font-weight: 400;')
ui.row.default_style('font-size: 20px; font-weight: 400;')
ui.button.default_style('color: white;')

@ui.page('/')
async def main():
    ui.page_title('Experiment')
    ui.query('body').style('background-color: #f2f2f2;')

    def start_experiment(proctor_password):
        if str(proctor_password).lower() == 'selab':
            participant_id = database.create_experiment()
            ui.open('/assistance/' + participant_id, new_tab=True)
            start_experiment_area.refresh()
        else:
            ui.notify('To start a new experiment, insert your password above.')
            ui.notify('If you need help, send a message to Felipe at (804) 298-0694 or on Discord at @fronchetti.')

    def resume_experiment(proctor_password, participant_id):
        if str(proctor_password).lower() == 'selab':
            ui.open('/assistance/' + participant_id, new_tab=True)
        else:
            ui.notify('To resume the experiment, insert your password above.')
            ui.notify('If you need help, send a message to Felipe at (804) 298-0694 or on Discord at @fronchetti.')

    def close_experiment(proctor_password, participant_id):
        if str(proctor_password).lower() == 'selab':
            database.close_experiment(participant_id=participant_id)
            start_experiment_area.refresh()
        else:
            ui.notify('To end the experiment, insert your password above.')
            ui.notify('If you need help, send a message to Felipe at (804) 298-0694 or on Discord at @fronchetti.')

    @ui.refreshable
    def start_experiment_area():
        experiment_data = database.read_last_experiment()    

        with ui.row().classes('w-full place-content-center'):
            if experiment_data and experiment_data['closed_at'] is None:
                with ui.row().classes('w-full place-content-center'):
                    with ui.row().classes('w-6/12 p-12'):
                        ui.html('Status').classes('w-full').style('font-size: 36px; font-weight: bold;')
                        ui.html('There is an experiment in progress. The proctor must resume or end the current experiment.').classes('w-full')
                        ui.html('<b>Participant number:</b> ' + experiment_data['participant_id']).classes('w-full')

                        ui.html('Post Checklist').classes('w-full').style('font-size: 36px; font-weight: bold;')
                        ui.html('After the experiment, the proctor must follow the steps below:').classes('w-full')
                        ui.checkbox('Save the program made by the participant on the FlexPendant (Files > Save As). The filename must be the participant number defined above.')
                        ui.checkbox('Open the survey and answer the proctor-related questions.').classes('w-full')
                        ui.checkbox('Once the proctor-related questions are completed, invite the participant to answer the survey.').classes('w-full')
                        ui.checkbox('Once the participant completes the survey, finish the experiment by clicking the "end experiment" button below.').classes('w-full')

                        ui.html('<b><a href="https://forms.gle/ZJLo9rMYEC6fqj7W8", style="color: red" target="_blank">Click here to open the survey</a></b>')

                        with ui.row().classes('w-full place-content-center'):
                            with ui.row().classes('w-2/12'):
                                password_field = ui.input(label='Proctor Password', password=True)

                        with ui.row().classes('w-full place-content-center'):
                            with ui.row().classes('w-2/12'):
                                ui.button(text="Resume experiment", color="gray", on_click=lambda: resume_experiment(password_field.value, experiment_data['participant_id'])).classes('full-width')

                            with ui.row().classes('w-2/12'):
                                ui.button(text="End experiment", color="red", on_click=lambda: close_experiment(password_field.value, experiment_data['participant_id'])).classes('full-width')
            else:
                with ui.row().classes('w-full place-content-center'):
                    with ui.row().classes('w-6/12 p-12'):
                        ui.html('Status').classes('w-full').style('font-size: 36px; font-weight: bold;')
                        ui.html('There is no experiment running at the moment, and a proctor can start a new one.').classes('w-full')

                        ui.html('Preliminary Checklist').classes('w-full').style('font-size: 36px; font-weight: bold;')
                        ui.html('Before proceeding with the experiment, the proctor must cover the steps below with the participant:').classes('w-full')
                        ui.checkbox('Open the starting program in the Wizard Easy Programming Tool on the FlexPendant.').classes('w-full')
                        ui.checkbox('Log in the desktop computer with your VCU credentials and open this website on the participants page. Make sure the desktop application is always available for the participant to use.').classes('w-full')
                        ui.checkbox('Confirm if the robot is in auto mode, with motors on and with speed at 15%.').classes('w-full')
                        ui.checkbox('Confirm if the coffee cans are randomly organized between the two dispensers.').classes('w-full')
                        ui.checkbox('Bring and introduce participant to the experiment area.').classes('w-full')
                        ui.checkbox('Read the experiment guidelines out loud to the participant.').classes('w-full')
                        ui.checkbox('Provide a printed copy of the experiment guidelines and the workspace map to the participant.').classes('w-full')
                        ui.checkbox('Start the experiment.').classes('w-full')
                        ui.html('<p style="color:red">Never give the participant hints about the solution of the experiment. You should only clarify questions about the information available in the experiment guidelines.</p>')
                        ui.html('<p style="color:red">You should only help the participant with the robot if the robot is not working for a reason not related to the programming language (e.g., mechanical failure, operating system failure).</p>')

                        with ui.row().classes('w-full place-content-center'):
                            with ui.row().classes('w-2/12'):
                                password_field = ui.input(label='Proctor Password', password=True)

                        with ui.row().classes('w-full place-content-center'):
                            with ui.row().classes('w-2/12'):
                                ui.button(text="Start experiment", color="green", on_click=lambda: start_experiment(password_field.value)).classes('full-width')

    with ui.header().classes('place-content-center'):
        ui.html('Experiment')

    start_experiment_area()

# Main pages
assistance.create()
resources.create()
# Resources
chat.create()
render_video.create()
render_document.create()
render_website.create()
# Survey
feedback.create()

ui.run(favicon="🐔", binding_refresh_interval =1, port=80)
