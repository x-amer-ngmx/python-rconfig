import sys
from enum import Enum
from typing import Callable, Optional

from rconfig import _serialize_value_to_json


try:
    import yaml
except ImportError:
    yaml = None


class ScriptFormat(Enum):
    inline: str = 'inline'
    new_line: str = 'new_line'


def to_bash(
        data: dict,
        format: ScriptFormat = ScriptFormat.inline,  # pylint: disable=W0622
        serializer: Callable = _serialize_value_to_json,
        prefix: str = '',
) -> Optional[str]:
    inline = ScriptFormat.inline == format
    bash = str()
    for key, value in data.items():
        line = f'{prefix}{key}={serializer(value)!r}'
        bash += f' {line}' if inline else f'export {line}\n'
    if not bash:
        return None
    return f'export {bash}' if inline else bash.rstrip('\n')


def to_yaml(data: dict, prefix: str = '') -> Optional[str]:
    if yaml is None:
        sys.stderr.write(
            'Missing yaml package.\nRun pip install "rconfig[yaml]"'
        )
    if not data:
        return None
    return yaml.dump(
        {f'{prefix}{k}': v for k, v in data.items()},
        default_flow_style=False,
    )
