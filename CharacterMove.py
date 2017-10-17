from pico2d import *

def handle_events():
    global running
    global right
    global left
    global up
    global down
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key==SDLK_RIGHT:
                right = True
                left = False
                up = False
                down = False
            elif event.key == SDLK_LEFT:
                right = False
                left = True
                up = False
                down = False
            elif event.key == SDLK_DOWN:
                right = False
                left = False
                up = False
                down = True
            elif event.key ==SDLK_UP:
                right = False
                left = False
                up = True
                down = False
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            right,down,up,left=False,False,False,False

open_canvas()
character = load_image('Character.png')
grass = load_image('Grass.png')
right = False
left = False
up = False
down = False
running = True

x = 400
y=0
dir=1
frame = 0
while (running):
    clear_canvas()
    for n in range(0,17):
        for m in range(0, 13):
            grass.clip_draw(0,0,50,50,n*50,m*50)
    if dir==1:
        character.clip_draw(frame * 100, 100, 100, 100, x, 100+y,50,50)
    elif dir==2:
        character.clip_draw(frame * 100, 200, 100, 100, x, 100+y,50,50)
    elif dir==3:
        character.clip_draw(frame * 100, 0, 100, 100, x, 100+y,50,50)
    elif dir==4:
        character.clip_draw(frame * 100, 300, 100, 100, x, 100+y,50,50)
    update_canvas()
    if right==True and left==False and up == False and down==False:
        dir = 1
        x+=5
    elif right==False and left==True and up == False and down==False:
        dir = 2
        x-=5
    elif right==False and left==False and up == True and down==False:
        dir = 3
        y+=5
    elif right==False and left==False and up == False and down==True:
        dir = 4
        y-=5
    frame =  (frame + 1) % 3
    delay(0.05)
    handle_events()

close_canvas()