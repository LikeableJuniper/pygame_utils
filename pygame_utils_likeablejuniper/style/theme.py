from pygame_utils_likeablejuniper.style.style import Style

class Theme:
    def __init__(self, styles: list[Style] | None = None):
        self.styles = styles or []
    
    def apply(self):
        for style in self.styles:
            style.apply()

class Themes:
    ...