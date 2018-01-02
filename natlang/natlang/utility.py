"""
Quick little utility functions.

Most of them interact with the provided redis client
"""

import json
from natlang.nlp import process_txt


# Quick Utility functions
def append_nlp(result):
    """Runs the nlp pipeline and adds to result"""
    combined_txt = "\n".join(
        [result['title'], result['desc'], result['story']])

    return {**result, **process_txt(combined_txt)}


def set_story(db_client, info):
    """Adds the story to redis"""
    url = info['url']
    info = json.dumps(info)
    db_client.pipeline().set(url, info).expire(url, 3600000).execute()

    return