import os
import re


def get_env_var(name, default=None, prefix='WEBSOCKET_EXPORTER_'):
    """ Returns the value of the environment variable with th given name
    :param name: name of environment variable
    :param prefix prefix to env var name
    :param default: default value if the environment variable was not set
    :return: value of the given environment variable
    """
    if not prefix:
        prefix = ''
    return os.environ.get(f'{prefix}{name}', default)


def validate_uri(uri):
    assert re.match(r'wss?://\S+', uri.strip()), "Not a valid websocket uri, start with ws(s)://"


URI = get_env_var('URI')
MESSAGE = get_env_var('SAMPLE_MESSAGE', None)
EXPECTED_MESSAGE = get_env_var('EXPECTED_MESSAGE', None)
MATCH_TYPE = get_env_var("MATCH_TYPE", 'contains')
TIMEOUT = int(get_env_var("TIMEOUT", '10'))
LISTEN_ADDR = get_env_var('LISTEN_ADDR', '0.0.0.0')
LISTEN_PORT = int(get_env_var('LISTEN_PORT', '9896'))
