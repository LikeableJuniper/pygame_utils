from dataclasses import dataclass, fields
from typing import TypeVar
import pygame as pg


@dataclass
class Style:
    def apply(self):
        raise NotImplementedError()

@dataclass
class Border:
    """
    Setting border_width = 0 means no border (nothing will be drawn)
    """
    border_width: int
    border_color: pg.typing.ColorLike

    def draw(self, screen: pg.Surface, rect: list[float]):
        if self.border_width == 0:
            return
        
        pg.draw.rect(screen, self.border_color, rect, self.border_width)

P = TypeVar("P", bound=Style)
C = TypeVar("C", bound=Style)

def merge_styles(preferred: P | None, base: C) -> C:
    if preferred is None:
        return base
    
    values = {}

    for f in fields(base):
        pref = getattr(preferred, f.name, None)
        values[f.name] = pref if pref is not None else getattr(base, f.name)

    return type(base)(**values)