import game_framework
from pico2d import *
import title_state

name = "StartState"
image = None
logo_time = 0.0

def enter():
    global image
    open_canvas(700,700)
    image = load_image('Graphics\\kpu_credit.png')
    #enter후에는 handle_event를 호출한다.
def exit():
    global image
    del(image)
    close_canvas()

def update():
    global logo_time
    logo_time
    if(logo_time>1.0):
        logo_time = 0
        #game_framework.quit()
        game_framework.push_state(title_state)
        #push_state는 현재상태를 저장하고 다음상태로 넘어간다.
        #change_state는 상태를 저장하지 않고 다음 상태로 넘어간다.
    delay(0.1)
    logo_time+=0.05

def draw():
    global image
    clear_canvas()
    image.draw(350,350)
    update_canvas()

def handle_events():
    events = get_events()
    #다음에 update를 호출한다.


def pause(): pass
    # 현재 state에서 남겨주고 싶은 것들을 처리한다. 저장해야 할 것들.

def resume(): pass




