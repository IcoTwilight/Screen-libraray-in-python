#import the library
import screen
#set the font
screen.base_font = screen.pygame.font.Font("unifont.ttf", 13)
screen.say("Python screen eval test, type [exit] to exit\n")
while(1):
    #ask for input, this will also call update()
    I = screen.ask(">>>")
    #set the title of the window to the input
    screen.CAPTION = str(I)
    
    if I == "quit":
        #quit
        screen.quit()
        
    #display the text to the output
    screen.say(I+"\n")
    #call update to display the screen.
    screen.update()
    
    if I == "clear":
        #clear the screen
        screen.clear()
    elif I == "purge":
        A = screen.ask("Amount?>>>")
        #remove A letters from the screen
        screen.purge(int(A))
