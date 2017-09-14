"""Methods to get article meta data from a given source."""

import logging
import pandas as pd
import json
import os


def get_article_content(article_id, source=None, filename=None, project=None,
                        dataset=None, table=None):
    """
    Get article content from a given source
    """
    if source is not None:
        # Check that the source given is supported
        supported_sources = ["bq", "json"]
        source_err_msg = ("The source supplied: '{}', has not been found in "
                          "the list of supported sources: {}"
                          .format(source, ", ".join(supported_sources)))
        assert source.lower() in supported_sources, source_err_msg
    else:
        # If the data source isn't given then assume data source.
        logging.warn("Data source not specified. Assuming data is coming from "
                     "BigQuery.")
        source = "bq"
        project = "newsuk-datatech-datatonic"
        dataset = "tutorial_data"
        table = "content_data"

    if source.lower() == "bq":
        # Check that the relevant arguments have been given for the required
        # content source
        err_msg_suffix = ("argument has not been supplied despite BigQuery "
                          "being selected as the source.")
        assert project is not None, "The 'project' {}".format(err_msg_suffix)
        assert dataset is not None, "The 'dataset' {}".format(err_msg_suffix)
        assert table is not None, "The 'table' {}".format(err_msg_suffix)

        # Return content
        logging.info("Extracting article data from BigQuery.")
        return get_article_content_from_bq(article_id, project, dataset, table)

    elif source.lower() == "json":
        # Check that the json filename has been given
        file_extension = filename.split(".")[-1].lower()
        filename_missing_err = ("The filename has not been given despite JSON "
                                "file being selected as the source.")
        filename_ext_err = ("The file extension given: '{}', does not end "
                            "with 'json'. Please ensure that a json file is "
                            "given as input.".format(file_extension))
        assert filename is not None, filename_missing_err
        assert file_extension == "json", filename_ext_err

        # Return content
        logging.info("Extracting article data from JSON formatted file.")
        return get_article_content_from_json(filename)


def get_article_content_from_json(filename):
    """
    Get article content from a JSON file
    """
    # Check that the file exists.
    err_msg = ("File: {}, not found. Please ensure the filename is correct."
               .format(filename))
    assert os.path.isfile(filename), err_msg

    with open(filename, "r") as artk_data_file:
        artk_data = json.load(artk_data_file)
    return artk_data


def get_article_content_from_bq(article_id, project, dataset, table):
    """
    Run query to return the article content from the NLAConverter dataset in
    BigQuery
    """
    query = """
    SELECT
      article_id,
      title,
      content
    FROM
      [{}:{}.{}]
    WHERE
      article_id = '{}'
    """.format(project, dataset, table, article_id)
    df = pd.io.gbq.read_gbq(query=query, project_id=project)
    return df.to_dict(orient="records")[0]


if __name__ == "__main__":
    article_id = "cc9aee50-98af-11e7-88ed-216bee20271a"
    data = get_article_content(article_id)
