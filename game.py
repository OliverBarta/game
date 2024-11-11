import pygame as pg

print("d")

pg.init()

WIDTH = 500

HEIGHT = 500

colourbg = [0,110,200]
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("TBD")
screen.fill(colourbg)
x = 250
change = 1
while True:
    x = x+change
    if x >= 250:
        change = -1
    elif x <= 20:
        change = 1
    screen.fill(colourbg)
    pg.draw.circle(screen, (240,240,240), (x,250), 30)
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.exit()
