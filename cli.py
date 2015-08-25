import os
import logging
import logging.config
import click

@click.group()
def cli(verbose, env, dev_env):
    """ Run the CLI tool from the specified arguments. """
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
        'loggers': {
            'glance': {
                'level': logging.INFO,
                'handlers': ['console'],
                'propagate': False,
            },
        },
        'root': {
            'level': logging.DEBUG if verbose else logging.WARNING,
            'handlers': ['console'],
        }
    })


@click.command()
@click.argument('secrets_path', type=click.Path(exists=True))
@click.argument('token_path', type=click.Path())
@click.argument('scope', required=True, nargs=-1)
def oauth(secrets_path, token_path, scope):
    """Generate an OAuth token."""
    from .oauth import get_credentials
    print secrets_path
    get_credentials(scope, secrets_path, token_path)

cli.add_command(oauth)
