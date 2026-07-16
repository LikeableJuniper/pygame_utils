from typing import Iterable
from vectors_likeablejuniper import Vector
import pygame as pg

from pygame_utils_likeablejuniper.core.element import GUIElement
from pygame_utils_likeablejuniper.style.style import LabelStyle

class Label(GUIElement):
    default_style: LabelStyle
    def __init__(self, rect: list[float], text: pg.Surface, style: LabelStyle | None = None):
        super().__init__(rect)
        topLeft = Vector(rect[:2])
        widthHeight = Vector(rect[2:])

        self.text = text
        self.text_rect = text.get_rect(center=(topLeft + 0.5*widthHeight).components)
    
    def update(self, events: Iterable[pg.Event]):
        raise NotImplementedError()

    def draw(self, screen: pg.Surface):
        screen.blit(self.text, self.text_rect)

    def set_text(self, text: pg.Surface):
        self.text = text