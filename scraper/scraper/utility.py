"""
Quick little utility functions.

Most of them interact with the provided redis client
"""

import json

def set_story(db_client, info):
    """Adds the story to redis"""
    url = info['url']
    info = json.dumps(info)
    db_client.pipeline().set(url, info).expire(url, 3600000).execute()

    return
