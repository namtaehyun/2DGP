from pico2d import *


Sound_List = {}

def LoadSoundData():
    global Sound_List
    Sound_List['Title'] = load_music('Sound\\Title.mp3')
    Sound_List['Battle'] = load_music('Sound\\Battle.mp3')
    Sound_List['Battle'].set_volume(8)
    Sound_List['GameOver'] = load_music('Sound\\GameOver.mp3')
    Sound_List['GameOver'].set_volume(8)

def PlayEffect(sound_name):
    global Sound_List
    Sound_List[sound_name].play()

def PlayRepeatSound(sound_name):
    global Sound_List
    Sound_List[sound_name].repeat_play()

def StopRepeat(sound_name):
    global Sound_List
    Sound_List[sound_name].stop()