import json
from typing import Callable, Tuple

from consul import Consul

from rconfig.utils import set_envs


def load_envs_from_consul(
        host: str,
        port: int,
        token: str,
        key: str,
        *other_keys: Tuple[str],
        prefix: str = '',
        deserializer: Callable = json.loads,
        **kwargs,
) -> None:
    data = load_config_from_consul(
        host,
        port,
        token,
        key,
        *other_keys,
        deserializer=deserializer,
        **kwargs,
    )
    set_envs(data, prefix=prefix)


def load_config_from_consul(  # pylint: disable=too-many-arguments
        host: str,
        port: int,
        token: str,
        key: str,
        *other_keys: Tuple[str],
        deserializer: Callable = json.loads,
        **kwargs,
) -> dict:
    """
    Load config from a ``Consul`` server to a ``dict``.

    ::

      <path-to-app-config>
          |___LOG_LEVEL=INFO
          |___DEBUG=false

    Suppose you have created config of your app on the path
    ``path-to-app-config`` on ``Consul`` server.

    If passed multiple keys for configs
    will merge them with priority from first mension to last mension.

    :param str host: host of a ``Consul`` server
    :param int port: port of a ``Consul`` server
    :param str token: access key to a ``Consul`` server
    :param str key: key path to a main config
    :param Tuple[str] other_keys: other paths to configs that should be merged
      with a main config
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
    if not raw_configs[0]['Values']:
        raw_configs = raw_configs[1:]
    raw_configs = raw_configs[0:] if raw_configs else list()
    return {
        config['Key'].lstrip(key): deserializer(config['Value'])
        for config in raw_configs
    }
