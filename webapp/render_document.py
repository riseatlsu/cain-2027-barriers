import database
from nicegui import ui, app

def create():
    @ui.page('/document/{participant_id}/{request_id}/{interaction_id}/')
    async def document_page(participant_id: str, request_id: str, interaction_id: str, document_url: str):
        ui.page_title('Document')
        ui.query('body').style('background-color: #f2f2f2;')

        def close_document():
            database.close_interaction(participant_id, request_id, interaction_id)
            ui.open('/resources/' + participant_id + '/' + request_id)

        with ui.header().classes('place-content-center'):
            ui.html('Document')
        with ui.row().classes('w-full place-content-center'):
            with ui.row().classes('w-full place-content-center'):
                path = app.add_static_file(local_file=document_url)
                ui.html(f'<embed src="{path}" width="1280" height="720" type="application/pdf">')

            with ui.row().classes('w-2/12'):
                ui.button(text="Return to resources", color="gray", on_click=lambda: close_document()).style('color: white;').classes('full-width')