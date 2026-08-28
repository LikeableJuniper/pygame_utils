from dataclasses import dataclass
from typing import Iterable
import pygame as pg
from vectors_likeablejuniper import Vector

from pygame_utils_likeablejuniper.core.element import GUIElement
from pygame_utils_likeablejuniper.style.style import Border, Style, merge_styles


@dataclass
class InputStyle(Style):
    """
    A style property with value None indicates that it should just be the default value.
    """
    background_color: pg.typing.ColorLike | None = None
    border: Border | None = None
    text_color: pg.typing.ColorLike | None = None
    font: pg.font.Font | None = None

@dataclass
class CompleteInputStyle(Style):
    """
    Always needs all fields to be non-None. Is used for defining fallback values and the result of merge_styles()
    """
    background_color: pg.typing.ColorLike
    border: Border
    text_color: pg.typing.ColorLike
    font: pg.font.Font
    
    def apply(self, target: 'Input | None' = None):
        if target:
            target.update_style(self)
        else:
            Input.default_style = self

DEFAULT_INPUT_STYLE = CompleteInputStyle(background_color=(255, 255, 200), border=Border(0, (0, 0, 0)), text_color=(0, 0, 0), font=pg.font.SysFont("Mono", 20))
DEFAULT_INPUT_ACTIVE_STYLE = CompleteInputStyle(background_color=(181, 181, 130), border=Border(5, (150, 150, 110)), text_color=(0, 0, 0), font=pg.font.SysFont("Mono", 20))

class Input(GUIElement[InputStyle, CompleteInputStyle]):
    default_style: CompleteInputStyle = DEFAULT_INPUT_STYLE
    default_active_style: CompleteInputStyle = DEFAULT_INPUT_ACTIVE_STYLE

    def __init__(self, rect: list[float], text: str | None = None, style: InputStyle | None = None):
        """
        Passing a custom style will also override the default active style on the supplied properties.
        This means you might have to manually set an active style, even if you only intended to set the non-active style.
        """
        # self.text assignment must be before super().__init__() because Input overrides _rerender() and uses self.text in it, which is called in GUIElement.__init__()
        self.text = text or ""
        self.text_surface: pg.Surface
        self.text_rect: pg.Rect
        self.cursor = len(self.text)
        self.last_cursor_visibility_change = 0
        self.cursor_blink_visible = True
        self.cursor_rect: list[float]
        super().__init__(rect, style, Input.default_style)
        self.active = False
        self.add_conditional_style(lambda input: input.active, merge_styles(style, Input.default_active_style))
    
    def update(self, events: Iterable[pg.Event], dt: float):
        super().update(events, dt)

        rerender_required = False
        
        clicked = pg.mouse.get_pressed()[0]
        if self.hovered and clicked and not self.active:
            self.active = True
            self.cursor = len(self.text)
            self.__reset_cursor_blink()
            rerender_required = True
        elif not self.hovered and clicked and self.active:
            self.active = False

        if self.active:
            self.last_cursor_visibility_change += dt
            if self.last_cursor_visibility_change >= 500:
                self.last_cursor_visibility_change -= 500
                self.cursor_blink_visible = not self.cursor_blink_visible
                rerender_required = True

            remove_count = 0
            add_str = ""
            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        remove_count += 1
                    elif event.key == pg.K_RIGHT:
                        self.cursor = min(self.cursor + 1, len(self.text))
                        rerender_required = True
                        self.__reset_cursor_blink()
                    elif event.key == pg.K_LEFT:
                        self.cursor = max(self.cursor - 1, 0)
                        rerender_required = True
                        self.__reset_cursor_blink()
                    else:
                        add_str += event.unicode

            if add_str or remove_count:
                if remove_count:
                    remove_count = min(remove_count, self.cursor)
                    self.text = self.text[:self.cursor - remove_count] + self.text[self.cursor:]
                    self.cursor -= remove_count
                self.text = self.text[:self.cursor] + add_str + self.text[self.cursor:]
                self.cursor += len(add_str)
                rerender_required = True
                self.__reset_cursor_blink()

        if rerender_required:
            self._rerender()

    def draw(self, screen: pg.Surface):
        super().draw(screen)

        if self.text:
            screen.blit(self.text_surface, self.text_rect)

        if self.cursor_blink_visible and self.active:
            pg.draw.rect(screen, self.style.text_color, self.cursor_rect)

    def set_text(self, text: str):
        self.text = text
        self._rerender()
    
    def _rerender(self):
        super()._rerender()

        if self.text:
            top_left = Vector(self.rect[:2])
            width_height = Vector(self.rect[2:])
            self.text_surface = self.__render_text(self.text)
            self.text_rect = self.text_surface.get_rect(center=(top_left + 0.5*width_height).components)

        if self.cursor_blink_visible:
            cursor_start = self.style.font.size(self.text[:self.cursor])[0]
            self.cursor_rect = [self.text_rect.left + cursor_start, self.text_rect.top, self.style.font.get_linesize()/23, self.text_rect.height]

    def __render_text(self, text: str):
        return self.style.font.render(text, True, self.style.text_color)

    def __reset_cursor_blink(self):
        self.last_cursor_visibility_change = 0
        self.cursor_blink_visible = True
