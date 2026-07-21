from dataclasses import dataclass
from typing import Iterable, cast
import pygame as pg

from pygame_utils_likeablejuniper.core.element import GUIElement
from pygame_utils_likeablejuniper.layout.layout import Layout
from pygame_utils_likeablejuniper.style.style import Border, Style, merge_styles


@dataclass
class ContainerStyle(Style):
    """
    A style property with value None indicates that it should just be the default value.
    """
    background_color: pg.typing.ColorLike | None = None
    border: Border | None = None

@dataclass
class CompleteContainerStyle(Style):
    """
    Always needs all fields to be non-None. Is used for defining fallback values and the result of merge_styles()
    """
    background_color: pg.typing.ColorLike
    border: Border
    
    def apply(self, target: 'Container | None' = None):
        if target:
            target.style = self
        else:
            Container.default_style = self

DEFAULT_CONTAINER_STYLE = CompleteContainerStyle((0, 0, 0, 0), Border(0, (0, 0, 0)))

class Container(GUIElement):
    default_style: CompleteContainerStyle = DEFAULT_CONTAINER_STYLE
    def __init__(self, rect: list[float], layout: Layout | None = None, elements: list[GUIElement] | None = None, style: ContainerStyle | None = None):
        self.layout = layout
        if self.layout:
            self.layout.set_rect(rect)
        super().__init__(rect, style, Container.default_style)
        self.elements = elements or []
        self.style = merge_styles(style, Container.default_style)
    
    def update(self, events: Iterable[pg.Event]):
        super().update(events)
        for element in self.elements:
            if element.enabled:
                element.update(events)
    
    def draw(self, screen: pg.Surface):
        super().draw(screen)

        for element in self.elements:
            if element.visible:
                element.draw(screen)
    
    def add(self, element: GUIElement):
        if isinstance(element, GUIElement):
            self.elements.append(element)
            if self.layout:
                self.layout.apply(self.elements)
            self._rerender()
        else:
            raise TypeError("Can only add GUIElement to Container")