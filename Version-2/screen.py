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
install_and_import("sys")
install_and_import("time")
install_and_import("threading")
install_and_import("clipboard")
from pygame.locals import *

pygame.init()
pygame.font.init()

CAPTION = "test"
MAX = 250

flags = HWSURFACE|DOUBLEBUF|RESIZABLE
bpp = 8
pygame.display.set_caption(CAPTION)
WINDOW = pygame.display.set_mode((400, 400), flags, bpp)
WINDOW.set_alpha(None)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])

clock = pygame.time.Clock()
ALL = pygame.sprite.Group()
keys = pygame.key.get_pressed()
base_font = pygame.font.Font(None, 20)

SCREEN_TEXT = ''
INPUT_TEXT = ''
scroll_height = 0
scroll_speed = 30

POINTER = 0

class _colors_:
    def __init__(self):
        self.screen_background = (50, 50, 50)
        self.input_background = (100, 100, 100)
        self.text_color = (200, 200, 200)
        

class _sprite_(pygame.sprite.Sprite):
    def __init__(self, surface):
        self.surf = surface
        self.rect = self.surf.get_rect()
        self.draw_area = [self.rect]
        pygame.sprite.Sprite.__init__(self, ALL)
        
    def move(self, pos, size):
        self.draw_area = [self.rect]
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect.w = size[0]
        self.rect.h = size[1]
        self.surf = pygame.transform.scale(self.surf, (self.rect.w, self.rect.h))
        self.draw_area.append(self.rect)

colors = _colors_()
SCREEN=_sprite_(pygame.Surface([50, 50]))
INPUT =_sprite_(pygame.Surface([50, 50]))

def blit_text(surface, text, pos, font, pointer = None, color=pygame.Color('black')):
    unix = int(time.time())
    pointed = False
    text = [word.split('\n') for word in text.splitlines()]  # 2D array where a row is a list of lines.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for k, line in enumerate(text):
        for j, word in enumerate(line):
            word = word + " "
            for i, letter in enumerate(word):
                #print(i, pointer)
                if i+j+k == pointer:
                    #if (unix % 2) == 0:
                    letter = "_"
                    pointed = True
                letter_surface = font.render(letter, 0, color)
                letter_width, letter_height = letter_surface.get_size()
                surface.blit(letter_surface, (x, y))
                x += letter_width
        x = pos[0]  # Reset the x.
        y += letter_height  # Start on new row.

def render_texts(text):
    blit_text(SCREEN.surf, str(SCREEN_TEXT), (10, 10 + scroll_height), base_font, None, colors.text_color)
    blit_text(INPUT.surf, str(text) + str(INPUT_TEXT), (10, 10), base_font, POINTER+len(text), colors.text_color)

def keys(ACTIVE):
    global INPUT_TEXT, POINTER, scroll_height, scroll_speed

    if POINTER>len(INPUT_TEXT):
        POINTER=len(INPUT_TEXT)
    elif POINTER<0:
        POINTER=0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scroll_height += scroll_speed
            elif event.button == 5:
                scroll_height -= scroll_speed
                
        if ACTIVE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if POINTER!=0:
                        INPUT_TEXT = INPUT_TEXT[:POINTER-1]+INPUT_TEXT[POINTER:]
                        POINTER = POINTER - 1
                    else:
                        INPUT_TEXT = INPUT_TEXT[1:]

                elif event.key == pygame.K_RIGHT:
                    POINTER = POINTER + 1
                    if POINTER>len(INPUT_TEXT):
                        POINTER=len(INPUT_TEXT)
                    elif POINTER<0:
                        POINTER=0

                elif event.key == pygame.K_LEFT:
                    POINTER = POINTER - 1
                    if POINTER>len(INPUT_TEXT):
                        POINTER=len(INPUT_TEXT)
                    elif POINTER<0:
                        POINTER=0
                        
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    pass

                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    CLIP=clipboard.paste()
                    if INPUT_TEXT!="":
                        INPUT_TEXT=INPUT_TEXT[0:POINTER]+CLIP+INPUT_TEXT[POINTER:]
                        POINTER += len(CLIP)
                    else:
                        INPUT_TEXT += CLIP
                        POINTER += len(CLIP)

                else:
                    if event.unicode != "\r":
                        if INPUT_TEXT!="":
                            INPUT_TEXT=INPUT_TEXT[0:POINTER]+event.unicode+INPUT_TEXT[POINTER:]
                            POINTER += 1
                        else:
                            INPUT_TEXT += event.unicode
                            POINTER += 1
                    else:
                        return False
    return True

def prepare():
    global scroll_height
    screen_w, screen_h = pygame.display.get_surface().get_size()
    SCREEN.move((0, 0), (screen_w, screen_h-50))
    SCREEN.surf.fill(colors.screen_background)
    INPUT.move((0, screen_h-50), (screen_w, 50))
    INPUT.surf.fill(colors.input_background)

def update(text = "", fps=120, ACTIVE = False):
    pygame.display.set_caption(CAPTION)
    x = keys(ACTIVE)
    prepare()
    WINDOW.fill((0, 0, 0))
    render_texts(text)
    for i in ALL: #get all the objects
        WINDOW.blit(i.surf, (i.rect.x, i.rect.y))
    pygame.display.update()
    clock.tick(fps)
    return x

def ask(text):
    global INPUT_TEXT
    while update(text, 120, True):
        pass
    INPUT_TEXT2 = INPUT_TEXT
    INPUT_TEXT = ""
    return INPUT_TEXT2

def say(text):
    text = str(text)
    global SCREEN_TEXT
    SCREEN_TEXT += text

def clear():
    global SCREEN_TEXT
    SCREEN_TEXT = ""

def quit():
    pygame.quit()
    sys.exit()

update()
