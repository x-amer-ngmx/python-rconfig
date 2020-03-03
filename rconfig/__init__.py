import json
import os
from typing import Any, Callable, Optional, Union

from consul import Consul


def load_config_from_consul(  # pylint: disable=too-many-arguments
        host: str,
        port: int,
        token: str,
        root_key: str,
        app_key: str,
        env_key: str,
        common_key: Optional[str] = None,
        value_deserializer=json.loads,
        deserializer: Callable = lambda x: x,
        **kwargs,
) -> Union[object, dict]:
    """
    Load config from ``consul`` server.

    It expects the following key structure on ``consul`` side

    <root-key>
        |____<common-config-key>
        |          |
        |          |___<some-env-key>
        |          |           |_____<key-value>
        |          |           |_____<key-value>
        |          |
        |          |___<another-env-key>
        |                      |_____<key-value>
        |                      |_____<key-value>
        |____<app-config-key>
                   |
                   |___<some-env-key>
                   |           |_____<key-value>
                   |           |_____<key-value>
                   |
                   |___<another-env-key>
                               |_____<key-value>
                               |_____<key-value>


    :param str host: host of consule server
    :param int port:
    :param str root_key:
    :param str app_key:
    :param str env_key:
    :param str common_key:
    """
    server = Consul(host, port, token, **kwargs)
    common_config = dict()
    if common_key:
        common_config = _get_config_for_keys_from_consul(
            server,
            f'{root_key}/{common_key}/{env_key}/',
            deserializer=value_deserializer,
        )

    app_config = _get_config_for_keys_from_consul(
        server,
        f'{root_key}/{app_key}/{env_key}/',
        deserializer=value_deserializer,
    )
    configs = deserializer({**common_config, **app_config})
    return configs


def _get_config_for_keys_from_consul(
        server: Consul,
        key: str,
        deserializer: Callable,
) -> dict:
    _, raw_configs = server.kv.get(key, recurse=True)
    raw_configs = raw_configs[1:] if raw_configs else list()
    return {
        config['Key'].lstrip(key): deserializer(config['Value'])
        for config in raw_configs
    }


def _set_environment_variables(config: dict, prefix: str = '') -> None:
    for key, value in config.items():
        os.environ[f'{prefix}{key}'] = _serialize_value(value)


def _serialize_value(
        value: Any,
        serializer: Callable = lambda x: json.dumps(x)
        if isinstance(x, (dict, list)) else str(x)
) -> str:
    return serializer(value)
