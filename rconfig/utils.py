from enum import Enum
from typing import Callable, Optional

from rconfig import _serialize_value_to_json


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
