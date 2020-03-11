import json
import os
import sys
from typing import Callable, Optional


try:
    import yaml
except ImportError:
    yaml = None


def to_bash(
        data: dict,
        inline: bool = False,
        serializer: Callable = (
            lambda x: x if isinstance(x, str) else json.dumps(x)
        ),
        prefix: str = '',
) -> Optional[str]:
    bash = str()
    for key, value in data.items():
        line = f'{prefix}{key}={serializer(value)!r}'
        bash += f' {line}' if inline else f'export {line}\n'
    if not bash:
        return None
    return f'export {bash}' if inline else bash.rstrip('\n')


def to_yaml(
        data: dict,
        shallow: bool = False,
        serializer: Callable = (
            lambda x: json.dumps(x) if isinstance(x, (dict, list)) else x
        ),
        prefix: str = '',
) -> Optional[str]:
    if yaml is None:
        sys.stderr.write(
            'Missing yaml package.\nRun pip install "rconfig[yaml]"'
        )
    if not data:
        return None
    return yaml.dump(
        {
            f'{prefix}{k}': serializer(v) if shallow else v
            for k, v in data.items()
        },
        default_flow_style=False,
    )


def to_dotenv(
        data: dict,
        serializer: Callable = (
            lambda x: x if isinstance(x, str) else json.dumps(x)
        ),
        prefix: str = '',
) -> Optional[str]:
    envs = '\n'.join(f'{prefix}{k}={serializer(v)}' for k, v in data.items())
    return envs if envs else None


def to_json(
        data: dict,
        pretty: bool = False,
        prefix: str = '',
) -> Optional[str]:
    if not data:
        return None
    return json.dumps(
        {f'{prefix}{k}': v for k, v in data.items()},
        indent=4 if pretty else None,
    )


def set_envs(
        data: dict,
        prefix: str = '',
        serializer: Callable = (
            lambda x: x if isinstance(x, str) else json.dumps(x)
        ),
) -> None:
    for key, value in data.items():
        os.environ[f'{prefix}{key}'] = serializer(value)
