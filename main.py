import pygame as pg
from pygame_utils_likeablejuniper import Container, Label

pg.init()
pg.font.init()
screen = pg.display.set_mode((800, 800))
main_font = pg.font.SysFont("Mono", 20)

test_container = Container()
test_container.add(Label([10, 10, 200, 50], main_font.render("Hallo", True, (0, 0, 0))))

running = True

while running:
    screen.fill((100, 100, 100))

    test_container.draw(screen)

    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
