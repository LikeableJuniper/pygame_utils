from dataclasses import dataclass
from typing import Any, Callable, Iterable
import pygame as pg
from vectors_likeablejuniper import Vector

from pygame_utils_likeablejuniper.core.element import GUIElement
from pygame_utils_likeablejuniper.style.style import Border, Style, merge_styles


@dataclass
class ButtonStyle(Style):
    """
    A style property with value None indicates that it should just be the default value.
    """
    background_color: pg.typing.ColorLike | None = None
    border: Border | None = None
    text_color: pg.typing.ColorLike | None = None
    font: pg.font.Font | None = None

@dataclass
class CompleteButtonStyle(Style):
    """
    Always needs all fields to be non-None. Is used for defining fallback values and the result of merge_styles()
    """
    background_color: pg.typing.ColorLike
    border: Border
    text_color: pg.typing.ColorLike
    font: pg.font.Font
    
    def apply(self, target: 'Button | None' = None):
        if target:
            target.update_style(self)
        else:
            Button.default_style = self

DEFAULT_BUTTON_STYLE = CompleteButtonStyle(background_color=(161, 253, 255), border=Border(0, (0, 0, 0)), text_color=(0, 0, 0), font=pg.font.SysFont("Mono", 20))
DEFAULT_BUTTON_HOVER_STYLE = CompleteButtonStyle(background_color=(82, 168, 191), border=Border(0, (0, 0, 0)), text_color=(0, 0, 0), font=pg.font.SysFont("Mono", 20))

class Button(GUIElement[ButtonStyle, CompleteButtonStyle]):
    default_style: CompleteButtonStyle = DEFAULT_BUTTON_STYLE
    default_hover_style: CompleteButtonStyle = DEFAULT_BUTTON_HOVER_STYLE

    def __init__(self, rect: list[float], text: str | None = None, on_click: Callable[..., Any] | None = None, style: ButtonStyle | None = None, hover_style: ButtonStyle | None = None):
        # self.text assignment must be before super().__init__() because Button overrides _rerender() and uses self.text in it, which is called in GUIElement.__init__()
        self.text = text or ""
        super().__init__(rect, style, Button.default_style)
        self.on_click = on_click or (lambda: None)
        self.idle_style = merge_styles(style, Button.default_style)
        self.hover_style = merge_styles(hover_style, Button.default_hover_style)
        # even though the mouse position is checked every time update() is called, this variable is used to prevent unnecessary style updates and rerenders
        self.hovered = False
        self.being_clicked = False
    
    def update(self, events: Iterable[pg.Event]):
        mouse_pos = Vector(pg.mouse.get_pos())
        top_left = Vector(self.rect[:2])
        width_height = Vector(self.rect[2:])
        in_rect = top_left < mouse_pos < top_left + width_height
        if in_rect and (not self.hovered or self.style != self.hover_style):
            self.hovered = True
            self.update_style(self.hover_style)
        elif not in_rect and self.hovered:
            self.hovered = False
            self.update_style(self.idle_style)
        
        if self.hovered:
            clicked = pg.mouse.get_pressed()[0]
            if clicked and not self.being_clicked:
                self.being_clicked = True
                self.on_click()
            elif not clicked and self.being_clicked:
                self.being_clicked = False

    def draw(self, screen: pg.Surface):
        super().draw(screen)

        if self.text:
            screen.blit(self.text_surface, self.text_rect)

    def set_text(self, text: str):
        self.text = text
        self._rerender()
    
    def update_hover_style(self, style: ButtonStyle | CompleteButtonStyle):
        self.hover_style = merge_styles(style, self.hover_style)
        self._rerender()
    
    def _rerender(self):
        super()._rerender()

        if self.text:
            top_left = Vector(self.rect[:2])
            width_height = Vector(self.rect[2:])
            self.text_surface = self.style.font.render(self.text, True, self.style.text_color)
            self.text_rect = self.text_surface.get_rect(center=(top_left + 0.5*width_height).components)
