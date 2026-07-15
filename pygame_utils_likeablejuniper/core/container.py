from typing import Iterable
import pygame as pg

from pygame_utils_likeablejuniper.core.element import GUIElement


class Container(GUIElement):
    def __init__(self, elements: list[GUIElement]):
        self.elements = elements
    
    def update(self, events: Iterable[pg.Event]):
        for element in self.elements:
            if element.enabled:
                element.update(events)
    
    def draw(self, screen: pg.Surface):
        for element in self.elements:
            if element.visible:
                element.draw(screen)
    
    def add(self, element: GUIElement):
        if isinstance(element, GUIElement):
            self.elements.append(element)
        else:
            raise TypeError("Can only add GUIElement to Container")