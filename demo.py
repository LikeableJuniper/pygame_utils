# A small demo program showcasing default styles and elements
import pygame as pg

from pygame_utils_likeablejuniper import Border
from pygame_utils_likeablejuniper import Container, ContainerStyle, VerticalLayout, HorizontalLayout
from pygame_utils_likeablejuniper import StaticLabel, LabelStyle
from pygame_utils_likeablejuniper import Button
from pygame_utils_likeablejuniper import Input

pg.init()
pg.font.init()
screen = pg.display.set_mode((800, 800))

root_style = ContainerStyle(border=Border(5, (255, 0, 0)))
row_style = ContainerStyle(border=Border(5, (0, 255, 0)))

root = Container([0, 0, 800, 800], VerticalLayout(), style=root_style)

title_row = Container([0, 0, 800, 100], HorizontalLayout(), style=row_style)
title_row.add(StaticLabel([0, 0, 500, 50], "Pygame Utils", LabelStyle(font=pg.font.SysFont("Mono", 50))))
root.add(title_row)

first_row = Container([0, 0, 800, 100], HorizontalLayout(), style=row_style)
first_row.add(StaticLabel([0, 0, 200, 50], "Hello Label"))
first_row.add(Button([0, 0, 200, 50], "Hello Button"))
root.add(first_row)

second_row = Container([0, 0, 800, 100], HorizontalLayout(), style=row_style)
second_row.add(Input([0, 0, 200, 50], "Input"))
root.add(second_row)

running = True
while running:
    screen.fill((100, 100, 100))

    root.draw(screen)

    events = pg.event.get()

    root.update(events)
    
    for event in events:
        if event.type == pg.QUIT:
            running = False

    pg.display.flip()

pg.quit()
