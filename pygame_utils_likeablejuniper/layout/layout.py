from pygame_utils_likeablejuniper.core.element import GUIElement

from vectors_likeablejuniper import Vector


class LayoutParams:
    """
    gap: the amount of space between elements in the layout. passing an int will set the same gap for both x and y axes, while passing a Vector will allow for different gaps in each axis
    direction: when using GridLayout, whether the layout should first fill along the x axis (0) or y axis (1)
    """
    def __init__(self, gap: float | Vector = 20, direction: int = 0):
        self.gap = gap if isinstance(gap, Vector) else Vector(gap, gap)
        self.direction = direction

DEFAULT_LAYOUT_PARAMS = LayoutParams(gap=20, direction=0)

class Layout:
    def __init__(self, layout_params: LayoutParams | None = None):
        self.rect: list[float]
        self.layout_params = layout_params or DEFAULT_LAYOUT_PARAMS
    
    def set_rect(self, rect: list[float]):
            self.rect = rect
            self.center = Vector(self.rect[:2]) + 0.5 * Vector(self.rect[2:])

    def apply(self, elements: list[GUIElement]):
        raise NotImplementedError()

class LinearLayout(Layout):
    def __init__(self, direction: int, layout_params: LayoutParams | None = None):
        super().__init__(layout_params)
        self.direction = direction

    def apply(self, elements: list[GUIElement]):
        content_size = 0
        for element in elements:
            content_size += element.rect[self.direction + 2]
        content_size += self.layout_params.gap[self.direction] * (len(elements) - 1)

        starting_coords = self.center[self.direction] - content_size / 2

        shift = 0
        for element in elements:
            new_pos = [0.0, 0.0]
            new_pos[self.direction] = starting_coords + shift
            new_pos[1 - self.direction] = self.center[1 - self.direction] - element.rect[(1 - self.direction) + 2] / 2
            element.set_rect(new_pos + element.rect[2:])
            shift += element.rect[self.direction + 2] + self.layout_params.gap[self.direction]

class VerticalLayout(LinearLayout):
    def __init__(self, layout_params: LayoutParams | None = None):
        super().__init__(1, layout_params)

class HorizontalLayout(LinearLayout):
    def __init__(self, layout_params: LayoutParams | None = None):
        super().__init__(0, layout_params)

class GridLayout(Layout):
    def __init__(self, layout_params: LayoutParams | None = None):
        super().__init__(layout_params)

    def apply(self, elements: list[GUIElement]):
        if len(elements) == 0:
            return

        gridded_elements: list[list[GUIElement]] = [[]]
        max_axis_size: float = 0
        max_cross_axis_size: list[float] = [0]
        # in this method "row" doesn't refer to a horizontal row necessarily, but rather a row along the main axis of the layout (which is determined by self.layout_params.direction)
        current_row_size = 0

        for element in elements:
            element_size = element.rect[2 + self.layout_params.direction]
            gap = (
                self.layout_params.gap[self.layout_params.direction]
                if gridded_elements[-1]
                else 0
            )

            # Wrap before placing the element, but only if the row already contains something.
            if (
                gridded_elements[-1]
                and current_row_size + gap + element_size > self.rect[2 + self.layout_params.direction]
            ):
                gridded_elements.append([])
                max_cross_axis_size.append(0)
                current_row_size = 0
                gap = 0

            # Place the element (guaranteed at least one per row)
            gridded_elements[-1].append(element)

            current_row_size += gap + element_size

            cross_size = element.rect[3 - self.layout_params.direction]
            if cross_size > max_cross_axis_size[-1]:
                max_cross_axis_size[-1] = cross_size

            if current_row_size > max_axis_size:
                max_axis_size = current_row_size

        content_dimensions = Vector(
            max_axis_size,
            sum(max_cross_axis_size) + self.layout_params.gap[1 - self.layout_params.direction] * (len(max_cross_axis_size) - 1)
        )

        starting_cross_axis_coords = self.center[1 - self.layout_params.direction] - 0.5 * content_dimensions[1]
        for row_index, row in enumerate(gridded_elements):
            starting_axis_coords = self.center[self.layout_params.direction] - 0.5 * (sum([element.rect[2 + self.layout_params.direction] for element in row]) + self.layout_params.gap[self.layout_params.direction] * (len(row) - 1))

            for element in row:
                new_pos = [0.0, 0.0]
                new_pos[self.layout_params.direction] = starting_axis_coords
                new_pos[1 - self.layout_params.direction] = starting_cross_axis_coords + 0.5 * max_cross_axis_size[row_index] - 0.5 * element.rect[3 - self.layout_params.direction]
                element.set_rect(new_pos + element.rect[:2])
                starting_axis_coords += element.rect[2 + self.layout_params.direction] + self.layout_params.gap[self.layout_params.direction]
            starting_cross_axis_coords += max_cross_axis_size[row_index] + self.layout_params.gap[1 - self.layout_params.direction]