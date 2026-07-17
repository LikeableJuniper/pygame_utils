from dataclasses import dataclass
from typing import Iterable
from vectors_likeablejuniper import Vector
import pygame as pg

from pygame_utils_likeablejuniper.core.element import GUIElement
from pygame_utils_likeablejuniper.style.style import Style, merge_styles

@dataclass
class LabelStyle(Style):
    """
    A style property with value None indicates that it should just be the default value.
    """
    background_color: pg.typing.ColorLike | None = None
    text_color: pg.typing.ColorLike | None = None
    font: pg.font.Font | None = None

@dataclass
class CompleteLabelStyle(Style):
    """
    Always needs all fields to be non-None. Is used for defining fallback values and the result of merge_styles()
    """
    background_color: pg.typing.ColorLike
    text_color: pg.typing.ColorLike
    font: pg.font.Font
    
    def apply(self, target: Label | None = None):
        if target:
            target.style = self
        else:
            Label.default_style = self

DEFAULT_LABEL_STYLE = CompleteLabelStyle(background_color=(255, 255, 200), text_color=(0, 0, 0), font=pg.font.SysFont("Mono", 20))

class Label(GUIElement):
    default_style: CompleteLabelStyle = DEFAULT_LABEL_STYLE
    def __init__(self, rect: list[float], text: str, style: LabelStyle | None = None):
        super().__init__(rect)

        self.style: CompleteLabelStyle = merge_styles(style, Label.default_style)
        self.text = text
    
    def update(self, events: Iterable[pg.Event]):
        raise NotImplementedError()

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.style.background_color, self.rect)

        text_surface = self.style.font.render(self.text, True, self.style.text_color)
        topLeft = Vector(self.rect[:2])
        widthHeight = Vector(self.rect[2:])
        text_rect = text_surface.get_rect(center=(topLeft + 0.5*widthHeight).components)
        screen.blit(text_surface, text_rect)

    def set_text(self, text: str):
        self.text = text

class StaticLabel(Label):
    """
    If you know a labels value is never going to change, use this class for improved performance.
    """
    def __init__(self, rect: list[float], text: str, style: LabelStyle | None = None):
        super().__init__(rect, text, style)

        topLeft = Vector(self.rect[:2])
        widthHeight = Vector(self.rect[2:])
        self.text_surface = self.style.font.render(self.text, True, self.style.text_color)
        self.text_rect = self.text_surface.get_rect(center=(topLeft + 0.5*widthHeight).components)
    
    def draw(self, screen: pg.Surface):
        screen.blit(self.text_surface, self.text_rect)
