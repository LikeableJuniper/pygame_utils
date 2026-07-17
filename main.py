import pygame as pg
from pygame_utils_likeablejuniper import Container, Label
from pygame_utils_likeablejuniper.component.label import LabelStyle

pg.init()
pg.font.init()
screen = pg.display.set_mode((800, 800))
main_font = pg.font.SysFont("Mono", 20)

test_container = Container()
custom_style = LabelStyle(background_color=(255, 0, 0))
label = Label([10, 10, 200, 50], "Hello", custom_style)
test_container.add(label)
test_container.add(Label([220, 10, 200, 50], "Other Hello"))

running = True

while running:
    screen.fill((100, 100, 100))

    test_container.draw(screen)

    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
