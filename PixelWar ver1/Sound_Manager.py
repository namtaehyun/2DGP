from pico2d import *

SoundList = {}
def LoadSoundData():
    global SoundList
    SoundList['Title'] = load_music('Title.ogg')
    SoundList['Title'].set_volume(16)

def PlayEffectSound(_sound_name):
    global  SoundList
    SoundList[_sound_name].play()
def PlayRepeatedEffectSound(_sound_name):
    global SoundList
    SoundList[_sound_name].repeat_play()


def StopRepeatedEffectSound(_sound_name):
    global SoundList
    SoundList[_sound_name].repeat_play()