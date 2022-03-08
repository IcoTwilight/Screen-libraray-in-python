import screen
import time
screen.base_font = screen.pygame.font.Font("unifont.ttf", 13)

i = 0

while (1):
    i += 1
    screen.say(str(i) + "\n")
    screen.CAPTION = f"{str(i)}:{str(screen.DT)}"
    screen.update()

for i in range(1000):
    screen.say(str(i) + "\n")
screen.update()
