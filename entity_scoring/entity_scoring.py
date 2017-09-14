from extract_content_data import get_article_content
from google_nlp import extract_entities
import lxml.html as HTML
import numpy as np


def parse_xml(xml_content):
    """
    Parse through XML tags to extract the content
    """
    return HTML.fromstring(xml_content).text_content().replace('.', '. ')


def rescore_salience(entities):
    """
    rescore the salience for the entities by simply multiplying by the number
    of mentions and doubling the score if the entity type is something other
    than "OTHER"
    """
    for entity_data in entities:
        entity_data["score"] = entity_data["salience"] * entity_data["mentions"]
        entity_data["score"] *= 2 if entity_data["type"] != "OTHER" else entity_data["score"]
    return entities


def softmax(x):
    """
    Compute softmax values for each sets of scores in x.
    """
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def apply_softmax_to_entity_scores(entities):
    """
    Take entity scores and apply softmax function to ensure values between
    0 and 1
    """
    score_array = np.array([x["score"] for x in entities])
    normalised_scores = softmax(score_array)
    for norm_score, entity_data in zip(normalised_scores, entities):
        entity_data["score"] = norm_score
    return entities


def score_article_entities(article_id):
    """
    Method to extract text for a given article and score the entities that are
    found in the text

    Parameters
    ----------
    article_id : str
        uuid of a given article

    Returns
    -------
    entities: list
        List of dictionaries. 1 dictionary per entity containing data about
        that entity. The calculated score value can be accessed with the
        "score" key.
    """
    data = get_article_content(article_id)
    cleaned_text = parse_xml(data["content"])
    entities = extract_entities(cleaned_text)
    entities = rescore_salience(entities)
    return apply_softmax_to_entity_scores(entities)


if __name__ == "__main__":
    article_id = "cc9aee50-98af-11e7-88ed-216bee20271a"
    entities = score_article_entities(article_id)
