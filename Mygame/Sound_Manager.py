from pico2d import *


Sound_List = {}

def LoadSoundData():
    global Sound_List
    Sound_List['Strike'] = load_music('Sound\\Strike.ogg')
    Sound_List['Buff_sound'] = load_music('Sound\\Buff_sound.ogg')
    Sound_List['Explosion'] = load_music('Sound\\Explosion.ogg')
    Sound_List['Ice_Field'] = load_music('Sound\\Ice_Field.ogg')
    Sound_List['Make_Turret'] = load_music('Sound\\Make_Turret.ogg')
    Sound_List['Button_on'] = load_music('Sound\\button.ogg')
    Sound_List['Button_on'].set_volume(8)
def PlayEffectSound(_sound_name):
    global Sound_List
    Sound_List[_sound_name].play ()

def PlayRepeatSound(sound_name):
    global Sound_List
    Sound_List[sound_name].repeat_play()

def StopRepeat(sound_name):
    global Sound_List
    Sound_List[sound_name].stop()