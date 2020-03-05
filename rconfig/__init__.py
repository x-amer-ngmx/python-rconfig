import json
import os
from typing import Any, Callable

from consul import Consul


def load_config_from_consul(  # pylint: disable=too-many-arguments
        host: str,
        port: int,
        token: str,
        key: str,
        *other_keys: str,
        deserializer: Callable = json.loads,
        **kwargs,
) -> dict:
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
    :param str key:
    :param str other_keys:
    :param Callable deserializer:
    """
    server = Consul(host, port, token, **kwargs)
    main_config = _get_config_for_keys_from_consul(
        server, f'{key.strip("/")}/', deserializer=deserializer,
    )
    other_configs = list()
    if other_keys:
        other_configs = [
            _get_config_for_keys_from_consul(
                server, f'{other_key.strip("/")}/', deserializer=deserializer,
            ) for other_key in other_keys
        ]

    configs = dict()
    for config in [main_config, *other_configs][::-1]:
        configs.update(config)
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


def _serialize_value_to_json(value: Any) -> str:
    return json.dumps(value) if not isinstance(value, (str)) else value


def _set_environment_variables(
        config: dict,
        prefix: str = '',
        serializer: Callable = _serialize_value_to_json,
) -> None:
    for key, value in config.items():
        os.environ[f'{prefix}{key}'] = serializer(value)
