from random import randint
import random


def create_square(s):
    ''' Creates one square in s x s grid'''
    num = randint(1, s)
    c = chr(randint(65, s + 64))
    square = "{}_{}".format(c, num)
    while ((square == "A_5") or (square == "A_6") or (square == "A_7")):
        num = randint(1, s)
        c = chr(randint(65, s + 64))
        square = "{}_{}".format(c, num)
    return square


def create_grid(s):
    ''' Creates an s x s dict with {color, id} with no id overlaps'''
    color_list = ["green", "red", "mint", "blue", "purple", "pink", "orange"]
    id_set = set()  # to guarantee no overlaps
    while len(id_set) < s:
        id_set.add(create_square(s))
    grid = dict(zip(color_list, id_set))
    return grid


def create_level(n, s):
    ''' Creates a dictionary of n grids with size s x s'''
    lvl = {}
    for i in range(n):
        grid = create_grid(s)
        lvl[i+1] = grid
    return lvl


def get_music(choose="", lvls_in_game=5, song="", lvl=0, trial="0"):
    ''' Choosing music for each round of the game'''
    mus_dict = {"citylife": "https://www.free-stock-music.com/music/artificial-music-city-life.mp3",
                "shortbreak": "https://www.free-stock-music.com/music/glitch-short-break.mp3",
                "stoned": "https://www.free-stock-music.com/music/alexander-nakarada-stoned.mp3",
                "agreatcalm": "https://www.free-stock-music.com/music/kev-rowe-a-great-calm.mp3",
                "kaleidoscope": "https://www.free-stock-music.com/music/fsm-team-escp-kaleidoscope.mp3",
                "vintageradiostation": "https://www.free-stock-music.com/music/sakura-hz-vintage-radio-station.mp3",
                "midnightdrive": "https://www.free-stock-music.com/music/inossi-midnight-drive.mp3"
                }
    a_list = ["agreatcalm", "citylife", "stoned", "vintageradiostation"]
    b_list = ["kaleidoscope", "midnightdrive", "melancholia", "spiritcross"]
    if trial == "4": # changing tempo
        tempo = 0
        if choose == "even":
            tempo = 10 * lvl - 30
        elif choose == "odd":
            tempo = -10 * lvl + 30
        mus = mus_dict[song] + "_" + str(tempo) + ".mp3"
        song += " " + str(tempo)
        return song, mus
    elif trial == "3":  # choose random song for each round
        mus_key = random.choice(list(mus_dict.keys()))
        return mus_key, mus_dict[mus_key] + ".mp3"
    elif trial == "2":
        if choose == "even":
            mus_key = random.choice(a_list)
            return mus_key, mus_dict[mus_key] + ".mp3"
        if choose == "odd":
            mus_key = random.choice(b_list)
            return mus_key, mus_dict[mus_key] + ".mp3"
    elif trial == "1":
        return "none", str()

            
