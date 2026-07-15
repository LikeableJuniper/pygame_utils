from typing import Iterable

import pygame as pg

from pygame_utils_likeablejuniper.core.element import GUIElement

class Label(GUIElement):
    def __init__(self, rect: pg.Rect, text: str):
        super().__init__(rect)
        self.text = text
    
    def update(self, events: Iterable[pg.Event]):
        raise NotImplementedError()

    def draw(self, screen: pg.Surface):
        raise NotImplementedError()

    def set_text(self, text: str):
        self.text = text