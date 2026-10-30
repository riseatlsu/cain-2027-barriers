import database
from nicegui import ui

def create():
    @ui.page('/website/{participant_id}/{request_id}/{interaction_id}/')
    async def website_page(participant_id: str, request_id: str, interaction_id: str, website_url: str):
        ui.page_title('Website')
        ui.query('body').style('background-color: #f2f2f2;')

        def close_website():
            database.close_interaction(participant_id, request_id, interaction_id)
            ui.open('/resources/' + participant_id + '/' + request_id)

        with ui.header().classes('place-content-center'):
            ui.html('Website')
        with ui.row().classes('w-full place-content-center'):
            with ui.row().classes('w-full place-content-center'):
                ui.open('https://rise.articulate.com/share/2sJK2Vk1hEknDryF2CeFEYl4Vtf7nFWt#/', new_tab=True)

            with ui.row().classes('w-2/12'):
                ui.button(text="Return to resources", color="gray", on_click=lambda: close_website()).style('color: white;').classes('full-width')