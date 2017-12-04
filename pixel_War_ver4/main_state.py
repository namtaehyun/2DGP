import random
import json
import os

from pico2d import *

import GameWin
import game_framework
import title_state
import GameOver
import Sound_Manager
name = "MainState"

class Field:
    img = None
    def __init__(self,x,y,state):
        self.x = x
        self.y = y
        self.state = state
        if Field.img == None:
            Field.image1 = load_image('Graphics\\grass.png')
            Field.image2 = load_image('Graphics\\road.png')
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
            Home.hpimage1 = load_image ('Graphics\\healthStatusBar.png')
            Home.hpimage2 = load_image ('Graphics\\healthStatusBar1.png')
        if Home.image == None:
            Home.image = load_image('Graphics\\home.PNG')
    def update(self):
        for M in monsterSet:
            if M.attack==True and M.attackframe>7 and math.sqrt((M.x-self.x)*(M.x-self.x)+(M.y-self.y)*(M.y-self.y))<50 and M.death==False:
                self.hp-=5
        if self.hp<0:
            game_framework.change_state(GameOver)
    def draw(self):
        self.hpimage2.draw (self.x, self.y + 100, 100, 20)
        self.hpimage1.draw (self.x + (100 - self.hp / 10) / 2, self.y + 100, self.hp / 10, 20)
        self.image.draw(self.x,self.y,150,150)
class Monster:
    image = None
    attackImage =None
    RIGHT_RUN,UP_RUN, DOWN_RUN = 1,0,3
    def __init__(self,state):
        self.hp = 0
        self.state = state
        self.damage = 3
        self.attack = False
        self.frame = 0
        self.attackframe=0
        self.attackspeed = 10
        self.speed = 100
        self.framespeed=10
        self.x,self.y =25,275
        self.death= False
        self.dir =0
        self.bloodtime=0
        self.bloodspeed = 10
        self.movestate = self.RIGHT_RUN
        if self.state == 0:
            self.hp = 100
            self.image=load_image('Graphics\\pig.png')
            self.attackImage = load_image('Graphics\\Monster_attack2.png')
        elif self.state == 1:
            self.hp = 150
            self.image =load_image('Graphics\\trash.png')
            self.attackImage = load_image('Graphics\\Monster_attack1.png')
        elif self.state == 2:
            self.hp = 200
            self.image =load_image('Graphics\\nohead.png')
            self.attackImage = load_image('Graphics\\Monster_attack.png')
    def update(self,frame_time):
        if self.death==False:
            if character.skillstate == 1 and character.Skill_Performing == True and math.sqrt((character.m_x-self.x)*(character.m_x-self.x)+(character.m_y-self.y)*(character.m_y-self.y))<100\
                    and character.skillframe>6:
                self.hp -= 50
            if character.skillstate == 2 and character.Skill_Performing == True and math.sqrt((character.m_x-self.x)*(character.m_x-self.x)+(character.m_y-self.y)*(character.m_y-self.y))<100:
                self.speed = 50
                self.damage = 1
            else:
                self.speed = 100
                self.damage = 5
            if(self.attack==True):
                self.attackframe += self.attackspeed*frame_time
                if (self.attackframe > 10):
                    self.attackframe = 0
                    self.attack = False
            if math.sqrt((self.x-character.x)*(self.x-character.x)+(self.y-character.y)*(self.y-character.y))<50 or \
                            math.sqrt((self.x-home.x)*(self.x-home.x)+(self.y-home.y)*(self.y-home.y))<50:
                self.attack=True
            else:
                self.attack=False

            if self.attack==False:
                self.frame = (self.frame + self.framespeed*frame_time) % 4
                if(self.movestate==self.RIGHT_RUN):
                    self.x+=self.speed*frame_time
                if(self.movestate==self.UP_RUN):
                    self.y+=self.speed*frame_time
                if(self.movestate==self.DOWN_RUN):
                    self.y-=self.speed*frame_time
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
        if self.hp<0 and self.death==False:
            character.money += 30
        if self.hp<0:
            self.bloodtime+=self.bloodspeed*frame_time
            self.death = True
    def draw(self):
        if self.death==False:
            self.image.clip_draw (int(self.frame) * 50, self.movestate* 50, 50, 50, self.x, self.y, 50, 50)
            if self.attack==True:
                self.attackImage.clip_draw(int(self.attackframe)*50,0,50,50,self.x,self.y)
        else:
            self.image = load_image('Graphics\\Blood.png')
            self.image.opacify(1-self.bloodtime/50)
            self.image.draw(self.x,self.y)
            if(self.bloodtime>50):
                monsterSet.remove(self)
class Character:
    global monsterSet
    global turret
    Buff_On_image = None
    Character_image = None
    Hp_Bar_Image = None
    Hp_status_image = None
    Attack_image = None
    attack = False
    Ring_Range_Image = None
    Bomb_Skill_image = None
    Ice_Skill_image = None
    Cursor_image = None
    Buff_Skill_image = None
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
        self.Skill_Performing=False #스킬시전
        self.Bomb_Skill_Cooltime_On = True
        self.Ice_Skill_Cooltime_On = True
        self.damage = 5
        self.Ring_Range_On = False
        self.hp = 1000
        self.frame = 0
        self.attackdir = 0
        self.Fire_Skill_Cool = False
        self.buffframe = 0
        self.Bomb_Cool_time = 0
        self.Ice_Skill_Cool = False
        self.Ice_Cool_time = 0
        self.turretOn = False
        self.skillcoolOn_speed = 20
        self.skillice_frame = 20
        self.attackframe=0
        self.buff_frame_speed = 30
        self.skillframe_speed = 20
        self.move_speed = 100
        self.attack_speed = 30
        self.move_frame_speed = 10
        self.tron = False
        self.state = self.DOWN_STAND
        if Character.Character_image == None:
            Character.Buff_Skill_image = load_image('Graphics\\buff.png')
            Character.Ring_Range_Image = load_image('Graphics\\SkillRing.png')
            Character.Character_image = load_image ('Graphics\\Character.png')
            Character.Attack_image = load_image('Graphics\\attack.png')
            Character.Hp_Bar_Image =load_image('Graphics\\healthStatusBar.png')
            Character.Hp_status_image =load_image('Graphics\\healthStatusBar1.png')
            Character.Bomb_Skill_image = load_image('Graphics\\Ice_field.png')
            Character.Ice_Skill_image = load_image ('Graphics\\bomb.png')
            Character.Cursor_image = load_image('Graphics\\cursor.png')
            Character.Buff_On_image = load_image('Graphics\\BUFF_ON.png')

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION and self.Ring_Range_On==True and self.Skill_Performing==False:
            self.m_x, self.m_y = event.x, 700 - event.y
        if event.type == SDL_MOUSEBUTTONDOWN and self.skillstate==1 and self.Skill_Performing==False \
                and math.sqrt((self.x-self.m_x)*(self.x-self.m_x)+(self.y-self.m_y)*(self.y-self.m_y))<150 and self.Fire_Skill_Cool == False and self.tron==False:
            Sound_Manager.PlayEffectSound('Explosion')
            self.Skill_Performing = True
            self.Fire_Skill_Cool = True
            self.Bomb_Skill_Cooltime_On = False
        elif event.type == SDL_MOUSEBUTTONDOWN and self.skillstate==2 and self.Skill_Performing==False \
                and math.sqrt ((self.x - self.m_x) * (self.x - self.m_x) + (self.y - self.m_y) * (self.y - self.m_y))< 150 and self.Ice_Skill_Cool == False and self.tron==False:
            Sound_Manager.PlayEffectSound('Ice_Field')
            self.Skill_Performing = True
            self.Ice_Skill_Cool = True
            self.Ice_Skill_Cooltime_On = False
        elif event.type == SDL_MOUSEBUTTONDOWN and self.turretOn==False and FieldSet[int(self.m_x/50)][int(self.m_y/50)].state==1 \
                and math.sqrt ((self.x - self.m_x) * (self.x - self.m_x) + (self.y - self.m_y) * (
                    self.y - self.m_y)) < 150:
            Sound_Manager.PlayEffectSound('Make_Turret')
            self.turret = Turret(int(self.m_x/50),int(self.m_y/50))
            self.money-=350
            self.turretOn = True
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_1) and self.Skill_Performing==False and self.Bomb_Skill_Cooltime_On==True :
            self.Ring_Range_On = True
            self.skillstate = 1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2) and self.Skill_Performing==False and self.Ice_Skill_Cooltime_On==True :
            self.Ring_Range_On = True
            self.skillstate = 2
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3) and self.buffOn == False:
            Sound_Manager.PlayEffectSound('Buff_sound')
            self.buffOn = True
            self.buffOn1 = True
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_4) and self.turretOn ==False and self.money>350:
            self.tron = True
            self.Ring_Range_On=True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_1):
            self.Ring_Range_On = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_2):
            self.Ring_Range_On = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_4):
            self.tron = False
            self.Ring_Range_On = False
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
            Sound_Manager.PlayEffectSound('Strike')
            self.attack = True

    def update(self,frame_time): #소수점이후로 다 버려버림..
        global FieldSet
        if self.turretOn==True:
            self.turret.update(frame_time)
        if self.buffOn == True:
            self.buffcoolTime += frame_time*self.skillcoolOn_speed
            self.buffTime += frame_time*self.skillcoolOn_speed
            self.buffframe += frame_time
            if (self.buffcoolTime > 300): #버프스킬 쿨타임 = 300초
                self.buffOn = False
                self.buffcoolTime = 0
                self.buffframe = 0
                self.buffTime=0
            if (self.buffTime > 150):
                self.damage = 5
                self.buffOn1 = False
            elif (self.buffTime<150):
                self.damage = 15
        if(self.Fire_Skill_Cool==True):
            self.Bomb_Cool_time+= frame_time * self.skillcoolOn_speed
            if(self.Bomb_Cool_time>150): #폭발스킬 쿨타임 150초
                self.Fire_Skill_Cool = False
                self.Bomb_Skill_Cooltime_On=True
                self.Bomb_Cool_time=0
        if(self.Ice_Skill_Cool==True):
            self.Ice_Cool_time+= frame_time * self.skillcoolOn_speed
            if(self.Ice_Cool_time>150): # 아이스필드스킬 쿨타임 150초
                self.Ice_Skill_Cooltime_On=True
                self.Ice_Skill_Cool = False
                self.Ice_Cool_time=0
        if(self.attack==True):
            self.attackframe += frame_time*self.attack_speed
            if (self.attackframe > 3):
                self.attackframe = 0
                self.attack = False
        if self.state < self.DOWN_RUN+1:
            self.frame = (self.frame+self.move_frame_speed*frame_time)%4
        if self.state == self.RIGHT_RUN:
            if FieldSet[int((self.x-25)/50)+1][int((self.y-25)/50)].state==0 :
                self.x = min (700, self.x + frame_time*self.move_speed)
        elif self.state == self.LEFT_RUN:
            if FieldSet[int((self.x-25)/50)][int((self.y-25)/50)].state==0 :
                self.x = max (0, self.x - frame_time*self.move_speed)
        elif self.state == self.UP_RUN:
            if FieldSet[int((self.x-25)/50)][int((self.y-25)/50)+1].state==0 :
                self.y = min (700, self.y + frame_time*self.move_speed)
        elif self.state == self.DOWN_RUN:
            if FieldSet[int((self.x-25)/50)][int((self.y-25)/50)].state==0 :
                self.y = max (0, self.y - frame_time*self.move_speed)


        for M in monsterSet:
            if M.attack==True and M.attackframe>7 and math.sqrt((M.x-self.x)*(M.x-self.x)+(M.y-self.y)*(M.y-self.y))<50 and M.death==False:
                self.hp-=M.damage
        if self.skillstate==1 and self.Skill_Performing==True:
            self.skillframe+=self.skillframe_speed*frame_time
            if(self.skillframe>8):
                self.skillframe=0
                self.Skill_Performing=False
        if self.skillstate==2 and self.Skill_Performing==True:
            self.skillframe=(self.skillframe+self.skillframe_speed*frame_time)%8
            self.icetime+=self.skillice_frame*frame_time
            if(self.icetime>50): # 아이스필드 스킬 시전시간
                self.skillframe=0
                self.icetime=0
                self.Skill_Performing=False
        if self.hp<0:
            game_framework.change_state(GameOver)
    def draw(self):
        if self.buffOn1==True:
            self.Buff_On_image.draw(500, 650)
        if self.turretOn == True:
            self.turret.draw()
        if self.Ring_Range_On==True:
            self.Ring_Range_Image.draw(self.x, self.y)
            self.Cursor_image.draw(self.m_x, self.m_y)
        self.Hp_status_image.draw (self.x, self.y + 30, 50, 20)
        self.Hp_Bar_Image.draw (self.x + (50 - self.hp / 20) / 2, self.y + 30, self.hp / 20, 20)
        if self.attack==False:
            if(self.state<4):
                self.Character_image.clip_draw (int(self.frame) * 50, self.state * 50, 50, 50, self.x, self.y, 50, 50)
            else:
                self.Character_image.clip_draw (int(self.frame) * 50, int(self.state - 4) * 50, 50, 50, self.x, self.y, 50, 50)
        else:
            self.Attack_image.clip_draw (self.attackdir * 50, int(self.attackframe) * 50, 50, 50, self.x, self.y, 50, 50)  # up
        if self.skillstate==1 and self.Skill_Performing==True:
            self.Ice_Skill_image.clip_draw(int(self.skillframe) % 8 * 200, 0, 200, 200, self.m_x, self.m_y)
        if self.skillstate==2 and self.Skill_Performing==True:
            self.Bomb_Skill_image.clip_draw(int(self.skillframe) % 8 * 200, 0, 200, 200, self.m_x, self.m_y)
        if self.buffOn==True and self.buffframe<10:
            self.Buff_Skill_image.clip_draw(int(self.buffframe * self.buff_frame_speed) * 100, 0, 100, 100, self.x, self.y + 20)
class Turret:
    global missile
    image = None
    missile = []
    def __init__(self,x,y):
        self.frame = 0
        self.x,self.y = x,y
        self.launchTime = 0
        self.frameSpeed = 20
        if Turret.image==None:
            self.image = load_image('Graphics\\Turret.png')
    def update(self,frame_time):
        self.launchTime +=1
        self.frame = (self.frame+frame_time*self.frameSpeed)%25
        if(self.launchTime%1000==0):
            missile.append(Missile (self.x*50+25,self.y*50+25,0))
            missile.append (Missile (self.x*50+25, self.y*50+25, 1))
            missile.append (Missile (self.x*50+25, self.y*50+25, 2))
            missile.append (Missile (self.x*50+25, self.y*50+25, 3))
        for M in missile:
            M.update(frame_time)
    def draw(self):
        self.image.clip_draw(int(self.frame)*80,0,80,80,self.x*50+25,self.y*50+25,50,50)
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
        self.speed = 200
        self.explodeframe = 0
        self.explodespeed = 20
        self.explode = False
        self.dir = dir
        self.remove = False
        if Missile.image==None:
            self.image = load_image ('Graphics\\Missile.png')
            self.image_Explode = load_image('Graphics\\MissileExplode.png')
    def update(self,frame_time):
        self.frame = (self.frame+frame_time*self.speed)%4
        if self.explode==False:
            if self.dir==0:
                self.x+=frame_time*self.speed
            elif self.dir==1:
                self.x-=frame_time*self.speed
            elif self.dir==2:
                self.y+=frame_time*self.speed
            elif self.dir==3:
                self.y-=frame_time*self.speed
        if self.explode==True:
            self.explodeframe+=frame_time*self.explodespeed
        if (self.x > 1000 or self.x < -100 or self.y < -100 or self.y > 1000) and self.remove==False:
            missile.remove (self)
            self.remove=True
        else:
            for M in monsterSet:
                if (math.sqrt ((self.x - M.x) * (self.x - M.x) + (self.y - M.y) * (
                    self.y - M.y)) < 25) and self.remove==False and M.death==False:
                    self.explode=True
                    if self.explodeframe>5:
                        missile.remove(self)
                        self.remove=True
                        M.hp -= 10

    def draw(self):
        if (self.explode==True):
            self.image_Explode.clip_draw(int(self.explodeframe)*100,0,100,100,self.x,self.y)
        else:
            self.image.clip_draw (int(self.frame) * 50, 0, 50, 50, self.x, self.y, 50, 50)
class UI:
    font = None
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
        UI.font = load_font('hjbmb.ttf')
        if self.image==None:
            self.image_BOMB_UI = load_image('Graphics\\Fire_UI.png')
            self.image_ICE_UI = load_image('Graphics\\ICE_UI.png')
            self.image_BUFF_UI = load_image('Graphics\\Buff_UI.png')
            self.image_BOMB_CLOSE_UI = load_image('Graphics\\FIRE_CLOSE_UI.png')
            self.image_ICE_CLOSE_UI = load_image('Graphics\\ICE_CLOSE_UI.png')
            self.image_BUFF_CLOSE_UI = load_image('Graphics\\BUFF_CLOSE_UI.png')
            self.image_Turret_CLOSE_UI = load_image('Graphics\\TURRET_CLOSE_UI.png')
            self.image_Turret_UI = load_image('Graphics\\Turret_UI.png')
    def draw(self):
        UI.font.draw(500,600,'Money:%d'%character.money,(100,0,0))
        self.image_BUFF_UI.draw(300,650)
        self.image_ICE_UI.draw(200,650)
        self.image_BOMB_UI.draw(100,650)
        self.image_Turret_UI.draw(400,650)
        if character.Bomb_Skill_Cooltime_On==False:
            self.image_BOMB_CLOSE_UI.draw(100,650)
        if character.Ice_Skill_Cooltime_On==False:
            self.image_ICE_CLOSE_UI.draw(200,650)
        if character.buffOn==True:
            self.image_BUFF_CLOSE_UI.draw(300,650)
        if character.turretOn==True or character.money<350:
            self.image_Turret_CLOSE_UI.draw(400,650)
    def update(self):
        pass

def enter():
    global Bgm
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
    Sound_Manager.LoadSoundData()
    Bgm = load_wav('Sound\\Battle.wav')
    Bgm.set_volume(8)
    Bgm.repeat_play()
    current_time = get_time()
    ui = UI()
    cursorMove = False
    stageimage1 = load_image('Graphics\\Stage1.png')
    stageimage2 = load_image ('Graphics\\Stage2.png')
    stageimage3 = load_image ('Graphics\\Stage3.png')
    cursorimage = load_image('Graphics\\cursor.png')
    monstercount = 0
    home = Home()
    character = Character()
    monsterSet=[]
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
    global Bgm
    del(Bgm)
def pause():
    global Bgm
    del(Bgm)
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
    if monstercount<3:
        if(MakeTime<3000): #실수로 하면 안되는데 자꾸 실수로나옴... 어떻게하징?
            if(MakeTime%250==1):
                monsterSet.append(Monster(monstercount))
        if (len (monsterSet) == 0):
            monstercount +=1
            MakeTime=0
    else:
        game_framework.change_state(GameWin)
    for M in monsterSet:
        M.update(frame_time)
    home.update()
    character.update(frame_time)
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
