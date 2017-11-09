import game_framework
from pico2d import *
import main_state
import main_state2
import Sound_Manager
name = "TitleState"
image = None
btnImage1 = None
btnImage2 = None
running = True
x=0
y=0
def enter():
    global image
    global btnImage2
    global btnImage1
    global bgm
    image = load_image('Start_Scene.png')
    btnImage1 = load_image('Normal_mode.png')
    btnImage2 = load_image('Hell_mode.png')
def exit():
    global image
    global btnImage2
    global btnImage1
    del(btnImage1)
    del(btnImage2)
    del(image)

def handle_events():
    global running
    global x,y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type,event.key)==(SDL_KEYDOWN,SDLK_ESCAPE):
                running = False
            elif event.type == SDL_MOUSEMOTION:
                x, y = event.x, 700 - event.y
            if event.type == SDL_MOUSEBUTTONDOWN:
                if x>260 and x<440 and y>70 and y<130: #stage 1 노말모드
                   game_framework.change_state (main_state)
                elif x>260 and x<440 and y>170 and y<230: #stage 2 헬모드
                   game_framework.change_state (main_state2)
def draw():
    clear_canvas()
    image.draw(350,350)
    btnImage1.draw(350,100)
    btnImage2.draw(350,200)
    update_canvas()







def update():
    if not running:
        game_framework.quit()


def pause():
    pass


def resume():
    pass






