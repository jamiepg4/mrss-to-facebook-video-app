import feedparser
import json
import os
import requests
from honcho import environ

def parse_videos_from_feed():
    """
    Injest MRSS feed into local scope; format videos to FB upload spec
    """

    data = feedparser.parse(os.getenv('MTFV_MRSS_URL'))
    videos = []
    for i, video in enumerate(data.entries):
        to_append = {}
        to_append['file_url'] = video['media_content'][0]['url']
        to_append['file_size'] = video['media_content'][0]['filesize']
        to_append['title'] = video['title']
        # to_append['thumb'] = video['media_thumbnail']['url'] # Requires downloading and including in post body
        videos.append( to_append )
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

def upload_video_to_facebook(video):
    """
    Uploads a given video to Facebook Graph API
    """

    request_url = 'https://graph-video.facebook.com/v2.3/%s/videos' % ( os.getenv('MTFV_FACEBOOK_ENTITY_ID') )
    print request_url
    print video
    response = requests.post( request_url, video )
    print response


update_env();
videos = parse_videos_from_feed();
for video in videos:
    upload_video_to_facebook( video )
