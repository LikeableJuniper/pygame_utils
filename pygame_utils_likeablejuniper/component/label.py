from dataclasses import dataclass
from typing import Iterable, cast
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
            target.update_style(self)
        else:
            Label.default_style = self

DEFAULT_LABEL_STYLE = CompleteLabelStyle(background_color=(255, 255, 200), text_color=(0, 0, 0), font=pg.font.SysFont("Mono", 20))

class Label(GUIElement):
    default_style: CompleteLabelStyle = DEFAULT_LABEL_STYLE
    def __init__(self, rect: list[float], text: str, style: LabelStyle | None = None):
        super().__init__(rect, style, Label.default_style)
        self.style = cast(CompleteLabelStyle, self.style)
        self.text = text
    
    def update(self, events: Iterable[pg.Event]):
        raise NotImplementedError()

    def draw(self, screen: pg.Surface):
        super().draw(screen)

        text_surface = self.style.font.render(self.text, True, self.style.text_color)
        topLeft = Vector(self.rect[:2])
        widthHeight = Vector(self.rect[2:])
        text_rect = text_surface.get_rect(center=(topLeft + 0.5*widthHeight).components)
        screen.blit(text_surface, text_rect)

    def set_text(self, text: str):
        self.text = text
    
    def update_style(self, style: LabelStyle | CompleteLabelStyle):
        """
        Updates the style of this Label instance.<br>
        You may leave out fields of the style object, this means that those fields will not be updated as a result of this call.<br>
        If you want to revert the styling to the default, use<br>
        `label.update_style(Label.default_style)`
        """
        self.style = merge_styles(style, self.style)

class StaticLabel(Label):
    """
    If you know a labels value is not going to change often, use this class for improved performance.<br>
    It will only rerender text and recalculate positioning on __init__ and on set_text and set_style<br>
    """
    def __init__(self, rect: list[float], text: str, style: LabelStyle | None = None):
        super().__init__(rect, text, style)
        self.__rerender()
    
    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.style.background_color, self.rect)
        screen.blit(self.text_surface, self.text_rect)
    
    def set_text(self, text: str):
        super().set_text(text)
        self.__rerender()
    
    def update_style(self, style: LabelStyle | CompleteLabelStyle):
        super().update_style(style)
        self.__rerender()
    
    def __rerender(self):
        """
        Recalculates all drawing-relevant data, including rerendering font and text.<br>
        Calling this function manually is usually not required nor is it recommended, as calling it too much removes the benefit you get from using StaticLabel over Label.<br>
        If you need to call this method manually for changes to take place, you aren't using the api correctly.<br>
        """
        topLeft = Vector(self.rect[:2])
        widthHeight = Vector(self.rect[2:])
        self.text_surface = self.style.font.render(self.text, True, self.style.text_color)
        self.text_rect = self.text_surface.get_rect(center=(topLeft + 0.5*widthHeight).components)
