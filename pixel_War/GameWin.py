import game_framework
from pico2d import *
import title_state

name = "GameWin"
image = None
btnImage1 = None
running = True
x=0
y=0
def enter():
    global image
    global Bgm
    Bgm = load_music('Sound\\Game_win.wav')
    Bgm.play()
    image = load_image('Graphics\\GameWin.png')
def exit():
    global image
    global Bgm
    del Bgm
    del image

def handle_events():
    global running
    global x,y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if (event.key,event.type) == (SDLK_ESCAPE,SDL_KEYDOWN):
            game_framework.change_state (title_state)
def draw():
    clear_canvas()
    image.draw(350,350)
    update_canvas()
def update():
    pass
def pause():
    pass
def resume():
    pass






