from typing import Iterable

import pygame as pg

class GUIElement:
    def __init__(self, rect: list[float]):
        self.rect = rect
        self.enabled = True
        self.visible = True
    
    def update(self, events: Iterable[pg.Event]):
        raise NotImplementedError()
    
    def draw(self, screen: pg.Surface):
        raise NotImplementedError()