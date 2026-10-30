import os
import json
import uuid 
from datetime import datetime

# CRUD Experiment
def create_experiment():
    participant_id = datetime.now().strftime("p%m%d%H%M")
    created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    experiment_data = update_experiment(participant_id, created_at, None)
    return participant_id

def read_experiment(participant_id):
    if os.path.isdir('data/participants/' + participant_id):
        with open('data/participants/' + participant_id + '/about_experiment.json', 'r') as experiment_file:
            experiment_data = json.load(experiment_file)
            return experiment_data

def close_experiment(participant_id):
    experiment_data = read_experiment(participant_id)
    
    if experiment_data:
        experiment_data['closed_at'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        update_experiment(**experiment_data)
    

def update_experiment(participant_id, created_at, closed_at):
    if not os.path.isdir('data/participants/' + participant_id):
        os.makedirs('data/participants/' + participant_id)

    with open('data/participants/last_experiment.json', 'w') as last_experiment_file:
        with open('data/participants/' + participant_id + '/about_experiment.json', 'w') as experiment_file:
            experiment_data = {'participant_id': participant_id,
                               'created_at': created_at,
                               'closed_at': closed_at}

            json_data = json.dumps(experiment_data)
            experiment_file.write(json_data)
            last_experiment_file.write(json_data)

    return experiment_data

def read_last_experiment():
    if os.path.isfile('data/participants/last_experiment.json'):
        with open('data/participants/last_experiment.json', 'r') as last_experiment_file:
            experiment_data = json.load(last_experiment_file)
            return experiment_data

# CRUD Request
def create_request(participant_id, description, category):
    request_id = 'request_' + str(uuid.uuid4().hex)
    created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    update_request(participant_id, request_id, description, category, created_at, None, None)
    return request_id

def close_request(participant_id, request_id, feedback):
    request_data = read_request(participant_id, request_id)
    
    if request_data:
        request_data['closed_at'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        request_data['feedback'] = [feedback]
        update_request(**request_data)
    
def read_request(participant_id, request_id):
    if os.path.isdir('data/participants/' + participant_id + '/requests/' + request_id):
        with open('data/participants/' + participant_id + '/requests/' + request_id + '/about_request.json', 'r') as request_file:
            request_data = json.load(request_file)
            return request_data

def update_request(participant_id, request_id, description, category, created_at, closed_at, feedback):
    if not os.path.isdir('data/participants/' + participant_id + '/requests/' + request_id):
        os.makedirs('data/participants/' + participant_id + '/requests/' + request_id)

    with open('data/participants/' + participant_id + '/requests/last_request.json', 'w') as last_request_file:
        with open('data/participants/' + participant_id + '/requests/' + request_id + '/about_request.json', 'w') as request_file:
            request_data = {'request_id': request_id,
                            'participant_id': participant_id,
                            'description': description,
                            'category': category,
                            'created_at': created_at,
                            'closed_at': closed_at,
                            'feedback': feedback}

            json_data = json.dumps(request_data)
            request_file.write(json_data)
            last_request_file.write(json_data)
    
    return request_data

def read_last_request(participant_id):
    if os.path.isfile('data/participants/' + participant_id + '/requests/last_request.json'):
        with open('data/participants/' + participant_id + '/requests/last_request.json', 'r') as last_request_file:
            request_data = json.load(last_request_file)
            return request_data

# CRUD Interaction
def create_interaction(participant_id, request_id, type, content):
    interaction_id = 'interaction_' + str(uuid.uuid4().hex)
    created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    update_interaction(participant_id, request_id, interaction_id, type, content, created_at, None)
    return interaction_id

def read_interaction(participant_id, request_id, interaction_id):
    if os.path.isdir('data/participants/' + participant_id + '/requests/' + request_id + '/interactions'):
        with open('data/participants/' + participant_id + '/requests/' + request_id + '/interactions/' + interaction_id + '.json', 'r') as interaction_file:
            interaction_data = json.load(interaction_file)
            return interaction_data

def close_interaction(participant_id, request_id, interaction_id):
    interaction_data = read_interaction(participant_id, request_id, interaction_id)
    
    if interaction_data:
        interaction_data['closed_at'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        update_interaction(**interaction_data)

def update_interaction(participant_id, request_id, interaction_id, type, content, created_at, closed_at):
    if not os.path.isdir('data/participants/' + participant_id + '/requests/' + request_id + '/interactions'):
        os.makedirs('data/participants/' + participant_id + '/requests/' + request_id + '/interactions')

    with open('data/participants/' + participant_id + '/requests/' + request_id + '/' + 'last_interaction.json', 'w') as last_interaction_file:
        with open('data/participants/' + participant_id + '/requests/' + request_id + '/interactions/' + interaction_id + '.json', 'w') as interaction_file:
            request_data = {'interaction_id': interaction_id,
                            'request_id': request_id,
                            'participant_id': participant_id,
                            'type': type,
                            'content': content,
                            'created_at': created_at,
                            'closed_at': closed_at}

            json_data = json.dumps(request_data)
            interaction_file.write(json_data)
            last_interaction_file.write(json_data)

def read_last_interaction(participant_id, request_id):
    if os.path.isfile('data/participants/' + participant_id + '/requests/' + request_id + '/' + 'last_interaction.json'):
        with open('data/participants/' + participant_id + '/requests/' + request_id + '/' + 'last_interaction.json', 'r') as last_interaction_file:
            request_data = json.load(last_interaction_file)
            return request_data