from pygame_utils_likeablejuniper.core.element import GUIElement

from vectors_likeablejuniper import Vector


class LayoutParams:
    def __init__(self, gap: int = 0):
        self.gap = gap

DEFAULT_LAYOUT_PARAMS = LayoutParams(gap=20)

class Layout:
    def __init__(self, layout_params: LayoutParams | None = None):
        self.rect: list[float]
        self.layout_params = layout_params or DEFAULT_LAYOUT_PARAMS
    
    def set_rect(self, rect: list[float]):
        self.rect = rect

    def apply(self, elements: list[GUIElement]):
        raise NotImplementedError()

class LinearLayout(Layout):
    def __init__(self, direction: int, layout_params: LayoutParams | None = None):
        super().__init__(layout_params)
        self.direction = direction

    def set_rect(self, rect):
        self.rect = rect
        self.center = Vector(self.rect[:2]) + 0.5 * Vector(self.rect[2:])

    def apply(self, elements: list[GUIElement]):
        content_size = 0
        for element in elements:
            content_size += element.rect[self.direction + 2]
        content_size += self.layout_params.gap * (len(elements) - 1)

        starting_coords = self.center[self.direction] - content_size / 2

        shift = 0
        for element in elements:
            element.rect[self.direction] = starting_coords + shift
            element.rect[1 - self.direction] = self.center[1 - self.direction] - element.rect[(1 - self.direction) + 2] / 2
            element._rerender()
            shift += element.rect[self.direction + 2] + self.layout_params.gap

class VerticalLayout(LinearLayout):
    def __init__(self, layout_params: LayoutParams | None = None):
        super().__init__(1, layout_params)

class HorizontalLayout(LinearLayout):
    def __init__(self, layout_params: LayoutParams | None = None):
        super().__init__(0, layout_params)