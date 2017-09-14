"""Script to analyse text using the Google Natural Language API."""

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def get_raw_entities(content):
    """
    Get the entities from a string of content.
    """
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('language', 'v1', credentials=credentials)
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'language': 'EN',
            'content': content,
        },
        'features': {
            'extract_entities': True,
        },
        'encodingType': 'UTF8',
    }
    request = service.documents().annotateText(body=body)
    response = request.execute(num_retries=3)
    return response['entities']


def process_entities(raw_entity_list):
    """
    Return a list of the entities with properties that are relevant to the
    scoring of the keywords
    """
    processed_entities = []
    for entity in raw_entity_list:
        entity_dict = {}
        if "wikipedia_url" in entity["metadata"]:
            entity_dict["wikipedia_url"] = entity["metadata"]["wikipedia_url"]
        else:
            entity_dict["wikipedia_url"] = ""
        entity_dict["name"] = entity["name"]
        entity_dict["mentions"] = len(entity["mentions"])
        entity_dict["salience"] = entity["salience"]
        entity_dict["type"] = entity["type"]
        processed_entities.append(entity_dict)
    return processed_entities


def extract_entities(content):
    """
    Run content through Google's NLP algorithm to get a list of dictionaries of
    entities and their corresponding properties.
    """
    raw_entities = get_raw_entities(content)
    return process_entities(raw_entities)
