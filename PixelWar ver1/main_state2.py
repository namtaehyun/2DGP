import random
import json
import os

from pico2d import *

import GameWin
import game_framework
import title_state
import GameOver

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
    def ReturnState(self):
        return self.state

class Home:
    hpimage1 = None
    hpimage2 = None
    image = None
    def __init__(self):
        self.hp = 1000
        self.x = 650
        self.y = 400
        if Home.hpimage1 == None:
            Home.hpimage1 = load_image ('healthStatusBar.png')
            Home.hpimage2 = load_image ('healthStatusBar1.png')
        if Home.image == None:
            Home.image = load_image('home.PNG')
    def update(self):
        for M in monsterSet:
            if M.attack==True and M.attackframe>7 and math.sqrt((M.x-self.x)*(M.x-self.x)+(M.y-self.y)*(M.y-self.y))<50 and M.death==False:
                self.hp-=5
        if self.hp<0:
            game_framework.push_state(GameOver)
    def draw(self):
        self.hpimage2.draw (self.x, self.y + 100, 100, 20)
        self.hpimage1.draw (self.x + (100 - self.hp / 10) / 2, self.y + 100, self.hp / 10, 20)
        self.image.draw(self.x,self.y,150,150)


class Monster:
    PIXEL_PER_METER = (10.0 / 0.3)  # pixel/meter 10픽셀에 30센치미터.
    RUN_SPEED_KMPH = 10.0  # km/h
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    TIME_PER_ACTION = 0.5
    image = None
    attackImage =None
    RIGHT_RUN,UP_RUN, DOWN_RUN = 1,0,3
    def __init__(self,state):
        self.hp = 0
        self.state = state
        self.damage = 5
        self.attack = False
        self.frame = 0
        self.attackframe=0
        self.speed = 5
        self.x,self.y =25,275
        self.death= False
        self.xdir =0
        self.ydir=0
        self.bloodtime=0
        self.movestate = self.RIGHT_RUN
        if self.state == 0:
            self.hp = 100
            self.image=load_image('pig.png')
            self.attackImage = load_image('Monster_attack2.png')
        elif self.state == 1:
            self.hp = 150
            self.image =load_image('trash.png')
            self.attackImage = load_image('Monster_attack1.png')
        elif self.state == 2:
            self.hp = 200
            self.image =load_image('nohead.png')
            self.attackImage = load_image('Monster_attack.png')
    def update(self,frame_time):
        distance = Monster.RUN_SPEED_PPS * frame_time
        if(self.attack==False):
            self.x += (self.xdir * distance)
            self.y += (self.ydir * distance)
        if self.death==False:
            if character.skillstate == 1 and character.skillGo == True and math.sqrt((character.m_x-self.x)*(character.m_x-self.x)+(character.m_y-self.y)*(character.m_y-self.y))<100\
                    and character.skillframe>6:
                self.hp -= 50
            if character.skillstate == 2 and character.skillGo == True and math.sqrt((character.m_x-self.x)*(character.m_x-self.x)+(character.m_y-self.y)*(character.m_y-self.y))<100:
                self.speed = 2
                self.damage = 1
            else:
                self.speed = 5
                self.damage =5
            if(self.attack==True):
                self.attackframe += 1
                if (self.attackframe > 10):
                    self.attackframe = 0
                    self.attack = False
            if math.sqrt((self.x-character.x)*(self.x-character.x)+(self.y-character.y)*(self.y-character.y))<50 or \
                            math.sqrt((self.x-home.x)*(self.x-home.x)+(self.y-home.y)*(self.y-home.y))<50:
                self.attack=True
            else:
                self.attack=False

            if self.attack==False:
                self.frame = (self.frame + 1) % 4
                if(self.movestate==self.RIGHT_RUN):
                    self.xdir = 1
                    self.ydir=0
                if(self.movestate==self.UP_RUN):
                    self.ydir=1
                    self.xdir=0
                if(self.movestate==self.DOWN_RUN):
                    self.ydir=-1
                    self.xdir=0
                if(self.movestate==self.RIGHT_RUN and FieldSet[int((self.x-25)/50)+1][int((self.y-25)/50)].state==1):
                    if(FieldSet[int((self.x-25)/50)][int((self.y-25)/50)+1].state==1):
                        self.movestate = self.DOWN_RUN
                    elif(FieldSet[int((self.x-25)/50)][int((self.y-25)/50)-1].state==1):
                        self.movestate = self.UP_RUN
                elif(self.movestate==self.DOWN_RUN and FieldSet[int((self.x-25)/50)][int((self.y-25)/50)-1].state==1):
                    self.movestate = self.RIGHT_RUN
                elif(self.movestate==self.UP_RUN and FieldSet[int((self.x-25)/50)][int((self.y-25)/50)+1].state==1):
                    self.movestate = self.RIGHT_RUN
            else:
                pass

            if math.sqrt((self.x-character.x)*(self.x-character.x)+(self.y-character.y)*(self.y-character.y))<50:
                if character.attackdir==3 and character.attack==True and character.attackframe>2:
                    if (FieldSet[int ((self.x - 25) / 50)+1][int ((self.y - 25) / 50)].state == 0):
                        self.hp-= character.damage
                elif character.attackdir==1 and character.attack==True and character.attackframe>2:
                    if (FieldSet[int ((self.x - 25) / 50)][int ((self.y - 25) / 50)].state == 0):
                        self.hp -= character.damage
                elif character.attackdir== 2 and character.attack==True and character.attackframe>2:
                    if (FieldSet[int ((self.x - 25) / 50)][int ((self.y - 25) / 50)+1].state == 0):
                        self.hp -= character.damage
                elif character.attackdir == 0 and character.attack==True and character.attackframe>2:
                    if (FieldSet[int ((self.x - 25) / 50)][int ((self.y - 25) / 50)].state == 0):
                        self.hp -= character.damage
        else:
            pass
        if self.hp<0:
            self.bloodtime+=1
            self.death = True
    def draw(self):
        if self.death==False:
            self.image.clip_draw (self.frame * 50, self.movestate* 50, 50, 50, self.x, self.y, 50, 50)
            if self.attack==True:
                self.attackImage.clip_draw(self.attackframe*50,0,50,50,self.x,self.y)
        else:
            self.image = load_image('Blood.png')
            self.image.draw(self.x,self.y)
            if(self.bloodtime>50):
                monsterSet.remove(self)
                character.money+=30

class Character:
    global monsterSet
    global turret
    PIXEL_PER_METER = (10.0 / 0.3)  # pixel/meter 10픽셀에 30센치미터.
    RUN_SPEED_KMPH = 10.0  # km/h
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    TIME_PER_ACTION = 0.5
    buffOnimage = None
    image = None
    hpimage1 = None
    hpimage2 = None
    attackimage = None
    attack = False
    ringimage = None
    SkillImage1 = None
    SkillImage2 = None
    cursorimage = None
    buffimage = None
    LEFT_RUN,LEFT_STAND, RIGHT_RUN, RIGHT_STAND,UP_RUN,UP_STAND,DOWN_RUN,DOWN_STAND = 2,6,1,5,0,4,3,7 #STAND = GO_STATE+4
    def __init__(self):
        self.m_x,self.m_y = 0,0
        self.x, self.y = 625,300
        self.skillstate = 0
        self.skillframe= 0
        self.icetime=0
        self.buffOn = False
        self.money = 0
        self.buffTime = 0
        self.buffcoolTime = 0
        self.buffOn1 = False
        self.skillGo=False #스킬시전
        self.skillcoolOn1 = True
        self.skillcoolOn2 = True
        self.damage = 15
        self.ringOn = False
        self.hp = 1000
        self.frame = 0
        self.attackdir = 0
        self.cool1 = False
        self.buffframe = 0
        self.skillcooltime1 = 0
        self.cool2 = False
        self.skillcooltime2 = 0
        self.turretOn = False
        self.attackframe=0
        self.state = self.DOWN_STAND
        if Character.image == None:
            Character.buffimage = load_image('buff.png')
            Character.ringimage = load_image('SkillRing.png')
            Character.image = load_image ('Character.png')
            Character.attackimage = load_image('attack.png')
            Character.hpimage1 =load_image('healthStatusBar.png')
            Character.hpimage2 =load_image('healthStatusBar1.png')
            Character.SkillImage1 = load_image('Ice_field.png')
            Character.SkillImage2 = load_image ('bomb.png')
            Character.cursorimage = load_image('cursor.png')
            Character.buffOnimage = load_image('BUFF_ON.png')

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION and self.ringOn==True and self.skillGo==False:
            self.m_x, self.m_y = event.x, 700 - event.y
        if event.type == SDL_MOUSEBUTTONDOWN and self.skillstate==1 and self.skillGo==False \
                and math.sqrt((self.x-self.m_x)*(self.x-self.m_x)+(self.y-self.m_y)*(self.y-self.m_y))<150 and self.cool1 == False:
            self.skillGo = True
            self.cool1 = True
            self.skillcoolOn1 = False
        elif event.type == SDL_MOUSEBUTTONDOWN and self.skillstate==2 and self.skillGo==False \
                and math.sqrt ((self.x - self.m_x) * (self.x - self.m_x) + (self.y - self.m_y) * (self.y - self.m_y))< 150 and self.cool2 == False:
            self.skillGo = True
            self.cool2 = True
            self.skillcoolOn2 = False
        elif event.type == SDL_MOUSEBUTTONDOWN and self.turretOn==False and FieldSet[int(self.m_x/50)][int(self.m_y/50)].state==1 \
                and math.sqrt ((self.x - self.m_x) * (self.x - self.m_x) + (self.y - self.m_y) * (
                    self.y - self.m_y)) < 150:
            self.turret = Turret(int(self.m_x/50),int(self.m_y/50))
            self.turretOn = True
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_1) and self.skillGo==False:
            self.ringOn = True
            self.skillstate = 1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2) and self.skillGo==False:
            self.ringOn = True
            self.skillstate = 2
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3) and self.buffOn == False:
            self.buffOn = True
            self.buffOn1 = True
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_4) and self.turretOn ==False and self.money>150:
            self.ringOn=True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_1):
            self.ringOn = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_2):
            self.ringOn = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_4):
            self.ringOn = False
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            self.attackdir = 1
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND,self.UP_STAND,self.DOWN_STAND):
                self.state = self.LEFT_RUN
            elif self.state in (self.RIGHT_RUN,self.UP_RUN,self.DOWN_RUN):
                self.state = self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
            self.attackdir = 3
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND,self.UP_STAND,self.DOWN_STAND):
                self.state = self.RIGHT_RUN
            elif self.state in (self.LEFT_RUN,self.UP_RUN,self.DOWN_RUN):
                self.state = self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
            self.attackdir = 2
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND,self.UP_STAND,self.DOWN_STAND):
                self.state = self.UP_RUN
            elif self.state in (self.RIGHT_RUN,self.LEFT_RUN,self.DOWN_RUN):
                self.state = self.UP_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            self.attackdir = 0
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND,self.UP_STAND,self.DOWN_STAND):
                self.state = self.DOWN_RUN
            elif self.state in (self.LEFT_RUN,self.UP_RUN,self.RIGHT_RUN):
                self.state = self.DOWN_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_a):
            if self.state in (self.LEFT_RUN,):
                self.state = self.LEFT_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_d):
            if self.state in (self.RIGHT_RUN,):
                self.state = self.RIGHT_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_w):
            if self.state in (self.UP_RUN,):
                self.state = self.UP_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_s):
            if self.state in (self.DOWN_RUN,):
                self.state = self.DOWN_STAND
        if (event.type,event.key)==(SDL_KEYDOWN,SDLK_SPACE):
            self.attack = True

    def update(self): #소수점이후로 다 버려버림..
        global FieldSet
        if self.turretOn==True:
            self.turret.update()
        if self.buffOn == True:
            self.buffcoolTime += 1
            self.buffTime += 1
            self.buffframe += 1
            if (self.buffcoolTime > 300): #버프스킬 쿨타임 = 300초
                self.buffOn = False
                self.buffcoolTime = 0
                self.buffframe = 0
                self.buffTime=0
            if (self.buffTime > 150):
                self.damage = 15
                self.buffOn1 = False
            elif (self.buffTime<150):
                self.damage = 50
        if(self.cool1==True):
            self.skillcooltime1+=1
            if(self.skillcooltime1>150): #폭발스킬 쿨타임 150초
                self.cool1 = False
                self.skillcoolOn1=True
                self.skillcooltime1=0
        if(self.cool2==True):
            self.skillcooltime2+=1
            if(self.skillcooltime2>150): # 아이스필드스킬 쿨타임 150초
                self.skillcoolOn2=True
                self.cool2 = False
                self.skillcooltime2=0
        if(self.attack==True):
            self.attackframe += 1
            if (self.attackframe > 3):
                self.attackframe = 0
                self.attack = False
        if self.state < self.DOWN_RUN+1:
            self.frame = (self.frame + 1) % 4
        if self.state == self.RIGHT_RUN:
            if FieldSet[int((self.x-25)/50)+1][int((self.y-25)/50)].state==0 :
                self.x = min (700, self.x + 5)
        elif self.state == self.LEFT_RUN:
            if FieldSet[int((self.x-25)/50)][int((self.y-25)/50)].state==0 :
                self.x = max (0, self.x - 5)
        elif self.state == self.UP_RUN:
            if FieldSet[int((self.x-25)/50)][int((self.y-25)/50)+1].state==0 :
                self.y = min (700, self.y + 5)
        elif self.state == self.DOWN_RUN:
            if FieldSet[int((self.x-25)/50)][int((self.y-25)/50)].state==0 :
                self.y = max (0, self.y - 5)


        for M in monsterSet:
            if M.attack==True and M.attackframe>7 and math.sqrt((M.x-self.x)*(M.x-self.x)+(M.y-self.y)*(M.y-self.y))<50 and M.death==False:
                self.hp-=M.damage
        if self.skillstate==1 and self.skillGo==True:
            self.skillframe+=1
            if(self.skillframe>8):
                self.skillframe=0
                self.skillGo=False
        if self.skillstate==2 and self.skillGo==True:
            self.skillframe=(self.skillframe+1)%8
            self.icetime+=1
            if(self.icetime>50): # 아이스필드 스킬 시전시간
                self.skillframe=0
                self.icetime=0
                self.skillGo=False
        if self.hp<0:
            game_framework.push_state(GameOver)
    def draw(self):
        if self.buffOn1==True:
            self.buffOnimage.draw(500,650)
        if self.turretOn == True:
            self.turret.draw()
        if self.ringOn==True:
            self.ringimage.draw(self.x,self.y)
            self.cursorimage.draw(self.m_x,self.m_y)
        self.hpimage2.draw (self.x, self.y + 30, 50, 20)
        self.hpimage1.draw (self.x + (50 - self.hp/20)/2, self.y + 30, self.hp/20, 20)
        if self.attack==False:
            if(self.state<4):
                self.image.clip_draw (self.frame * 50, self.state * 50, 50, 50, self.x, self.y,50,50)
            else:
                self.image.clip_draw (self.frame * 50, (self.state-4) * 50, 50, 50, self.x, self.y,50,50)
        else:
            self.attackimage.clip_draw (self.attackdir*50, self.attackframe * 50, 50, 50, self.x, self.y, 50, 50)  # up
        if self.skillstate==1 and self.skillGo==True:
            self.SkillImage2.clip_draw(self.skillframe * 200, 0, 200, 200, self.m_x, self.m_y)
        if self.skillstate==2 and self.skillGo==True:
            self.SkillImage1.clip_draw(self.skillframe * 200, 0, 200, 200, self.m_x, self.m_y)
        if self.buffOn==True and self.buffframe<10:
            self.buffimage.clip_draw(self.buffframe*100,0,100,100,self.x,self.y+20)

class Turret:
    global missile
    image = None
    missile = []
    def __init__(self,x,y):
        self.frame = 0
        self.x,self.y = x,y
        self.launchTime = 0
        if Turret.image==None:
            self.image = load_image('Turret.png')
    def update(self):
        self.frame = (self.frame+1)%25
        self.launchTime+=1
        print(self.x)
        if self.launchTime%30==0:
            missile.append(Missile (self.x*50+25,self.y*50+25,0))
            missile.append (Missile (self.x*50+25, self.y*50+25, 1))
            missile.append (Missile (self.x*50+25, self.y*50+25, 2))
            missile.append (Missile (self.x*50+25, self.y*50+25, 3))
        for M in missile:
            M.update()
    def draw(self):
        self.image.clip_draw(self.frame*80,0,80,80,self.x*50+25,self.y*50+25,50,50)
        for M in missile:
            M.draw()

class Missile:
    image = None
    image_Explode =None
    global monsterSet
    global missile
    def __init__(self,x,y,dir):
        self.frame = 0
        self.x,self.y = x,y
        self.explodeframe = 0
        self.explode = False
        self.dir = dir
        self.remove = False
        if Missile.image==None:
            self.image = load_image ('Missile.png')
            self.image_Explode = load_image('MissileExplode.png')
    def update(self):
        self.frame = (self.frame+1)%4
        if self.explode==False:
            if self.dir==0:
                self.x+=10
            elif self.dir==1:
                self.x-=10
            elif self.dir==2:
                self.y+=10
            elif self.dir==3:
                self.y-=10
        if self.explode==True:
            self.explodeframe+=1
        if (self.x > 1000 or self.x < -100 or self.y < -100 or self.y > 1000) and self.remove==False:
            missile.remove (self)
            self.remove=True
        else:
            for M in monsterSet:
                if (math.sqrt ((self.x - M.x) * (self.x - M.x) + (self.y - M.y) * (
                    self.y - M.y)) < 50) and self.remove==False and M.death==False:
                    self.explode=True
                    if self.explodeframe>5:
                        missile.remove(self)
                        self.remove=True
                        M.hp -= 10

    def draw(self):
        if (self.explode==True):
            self.image_Explode.clip_draw(self.explodeframe*100,0,100,100,self.x,self.y)
        else:
            self.image.clip_draw (self.frame * 50, 0, 50, 50, self.x, self.y, 50, 50)

class UI:
    image = None
    image_BOMB_UI = None
    image_ICE_UI = None
    image_BUFF_UI = None
    image_BOMB_CLOSE_UI = None
    image_ICE_CLOSE_UI = None
    image_BUFF_CLOSE_UI = None
    image_Turret_UI = None
    image_Turret_CLOSE_UI = None

    def __init__(self):
        self.x = 0
        self.y = 0
        if self.image==None:
            self.image_BOMB_UI = load_image('Fire_UI.png')
            self.image_ICE_UI = load_image('ICE_UI.png')
            self.image_BUFF_UI = load_image('Buff_UI.png')
            self.image_BOMB_CLOSE_UI = load_image('FIRE_CLOSE_UI.png')
            self.image_ICE_CLOSE_UI = load_image('ICE_CLOSE_UI.png')
            self.image_BUFF_CLOSE_UI = load_image('BUFF_CLOSE_UI.png')
            self.image_Turret_CLOSE_UI = load_image('TURRET_CLOSE_UI.png')
            self.image_Turret_UI = load_image('Turret_UI.png')
    def draw(self):
        self.image_BUFF_UI.draw(300,650)
        self.image_ICE_UI.draw(200,650)
        self.image_BOMB_UI.draw(100,650)
        self.image_Turret_UI.draw(400,650)
        if character.skillcoolOn1==False:
            self.image_BOMB_CLOSE_UI.draw(100,650)
        if character.skillcoolOn2==False:
            self.image_ICE_CLOSE_UI.draw(200,650)
        if character.buffOn==True:
            self.image_BUFF_CLOSE_UI.draw(300,650)
        if character.turretOn==True or character.money<150:
            self.image_Turret_CLOSE_UI.draw(400,650)
    def update(self):
        pass
def enter():
    global FieldSet
    global character
    global home
    global monster
    global cursorimage
    global MakeTime
    global monsterSet
    global monstercount
    global stageimage1
    global stageimage2
    global stageimage3
    global cursorMove
    global ui
    global current_time
    current_time = get_time()
    ui = UI()
    cursorMove = False
    stageimage1 = load_image('Stage1.png')
    stageimage2 = load_image ('Stage2.png')
    stageimage3 = load_image ('Stage3.png')
    cursorimage = load_image('cursor.png')
    monstercount = 0
    home = Home()
    character = Character()
    monsterSet=[]
    monster = Monster(0)
    MakeTime = 0
    FieldSet = [[0 for col in range(14)] for row in range(14)]
    for y in range (0, 14):
        for x in range (0, 14):
            FieldSet[y][x]=Field(y * 50 + 25, x * 50 + 25, 1)

    Field.Change (FieldSet[5][2], 0)
    Field.Change (FieldSet[4][2], 0)
    Field.Change (FieldSet[10][2], 0)
    Field.Change (FieldSet[11][2], 0)
    for i in range(0,3):
        Field.Change(FieldSet[i][5],0)
    for i in range(0,4):
        Field.Change(FieldSet[3][5-i],0)
    for i in range(0,3):
        Field.Change(FieldSet[3+i][1],0)
    for i in range(1,8):
        Field.Change(FieldSet[6][i],0)
    for i in range(0,3):
        Field.Change(FieldSet[6+i][8],0)
    for i in range(0,7):
        Field.Change(FieldSet[9][8-i],0)
    for i in range(0,4):
        Field.Change(FieldSet[9+i][1],0)
    for i in range(0,7):
        Field.Change(FieldSet[12][1+i],0)


def exit():
    pass

def pause():
    pass


def resume():
    pass

running = True
def handle_events():
    global character
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            character.handle_event(event)



def get_frame_time():
    global current_time
    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time

def update():
    global running
    global MakeTime
    global monsterSet
    global monstercount
    global home
    MakeTime +=1
    frame_time = get_frame_time()
    print(frame_time)
    if monstercount<3:
        if(MakeTime<500):
            if(MakeTime%50==1):
                monsterSet.append(Monster(monstercount))
        if (len (monsterSet) == 0):
            monstercount +=1
            MakeTime=0
    else:
        game_framework.change_state(GameWin)
    for M in monsterSet:
        M.update(frame_time)
    home.update()
    character.update()
    if not running:
        game_framework.change_state(title_state)
        running=True


def draw():
    global ui
    global FieldSet
    global monstercount
    global monsterSet
    global stageimage1
    global stageimage2
    global stageimage3
    clear_canvas()
    for y in range(0,14):
        for x in range (0, 14):
            FieldSet[y][x].draw()
    if (monstercount == 0):
        stageimage1.draw (600, 650)
    elif (monstercount == 1):
        stageimage2.draw (600, 650)
    elif (monstercount == 2):
        stageimage3.draw (600, 650)
    ui.draw()
    home.draw()
    for M in monsterSet:
        M.draw()
    character.draw()
    update_canvas()
