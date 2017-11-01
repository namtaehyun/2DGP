import random
import json
import os

from pico2d import *

import game_framework
import title_state

name = "MainState2"

class Field:
    img = None
    def __init__(self,x,y,state):
        self.x = x
        self.y = y
        self.state = state
        if Field.img == None:
            Field.image1 = load_image('grass.png')
            Field.image2 = load_image('road.png')
    def draw(self):
        if self.state == 1:
            self.image1.draw(self.x, self.y)
        else:
            self.image2.draw(self.x,self.y)
    def Change(self,state):   #바닥의 상태를 바꿔준다.
        self.state = state

class Character:
    image = None
    attackimage = None
    attack = False
    bullet=[]
    def __init__(self):
        self.x, self.y = 90, 90
        self.attackframe=0
        self.frame = 0
        self.idle = True
        self.dir = 0
        self.attackdir=0
        if Character.image == None:
            Character.image = load_image('Character.png')
            Character.attackimage = load_image('attack.png')
    def update(self):
        if(self.attack==True):
            self.attackframe += 1
            if (self.attackframe > 3):
                self.attackframe = 0
                self.attack = False

        if(self.idle==False):
            self.frame = (self.frame + 1) % 4
            if(self.dir==0):
                self.y += 5
                if(self.y>575):
                    self.y-=5
            elif(self.dir==150):
                self.y-=5
                if(self.y<-75):
                    self.y+=5
            elif(self.dir==100):
                self.x-=5
                if(self.x<25):
                    self.x+=5
            elif(self.dir==50):
                self.x+=5
                if(self.x>675):
                    self.x-=5
    def IDLE(self):
        self.idle = True
    def ATTACK(self):
        self.attack=True
    def UP_GO(self):
        self.dir = 0
        self.attackdir = 100
        self.idle = False
    def DOWN_GO(self):
        self.dir = 150
        self.attackdir = 0
        self.idle = False
    def LEFT_GO(self):
        self.dir = 100
        self.attackdir = 50
        self.idle = False
    def RIGHT_GO(self):
        self.dir = 50
        self.attackdir = 150
        self.idle = False
    def draw(self):
        if(self.attack==True):
            self.attackimage.clip_draw (self.attackdir,self.attackframe * 50, 50, 50, self.x, 100 + self.y, 50, 50) #up
            # (left, bottom, width, height, x, y)
        else:
            self.image.clip_draw (self.frame * 50, self.dir, 50, 50, self.x, 100 + self.y, 50, 50) #up

def enter():
    global FieldSet
    global character
    character = Character()
    FieldSet = []
    for i in range (0, 14):
        for j in range (0, 14):
            FieldSet.append (Field(i * 50 + 25, j * 50 + 25, 1))

def exit():
    global character
    global FieldSet
    del(character)
    del(FieldSet)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            Character.LEFT_GO(character)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
            Character.RIGHT_GO(character)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
            Character.UP_GO(character)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            Character.DOWN_GO(character)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            Character.ATTACK(character)
        elif event.type == SDL_KEYUP:
            Character.IDLE(character)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)

def update():
    character.update()


def draw():
    global FieldSet
    clear_canvas()
    for F in FieldSet:
        F.draw()
    character.draw()
    update_canvas()
    delay(0.05)





