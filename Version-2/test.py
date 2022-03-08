import screen
import time
screen.base_font = screen.pygame.font.Font("unifont.ttf", 13)
screen.FPS = 100
while (1):
    for i in range(1000):
        screen.say(str(i) + "\n")
        screen.CAPTION = f"{str(i)}:{str(screen.DT)}"
        screen.update()
    for i in range(3000):
        screen.purge(2)
        screen.CAPTION = f"{str(i)}:{str(screen.DT)}"
        screen.update()
