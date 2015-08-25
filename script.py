import feedparser
import os
from honcho import environ

def parse_videos_from_feed():
    """
    Injest MRSS feed into local scope
    """

    data = feedparser.parse(os.getenv('MTFV_MRSS_URL'))
    videos = []
    for i, video in enumerate(data.entries):
        videos.append( video )
    return videos

def update_env(filename='.env'):
    """
    Update os.environ with variables from an .env file.

    Parameters:
        filename (Optional[str]): the name of the .env file. Defaults to '.env'.
    """
    with open(filename) as f:
        content = f.read()
    envvars = environ.parse(content)

    for k, v in envvars.items():
        os.environ[k] = v

update_env();
videos = parse_videos_from_feed();
print videos
