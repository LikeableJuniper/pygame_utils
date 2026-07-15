import pygame as pg
import pygame_utils_likeablejuniper as pgu

pg.init()
screen = pg.display.set_mode((800, 800))

running = True

while running:
    screen.fill((100, 100, 100))

    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
