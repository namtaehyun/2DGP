# hero_controller.py : control hero move with left and right key

import random
from pico2d import *

running = None
hero = None

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


class Hero:
    image = None

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND= 0, 1, 2, 3


    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.runstate = self.RIGHT_RUN
        self.state = self.RIGHT_STAND
        self.HeightDir = 1
        self.keydown = False
        self.LRkeydown = False
        self.LRrest = 1
        self.Dash = False

        if Hero.image == None:
            Hero.image = load_image('animation_sheet.png')

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.LRkeydown = True
            self.LRrest = 2
            if self.state in (self.RIGHT_STAND,self.LEFT_STAND):
                self.state = self.LEFT_RUN
            elif self.state in (self.RIGHT_RUN,):
                self.state = self.LEFT_RUN

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.LRkeydown = True
            self.LRrest = 3
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND):
                self.state = self.RIGHT_RUN
            elif self.state in (self.LEFT_RUN,):
                self.state = self.RIGHT_RUN

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            self.keydown = True
            self.HeightDir = 1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            self.keydown = True
            self.HeightDir = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            self.Dash = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_SPACE):
            self.Dash = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,):
                self.LRkeydown = False
                self.state = self.LEFT_STAND

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN,):
                self.LRkeydown = False
                self.state = self.RIGHT_STAND

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            self.keydown = False
            self.HeightDir = 1

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            self.keydown = False
            self.HeightDir = 0

    def update(self):
        print(self.Dash)
        self.frame = (self.frame+1)%8
        if self.state==self.RIGHT_RUN:
            self.runstate=self.RIGHT_RUN
            self.x = min(800,self.x+5)
            if(self.Dash==True):
                self.x = min (800, self.x + 5)
            if(self.HeightDir==1 and self.keydown == True):
                self.y = min (600, self.y + 5)
                if(self.Dash==True):
                    self.y = min (600, self.y + 5)
            elif(self.HeightDir==0 and self.keydown == True):
                self.y = max (0, self.y - 5)
                if(self.Dash==True):
                    self.y = max (0, self.y - 5)
        elif self.state == self.LEFT_RUN:
            self.runstate=self.LEFT_RUN
            self.x = max(0,self.x-5)
            if(self.Dash==True):
                self.x = max (0, self.x - 5)
            if(self.HeightDir==1 and self.keydown == True):
                self.y = min (600, self.y + 5)
                if(self.Dash==True):
                    self.y = min (600, self.y + 5)
            elif(self.HeightDir==0 and self.keydown == True):
                self.y = max (0, self.y - 5)
                if(self.Dash==True):
                    self.y =max (0, self.y - 5)
        elif (self.LRkeydown == False and self.keydown ==True):
            if(self.HeightDir==1 and self.keydown == True):
                self.y = min (600, self.y + 5)
                if(self.Dash==True):
                    self.y = min (600, self.y + 5)
            elif(self.HeightDir==0 and self.keydown == True):
                self.y = max (0, self.y - 5)
                if(self.Dash==True):
                    self.y = max (0, self.y - 5)
        pass

    def draw(self):
        if(self.LRkeydown==True):
            self.image.clip_draw(self.frame * 100, self.state * 100, 100, 100, self.x, self.y)
        elif(self.LRkeydown==False and self.keydown==True):
            self.image.clip_draw(self.frame * 100, self.runstate * 100, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, self.LRrest * 100, 100, 100, self.x, self.y)


def handle_events():
    global running
    global hero
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            hero.handle_event(event)
def main():

    open_canvas()

    global hero
    global running

    hero = Hero()
    grass = Grass()

    running = True
    while running:
        handle_events()

        hero.update()

        clear_canvas()
        grass.draw()
        hero.draw()
        update_canvas()

        delay(0.04)

    close_canvas()


if __name__ == '__main__':
    main()