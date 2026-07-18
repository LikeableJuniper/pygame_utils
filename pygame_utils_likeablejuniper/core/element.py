from typing import Callable, Generic, Iterable, Self, TypeVar

import pygame as pg

from pygame_utils_likeablejuniper.style.style import Style, merge_styles

E = TypeVar("E", bound='GUIElement')
class ConditionalStyle(Generic[E]):
    def __init__(self, condition: Callable[[E], bool], style: Style):
        self.condition = condition
        self.style = style

S = TypeVar("S", bound=Style)
C = TypeVar("C", bound=Style)
class GUIElement(Generic[S, C]):
    def __init__(self, rect: list[float], style: S | None, base_style: C):
        self.rect = rect
        self.style = merge_styles(style, base_style)
        self.unconditional_style = self.style
        self.conditional_styles: list[ConditionalStyle] = []
        self._rerender()
        self.enabled = True
        self.visible = True
    
    def update(self, events: Iterable[pg.Event]):
        raise NotImplementedError()
    
    def draw(self, screen: pg.Surface):
        self.__draw_background(screen)
        self.__draw_border(screen)
    
    def update_style(self, style: S | C):
        self.unconditional_style = merge_styles(style, self.unconditional_style)
        self.conditional_styles.clear()
        self._rerender()
    
    def add_conditional_style(self, condition: Callable[[Self], bool], style: S | C):
        self.conditional_styles.append(ConditionalStyle(condition, style))
        self._rerender()
    
    def _rerender(self):
        """
        Recalculates all drawing-relevant data, including rerendering font and text.<br>
        Calling this function manually is usually not required nor is it recommended.<br>
        If you need to call this method manually for changes to take place, you aren't using the api correctly.<br>
        """

        self.style = self.unconditional_style
        for conditional_style in self.conditional_styles:
            if conditional_style.condition(self):
                self.style = merge_styles(conditional_style.style, self.style)

        if self.__has_background():
            self.background_surface = pg.Surface(self.rect[2:])
            if len(self.style.background_color) >= 4: # pyright: ignore[reportAttributeAccessIssue]
                self.background_surface.set_alpha(self.style.background_color[3]) # pyright: ignore[reportAttributeAccessIssue]
            self.background_surface.fill(self.style.background_color) # pyright: ignore[reportAttributeAccessIssue]

    def __draw_background(self, screen: pg.Surface):
        if self.__has_background():
            screen.blit(self.background_surface, self.rect[:2])
    
    def __draw_border(self, screen: pg.Surface):
        if self.__has_border():
            self.style.border.draw(screen, self.rect) # pyright: ignore[reportAttributeAccessIssue]
    
    def __has_background(self):
        return hasattr(self.style, "background_color")

    def __has_border(self):
        return hasattr(self.style, "border")