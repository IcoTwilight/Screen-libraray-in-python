import screen
import time
screen.base_font = screen.pygame.font.Font("unifont.ttf", 13)

j = 0

while (1):
    for i in range(100):
        screen.say(str(i+(j*100)) + "\n")
        screen.CAPTION = f"{str(i+(j*100))}:{str(screen.DT)}"
    screen.update()
    j +=1
