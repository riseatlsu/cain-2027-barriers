import os
import json
import pandas

interaction_folder = "C:\\Users\\conso\\OneDrive\\Documents\\GitHub\\robot-barriers\\data\\interactions"
subfolders = [folder.path for folder in os.scandir(interaction_folder) if folder.is_dir()]

experiment_df = pandas.DataFrame(columns=["participant_id", "created_at", "closed_at", "requests_count", "total_interactions"])
request_df = pandas.DataFrame(columns=["request_id", "participant_id", "created_at", "closed_at", "description", "category", "video_count", "chat_count", "text_count", "total_request_interactions", "rate_satisfaction", "most_useful_category", "was_category_correct"])
# Fieldnames: interaction_id, request_id, participant_id, type, created_at, closed_at, content (if text or video, use "title" field, if chat use "messages" field), messages_count (for chat)
interaction_df = pandas.DataFrame(columns=["interaction_id", "request_id", "participant_id", "created_at", "closed_at", "request_category", "request_description", "type", "content", "bot_messages_count", "participant_messages_count"])
participant_messages = pandas.DataFrame(columns=["messages", "participant_id"])
bot_messages = pandas.DataFrame(columns=["messages", "participant_id"])

for subfolder in subfolders:
    total_interactions = 0
    about_file_path = os.path.join(subfolder, 'about_experiment.json')
    about_file_content = json.load(open(about_file_path, 'r'))
    requests_subfolder = os.path.join(subfolder, 'requests')

    if os.path.isdir(requests_subfolder):
        requests_folder_paths = [folder.path for folder in os.scandir(requests_subfolder) if folder.is_dir()]    
        about_file_content['requests_count'] = len(requests_folder_paths)

        for request_folder_path in requests_folder_paths:
            about_request_path = os.path.join(request_folder_path, 'about_request.json')
            about_request_content = json.load(open(about_request_path, 'r'))
            video_count = 0
            text_count = 0
            chat_count = 0

            if 'feedback' in about_request_content.keys():
                if about_request_content['feedback'] is not None:
                    about_request_content['rate_satisfaction'] = about_request_content['feedback'][0]['rate_satisfaction']
                    about_request_content['most_useful_category'] = about_request_content['feedback'][0]['most_useful_category']
                    about_request_content['was_category_correct'] = about_request_content['feedback'][0]['was_category_correct']
                else:
                    about_request_content['rate_satisfaction'] = ''
                    about_request_content['most_useful_category'] = ''
                    about_request_content['was_category_correct'] = ''

            interactions_subfolder = os.path.join(request_folder_path, 'interactions')

            if os.path.isdir(interactions_subfolder):
                interactions_filepaths = [interaction.path for interaction in os.scandir(interactions_subfolder) if interaction.is_file()]

                for interaction_filepath in interactions_filepaths:
                    interaction_content = json.load(open(interaction_filepath, 'r'))
                    interaction_content['request_description'] = about_request_content['description']
                    interaction_content['request_category'] = about_request_content['category']

                    if interaction_content['type'] == 'text':
                        text_count += 1
                        interaction_content['content'] = interaction_content['content']['title']
                        interaction_content['bot_messages_count'] = ''
                        interaction_content['participant_messages_count'] = ''
                    elif interaction_content['type'] == 'video':
                        video_count += 1
                        interaction_content['content'] = interaction_content['content']['title']
                        interaction_content['bot_messages_count'] = ''
                        interaction_content['participant_messages_count'] = ''
                    else:
                        chat_count += 1
                        bot_messages_count = 0
                        participant_messages_count = 0

                        parsed_messages = ""
                        for message in interaction_content['content']['messages']:
                            
                            if message['user_type'] == 'bot':
                                bot_messages_count += 1
                                bot_messages.loc[len(bot_messages.index)] = {"messages": message["text"], "participant_id": interaction_content["participant_id"]}

                            elif message['user_type'] == 'participant':
                                participant_messages_count += 1
                                participant_messages.loc[len(participant_messages.index)] = {"messages": message["text"], "participant_id": interaction_content["participant_id"]}

                            parsed_messages = parsed_messages + "\n__" + message['user_type'].capitalize() + "__: " + message['text'].strip() + "\n"

                        interaction_content['content'] = parsed_messages
                        interaction_content['bot_messages_count'] = bot_messages_count
                        interaction_content['participant_messages_count'] = participant_messages_count

                    interaction_df.loc[len(interaction_df.index)] = interaction_content

            about_request_content['video_count'] = video_count
            about_request_content['text_count'] = text_count
            about_request_content['chat_count'] = chat_count
            about_request_content['total_request_interactions'] = video_count + text_count + chat_count
            total_interactions += video_count + text_count + chat_count
            request_df.loc[len(request_df.index)] = about_request_content
    else:
        about_file_content['requests_count'] = 0
   
    about_file_content['total_interactions'] = total_interactions
    experiment_df.loc[len(experiment_df.index)] = about_file_content

with pandas.ExcelWriter("C:\\Users\\conso\\OneDrive\\Documents\\GitHub\\robot-barriers\\data\\interactions_summary_new.xlsx") as writer:
    experiment_df.to_excel(writer, sheet_name="Experiments", index=False)
    request_df.to_excel(writer, sheet_name="Requests", index=False)
    interaction_df.to_excel(writer, sheet_name="Interactions", index=False)
    participant_messages.to_excel(writer, sheet_name="Participant Messages", index=False)
    bot_messages.to_excel(writer, sheet_name="Bot Messages", index=False)