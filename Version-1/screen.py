def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

install_and_import("pygame")
import sys
from datetime import date
from datetime import datetime
install_and_import("threading")
install_and_import("clipboard")

pygame.init()

Qu=""

POINTER=0

STARED=False

TEXT_SIZE=12
TEXT_FONT = pygame.font.Font("consola.ttf", TEXT_SIZE)
COLOUR=(0, 0, 0)

QUERY=[]
QUERY_POINTER=-1

FPS=60

WINDOW_H=500
WINDOW_W=720
WINDOW = pygame.display.set_mode([WINDOW_W, WINDOW_H])

INPUT_BOX_W=140
INPUT_BOX_H=20
INPUT_BOX_X=5
INPUT_BOX_Y=WINDOW_H-(INPUT_BOX_H+5)
INPUT_BOX_T = ''
INPUT_BOX = pygame.Rect(INPUT_BOX_X, INPUT_BOX_Y, INPUT_BOX_W, INPUT_BOX_H)

SCREEN_L=37
SCREEN_X=0
SCREEN_Y=0
SCREEN_W=100
SCREEN_H=(TEXT_SIZE*SCREEN_L)+10
SCREEN_T=[""] * SCREEN_L
#SCREEN_T="HEY"
SCREEN=pygame.Rect(SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H)

clock = pygame.time.Clock()

color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive

II=0

###FILE_FUNCTIONS###
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    global INPUT_BOX_T, POINTER, SCREEN_L
    text="\n".join(text)
    text=text.split("\n")
    while len(text)>SCREEN_L:
        text.pop(0)
    text= [str(date.today())+" "*10+str(datetime.now().strftime("%H:%M:%S"))] + text
    text="\n".join(text)
    words = [word.split('\n') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def update():
    global INPUT_BOX_T, II, POINTER, Qu, STARED
    stared=STARED
    input_box_t=INPUT_BOX_T
    if stared==True:
        input_box_t="*"*len(input_box_t)
        
    input_box_t=Qu+input_box_t
    if II<=25:
        input_box_t=input_box_t[:POINTER+len(Qu)]+"█"+input_box_t[POINTER+1+len(Qu):]
        
    WINDOW.fill((255, 255, 255))
    pygame.draw.rect(WINDOW, color, INPUT_BOX)

    #color
    INPUT_BOX_SURFACE = TEXT_FONT.render(input_box_t, True, (255, 255, 255))
    WINDOW.blit(INPUT_BOX_SURFACE, (INPUT_BOX.x+5, INPUT_BOX.y+3))
    blit_text(WINDOW, SCREEN_T, (5, 5), TEXT_FONT, COLOUR)
    
    INPUT_BOX.w = max(100, INPUT_BOX_SURFACE.get_width()+10)
    pygame.display.flip()
    clock.tick(FPS)

def keys():
    global INPUT_BOX_T
    global QUERY, QUERY_POINTER, POINTER
    
    if POINTER>len(INPUT_BOX_T):
        POINTER=len(INPUT_BOX_T)
    elif POINTER<0:
        POINTER=0
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if POINTER!=0:
                    INPUT_BOX_T = INPUT_BOX_T[:POINTER-1]+INPUT_BOX_T[POINTER:]
                    POINTER = POINTER - 1
                else:
                    INPUT_BOX_T = INPUT_BOX_T[1:]

            elif event.key == pygame.K_RIGHT:
                POINTER = POINTER + 1
                if POINTER>len(INPUT_BOX_T):
                    POINTER=len(INPUT_BOX_T)
                elif POINTER<0:
                    POINTER=0

            elif event.key == pygame.K_LEFT:
                POINTER = POINTER - 1
                if POINTER>len(INPUT_BOX_T):
                    POINTER=len(INPUT_BOX_T)
                elif POINTER<0:
                    POINTER=0
                    
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                return

            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                CLIP=clipboard.paste()
                if INPUT_BOX_T!="":
                    INPUT_BOX_T=INPUT_BOX_T[0:POINTER]+CLIP+INPUT_BOX_T[POINTER:]
                    POINTER += len(CLIP)
                else:
                    INPUT_BOX_T += CLIP
                    POINTER += len(CLIP)

            elif event.key == pygame.K_RETURN:
                run=False
                if INPUT_BOX_T != "":
                    QUERY.append(INPUT_BOX_T)
                    QUERY_POINTER +=1
                T=INPUT_BOX_T
                INPUT_BOX_T=""
                return T
            else:
                if event.key != pygame.K_RETURN:
                    if INPUT_BOX_T!="":
                        INPUT_BOX_T=INPUT_BOX_T[0:POINTER]+event.unicode+INPUT_BOX_T[POINTER:]
                        POINTER += 1
                    else:
                        INPUT_BOX_T += event.unicode
                        POINTER += 1

def thread_say(text):
    global SCREEN_T
    SCREEN_T.pop(0)
    SCREEN_T.append(text)
    update()

###CALLABLE_FUNCTIONS###

def set(loc, text):
    global SCREEN_T
    SCREEN_T[loc]=text
    update()

def say(text):
    t1 = threading.Thread(target=thread_say, args=(text,))
    t1.start()

def ask(Q="", display=True, stared=False):
    global INPUT_BOX_T, II, Qu, STARED
    STARED=stared
    Qu=Q
    run=True
    while run:
        T=keys()
        if T != None:
            if display==True:
                if stared==False:
                    say(Q+T)
                else:
                    say(Q+"*"*len(T))
            return T
        if II<=50:
            II=II+1
        else:
            II=1
        update()

def clear(screen=True, input_box=True):
    global SCREEN_T, INPUT_BOX_T
    if screen:
        SCREEN_T=[""]*len(SCREEN_T)
    if input_box:
        INPUT_BOX_T=""

def quit():
    pygame.quit()


keys()
update()


print("Screen up and running")
