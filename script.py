import click
import feedparser
import logging
import logging.config
import os
from urllib import urlencode
from honcho import environ

@click.group()
def cli():
    """ Run the CLI tool from the specified arguments. """
    update_env();
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(levelname)s:%(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            }
        },
        'root': {
            'level': logging.DEBUG,
            'handlers': ['console'],
        }
    })


@click.command()
@click.argument('secrets_path', type=click.Path(exists=True))
@click.argument('token_path', type=click.Path())
@click.argument('scope', required=True, nargs=-1)
def oauth(secrets_path, token_path, scope):
    """Generate an OAuth token."""
    from oauth import get_credentials
    get_credentials(scope, secrets_path, token_path)


cli.add_command(oauth)


@click.command()
def upload():
    """Upload videos to Facebook from MRSS feed"""
    videos = parse_videos_from_feed();
    logging.info("Found %d videos to upload" % len(videos))
    for video in videos:
        upload_video_to_facebook( video )


cli.add_command(upload)


def parse_videos_from_feed():
    """
    Injest MRSS feed into local scope; format videos to FB upload spec
    """

    data = feedparser.parse(os.getenv('MTFV_MRSS_URL'))
    return [{
        'title': video['title'],
        'description': video['summary'],
        'file_url': video['media_content'][0]['url'],
        'file_size': video['media_content'][0]['filesize']} for video in data.entries]

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
    from oauth import authorize_installed_app

    http = authorize_installed_app(
        scope=('publish_actions',),
        env_key='FACEBOOK_OAUTH',
    )

    request_url = 'https://graph-video.facebook.com/v2.4/%s/videos' % ( os.getenv('MTFV_FACEBOOK_ENTITY_ID') )
    response = http.request( request_url, method='POST', body=urlencode(video) )
    logging.info(response)

