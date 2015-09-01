import os
import httplib2
from oauth2client.client import Credentials, Storage, flow_from_clientsecrets
from oauth2client.tools import argparser, run_flow


def authorize_service_account(scope, env=os.environ):
    """Prepare oAuth2 credentials for a service account.

    Environment:
        GOOGLE_SERVICE_ACCOUNT: Service account email address
        GOOGLE_SERVICE_KEY: Private key

    Returns:
        An authorized httplib2.Http() instance.
    """
    from oauth2client.client import SignedJwtAssertionCredentials

    credentials = SignedJwtAssertionCredentials(
        service_account_name=env['GOOGLE_SERVICE_ACCOUNT'],
        private_key=env['GOOGLE_SERVICE_KEY'].encode('utf-8'),
        scope=scope
    )

    return credentials.authorize(httplib2.Http())


def authorize_installed_app(scope, env_key):
    """Prepare oAuth2 credentials for an installed app.

    Args:
        env_key: The environment variable from which to read the credentials.
        scope: The scope needed. (Only used here for documentation purposes.)

    Returns:
        An authorized httplib2.Http() instance.
    """
    content = os.getenv(env_key)

    if not content:
        raise RuntimeError(
            'Missing credentials for %s' % env_key)

    try:
        credentials = Credentials.new_from_json(content)
        if credentials.invalid:
            raise ValueError()
    except ValueError:
        raise RuntimeError(
            'Invalid credentials for %s' % env_key)

    return credentials.authorize(httplib2.Http())


class JsonStorage(Storage):
    def __init__(self, path):
        self._path = path

    def locked_put(self, credentials):
        """Write Credentials to a file.

        Args:
            credentials: The Credentials to store.
        """
        with open(self._path, 'w') as fp:
            fp.write(credentials.to_json())

    def locked_delete(self):
        del os.environ[self._key]


def get_credentials(scope, secrets_path, token_path):
    storage = JsonStorage(token_path)

    flow = flow_from_clientsecrets(secrets_path, scope)

    run_flow(flow, storage, argparser.parse_args([]))
