import pygame as pg
from pygame_utils_likeablejuniper import Container
from pygame_utils_likeablejuniper import LabelStyle, StaticLabel
from pygame_utils_likeablejuniper import ContainerStyle
from pygame_utils_likeablejuniper import Border
from pygame_utils_likeablejuniper import Button, ButtonStyle
from pygame_utils_likeablejuniper.layout.layout import HorizontalLayout, LayoutParams, VerticalLayout


pg.init()
pg.font.init()
screen = pg.display.set_mode((800, 800))
clock = pg.time.Clock()

container_style = ContainerStyle(border=Border(5, (0, 255, 0)))
container = Container([10, 10, 780, 780], layout=VerticalLayout([10, 10, 780, 780]), style=container_style)
custom_style = LabelStyle(background_color=(255, 0, 0))
label = StaticLabel([20, 20, 200, 50], "Hello", custom_style)
container.add(label)
container.add(StaticLabel([240, 20, 200, 50], "Other Hello"))

button = Button([20, 100, 200, 50], "Click me", on_click=lambda: print("Clicked"))
container.add(button)

conditional_label = StaticLabel([240, 100, 200, 50], "Cond")
conditional_label.add_conditional_style(
    lambda label: len(label.text) > 5,
    LabelStyle(background_color=(0, 255, 0), text_color=(0, 0, 0), font=pg.font.SysFont("Mono", 20))
)
counter = 0
conditional_label.add_conditional_style(
    lambda label: counter % 2 == 0,
    LabelStyle(background_color=(0, 0, 255), text_color=(255, 255, 255), font=pg.font.SysFont("Mono", 20))
)
container.add(conditional_label)

running = True

frame_counter = 0
changes = 0

while running:
    screen.fill((100, 100, 100))

    container.draw(screen)
    container.update(pg.event.get())

    pg.display.flip()

    clock.tick(60)

    frame_counter += 1

    if frame_counter >= 60:
        frame_counter = 0
        changes += 1
        changes %= 3
        # runtime value and style changes
        if len(label.text) < 10:
            label.set_text(label.text + "o")
            button.set_text(button.text + "o")
        
        #conditional_label.set_text(conditional_label.text + "o")
        #if len(conditional_label.text) > 7:
        #    conditional_label.set_text("Cond")
        counter += 1
        
        new_color = [0, 0, 0]
        new_color[changes] = 255
        label.update_style(LabelStyle(background_color=new_color))
        button.conditional_styles.clear()
        button.add_conditional_style(
            lambda button: button.hovered,
            ButtonStyle(border=Border(5, new_color))
        )

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
