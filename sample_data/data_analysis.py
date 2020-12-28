import csv
import statistics
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def get_names(fp, reader): 
    """Finds all players from .csv file"""
    name_set = set()
    for line in reader:
        name = line[1]
        if name and not ("test" in name):  # gets rid of empties and tests
            name_set.add(name)
    names_list = list(name_set)
    names_list.sort()
    return names_list


def get_songs(player_name, fp, reader):
    """Finds all songs listened to by a specific player from .csv file"""
    fp.seek(0)
    next(reader, None)
    music_set = set()
    for line in reader:
        player = line[1]
        music = line[6]
        if (music != "---") and (player == player_name):
            music_set.add(music)
    return music_set


def total_data(player_name, fp, reader):
    """Calculates percent error data for one player"""
    fp.seek(0)
    next(reader, None)
    total_move_count = 0
    total_bad_count = 0
    practice_move_count = 0
    play_move_count = 0
    practice_bad_count = 0
    play_bad_count = 0
    for line in reader:
        player = line[1]
        state = line[5]
        music = line[6]
        if player == player_name:
            total_move_count += 1
            if music == "---":
                practice_move_count += 1
                if state == "bad":
                    practice_bad_count += 1
                    total_bad_count += 1
            else:
                play_move_count += 1
                if state == "bad":
                    play_bad_count += 1
                    total_bad_count += 1

    total_percent_bad = (total_bad_count / total_move_count)
    practice_percent_bad = (practice_bad_count / practice_move_count)

    print("\t number of total moves: {}".format(total_move_count))
    print("\t number of total bad moves: {}".format(total_bad_count))
    print("\t percent error over all games: {:.3%}".format(total_percent_bad))
    print("\t ---------------------------------")
    print("\t number of practice moves: {}".format(practice_move_count))
    print("\t number of practice bad moves: {}".format(practice_bad_count))
    print("\t percent error over practice games: {:.3%}".format(practice_percent_bad))
    print("\t ---------------------------------")
    if play_move_count:
        play_percent_bad = (play_bad_count / play_move_count)
        print("\t number of game moves: {}".format(play_move_count))
        print("\t number of game bad moves: {}".format(play_bad_count))
        print("\t percent error over real games: {:.3%}".format(play_percent_bad))
    else:
        print("\t no real games played ")
        play_percent_bad = 0
    print("\t ---------------------------------")

    return total_percent_bad, practice_percent_bad, play_percent_bad


def song_data(song_name, player_name, fp, reader):
    """Calculates percent error for a player while listening to a specific song"""
    fp.seek(0)
    next(reader, None)
    move_count = 0
    bad_count = 0
    for line in reader:
        player = line[1]
        music = line[6]
        state = line[5]
        if (player_name == player) and (song_name == music):  # collect data for specified player and song
            move_count += 1
            if state == "bad":
                bad_count += 1

    percent_bad = (bad_count / move_count)
    print("\t number of moves while listening to \"{}\": {}".format(song_name, move_count))
    print("\t number of bad moves while listening to \"{}\": {}".format(song_name, bad_count))
    print("\t percent error while listening to \"{}\": {:.3%}".format(song_name, percent_bad))
    print("\t ---------------------------------")


def avg_speed(player_name, fp, reader):
    """Calculates average average speed of cursor between clicks"""
    # not enough precision here, need milliseconds (fix later)
    fp.seek(0)
    next(reader, None)
    distance_travelled = 0
    start_time = ""
    speed_list = []
    practice_speed_list = []
    play_speed_list = []
    for line in reader:
        player = line[1]
        event = line[4]
        element_id = line[2]
        timestamp = line[3]
        music = line[6]
        if player == player_name:
            if element_id == "---":
                start_time = int(timestamp[-2:])
            if event == "hover":
                distance_travelled += 1
            if event == "click":
                end_time = int(timestamp[-2:])
                diff_time = end_time - start_time
                if diff_time < 0:
                    diff_time += 60
                if diff_time:  # removes trials where move takes <1s (fix precision)
                    speed = distance_travelled/diff_time
                    speed_list.append(speed)
                    if music == "---":
                        practice_speed_list.append(speed)
                    else:
                        play_speed_list.append(speed)
                distance_travelled = 0
    total_avg_speed = statistics.mean(speed_list)
    practice_avg_speed = statistics.mean(practice_speed_list)
    print("\t avg speed of cursor for all moves: {:.3} (moves/second)".format(total_avg_speed))
    if play_speed_list:
        play_avg_speed = statistics.mean(play_speed_list)
        print("\t avg speed of cursor for practice moves: {:.3} (moves/second)".format(practice_avg_speed))
        print("\t avg speed of cursor for game moves: {:.3} (moves/second)".format(play_avg_speed))
    else:
        play_avg_speed = 0
    print("\t ---------------------------------")
    return total_avg_speed, practice_avg_speed, play_avg_speed


def plot_data(names_list, totals_list, play_list, practice_list, y_axis, title):
    # credit to: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    x = np.arange(len(names_list))
    width = 0.25
    fig, ax = plt.subplots()

    r1 = np.arange(len(names_list))
    r2 = [x + width for x in r1]
    r3 = [x + width for x in r2]

    rects3 = ax.bar(r3, totals_list, width, label='overall')
    rects1 = ax.bar(r1, play_list, width, label='play (with music)')
    rects2 = ax.bar(r2, practice_list, width, label='practice')

    ax.set_ylabel(y_axis)
    ax.set_title(title)
    ax.set_xticks(x + width)
    ax.set_xticklabels(names_list)
    ax.legend(loc='best')

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    fig.tight_layout()
    plt.show()


def main():
    fp = open("mysite/sample_location.csv") # open .csv file and reader
    reader = csv.reader(fp)
    next(reader, None)
    names_list = get_names(fp, reader)
    totals_list, play_list, practice_list = [], [], []
    total_speed_list, play_speed_list, practice_speed_list = [], [], []

    # displays data for each player individually
    for player_name in names_list:  
        print("Data for {}".format(player_name))
        p_total, p_practice, p_play = total_data(player_name, fp, reader)
        totals_list.append(round((p_total*100), 2))
        play_list.append(round((p_play*100), 2))
        practice_list.append(round((p_practice*100), 2))
        music_set = get_songs(player_name, fp, reader)
        if not len(music_set):
            print("\t no games played with music ")
            print("\t ---------------------------------")
        for song in music_set:
            song_data(song, player_name, fp, reader)
        s_total, s_practice, s_play = avg_speed(player_name, fp, reader)
        total_speed_list.append(round(s_total, 2))
        practice_speed_list.append(round(s_practice, 2))
        play_speed_list.append(round(s_play, 2))
    fp.close()
    
    # display data for all players in a bar graph
    p_y_axis = "Percent error (%)"
    p_title = "Percent error of player moves while playing game"
    plot_data(names_list, totals_list, play_list, practice_list, p_y_axis, p_title)
    s_y_axis = "Average speed of cursor (moves/second)"
    s_title = "Average speed of cursor of each player while playing game"
    plot_data(names_list, total_speed_list, play_speed_list, practice_speed_list, s_y_axis, s_title)


if __name__ == '__main__':
    main()
