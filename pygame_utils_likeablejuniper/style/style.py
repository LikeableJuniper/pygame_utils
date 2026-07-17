from dataclasses import dataclass, fields
from typing import TypeVar


@dataclass
class Style:
    def apply(self):
        raise NotImplementedError()

P = TypeVar("P", bound=Style)
C = TypeVar("C", bound=Style)

def merge_styles(preferred: P | None, base: C) -> C:
    if P is None:
        return base
    
    values = {}

    for f in fields(base):
        pref = getattr(preferred, f.name, None)
        values[f.name] = pref if pref is not None else getattr(base, f.name)

    return type(base)(**values)