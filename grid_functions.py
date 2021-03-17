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
    ''' Creates an s x s dict with {color: id} with no id overlaps'''
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
    mus_dict = {"citylife": "/static/artificial-music-city-life",
                "shortbreak": "/static/glitch-short-break",
                "stoned": "/static/alexander-nakarada-stoned",
                "agreatcalm": "/static/kev-rowe-a-great-calm",
                "kaleidoscope": "/static/fsm-team-escp-kaleidoscope",
                "vintageradiostation": "/static/sakura-hz-vintage-radio-station",
                "midnightdrive": "/static/inossi-midnight-drive",
                "melancholia" : "/static/fsm-team-escp-yellowtree-melancholia-goth-emo-type-beat" ,
                "spiritcross" : "/static/schematist-spirit-cross",
                "catalyst" : "/static/alexander-nakarada-catalyst",
                "meadows" : "/static/artificial-music-meadows-in-the-sky",
                "banger" : "/static/fsm-team-banger",
                "poprock" : "/static/lukenield-alternative-pop-rock-instrumental",
                "altrock" : "/static/lukenield-alternative-rock-instrumental",
                "wavy" : "/static/punch-deck-keep-it-wavy",
                "rise" : "/static/punch-deck-rise",
                "chilly": "/static/purrple-cat-chilly",
                "gottago" : "/static/tokyo-music-walker-gotta-go",
                "ninendo" : "/static/yoitrax-nintendo-64",
                "springtime" : "/static/fsm-team-escp-eternal-springtime"
                }
    list1 = ["agreatcalm", "citylife", "vintageradiostation", "meadows", "chilly"]
    list2 = ["kaleidoscope", "springtime", "ninendo", "gottago" ]
    list3 = ["midnightdrive", "banger", "altrock", "poprock", "rise"]
    list4 = ["stoned", "melancholia", "spiritcross", "wavy", "catalyst"]
    tempo_change = ["agreatcalm", "citylife", "vintageradiostation", "kaleidoscope", "midnightdrive", "stoned", "melancholia", "spiritcross"]
    if trial == "4":
        tempo = 0
        if choose%2:
            tempo = 10 * lvl - 30
        else:
            tempo = -10 * lvl + 30
        mus = mus_dict[song] + "_" + str(tempo) + ".mp3"
        song += (" " + str(tempo))
        return song, mus
    elif trial == "random":
        mus_key = random.choice(tempo_change)
        return mus_key, mus_dict[mus_key] + ".mp3"
    elif trial == "3":  # choose random song for each round
        mus_key = random.choice(list(mus_dict.keys()))
        return mus_key, mus_dict[mus_key] + ".mp3"
    elif trial == "2":
        mus_list = []
        if song == "1":
            mus_list = list1
        if song == "2":
            mus_list = list2
        if song == "3":
            mus_list = list3
        if song == "4":
            mus_list = list4
        mus_key = random.choice(mus_list)
        return mus_key, mus_dict[mus_key] + ".mp3"
    elif trial == "1":
        return "none", str()

            
