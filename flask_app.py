from flask import Flask
from flask import render_template
from random import randint
from flask import redirect
import gridfunctions
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from datetime import datetime
import json


app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="townsonr",
    password="heartattackman",
    hostname="townsonr.mysql.pythonanywhere-services.com",
    databasename="townsonr$game_data",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'ca87f6b15b5c0504b3b2d8ed'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    '''Collects usernames of players and their high scores.'''

    __tablename__ = "login_data"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    high_score = db.Column(db.Integer)
    form_filled = db.Column(db.Boolean)
    practice_score = db.Column(db.Integer)


class Hover(db.Model):
    '''Tracks the location of the mouse and actions of the player during the game.'''

    __tablename__ = "mouse_location"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))  # who is playing
    element_id = db.Column(db.String(20))  # location of mouse (ie "A_1")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # time of event
    event = db.Column(db.String(20))  # mouseover, click, start level, start round, restart level
    state = db.Column(db.String(20))  # good or bad
    music = db.Column(db.String(20))  # name of song playing

    
class GridInfo(db.Model):
    '''Tracks the layout of the grid each time the player starts a new round.'''

    __tablename__ = "grid_info"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))  # who is playing
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # time of grid creation
    green = db.Column(db.String(20))  # ids of different colored boxes on the grid
    red = db.Column(db.String(20))
    mint = db.Column(db.String(20))
    blue = db.Column(db.String(20))
    purple = db.Column(db.String(20))
    pink = db.Column(db.String(20))
    orange = db.Column(db.String(20))
    level = db.Column(db.Integer)

    
@login_manager.user_loader
def load_user(user_id):
    ''' gets username of currently logged in player '''
    return User.query.get(int(user_id))


@app.route('/home')
@app.route('/')
def home():
    ''' Displays home page of personal website '''
    return render_template('home.html')


@app.route('/welcome')
def welcome():
    ''' Displays welcome message and gif '''
    return render_template('welcome.html')


@app.route('/credit')
def credit():
    ''' Displays credits for music used in the game '''
    return render_template('music_credit.html')


@app.route('/about')
def about():
    ''' Displays info about the research project '''
    return render_template('about.html')


@app.route('/login')
def game():
    ''' Asks for player name to store in tables and login user'''
    return render_template('game_login.html')


@app.route('/get_login', methods=['POST'])
def get_login():
    '''Adds login info to data table'''
    name = request.form["name"]
    login = User(username=name, form_filled=False)
    user = User.query.filter_by(username=name).first()
    if user:
        login_user(user)
        form_bool = current_user.form_filled
        if form_bool:
            return redirect('/instructions')
        else:
            return redirect('/form')
    else:
        db.session.add(login)
        db.session.commit()
        user = User.query.filter_by(username=name).first()
        login_user(user)
        return redirect('/form')

    
@app.route('/form')
def form():
    ''' Displays Google form to collect info about current player '''
    return render_template('info_form.html')


@app.route('/instructions')
def game_instructions():
    ''' Displays instructions and gifs, chooses value for music'''
    high_score_str = str(current_user.high_score)
    if not (high_score_str == "None"):
        msg = "Your previous high score was " + high_score_str + "."
        welcome = "Welcome back, " + current_user.username + "!"
    else:
        msg = ""
        welcome = "Hello, " + current_user.username + "!"
    return render_template('game_instructions.html', msg=msg, welcome=welcome)


@app.route('/get_level_<my_lvl>', methods=['GET', 'POST'])
def get_level(my_lvl):
    '''Sets up grid layouts for all rounds of a game'''
    lvl_int = int(my_lvl) - 1
    rounds_in_lvl = 5*(2**lvl_int)
    lvl = gridfunctions.create_level(rounds_in_lvl, 7)
    username = current_user.username
    for rnd, grid in lvl.items():
        green = grid["green"]
        red = grid["red"]
        mint = grid["mint"]
        blue = grid["blue"]
        purple = grid["purple"]
        pink = grid["pink"]
        orange = grid["orange"]
        grid_data = GridInfo(green=green, red=red, mint=mint, blue=blue, purple=purple, pink=pink, orange=orange, username=username, level=my_lvl)
        db.session.add(grid_data)
        db.session.commit()
    return jsonify(lvl)


@app.route('/get_data', methods=['POST'])
def get_data():
    '''Adds a move to the data table'''
    data_dict = request.get_json(force=True)
    username = current_user.username
    element_id = data_dict['element_id']
    event = data_dict['event']
    state = data_dict['state']
    music = data_dict['music']
    mouse_data = Hover(username=username, element_id=element_id, event=event, state=state, music=music)
    db.session.add(mouse_data)
    db.session.commit()
    return jsonify({"hello": "world"})


@app.route('/start_trial/trial<trial_number>')
def start_trial(trial_number):
    ''' Displays trial start page'''
    return render_template('start_trial.html', trial_number=trial_number)


# default play (for testing)
@app.route('/play/lvl')
def game_play():
    ''' runs the Squares game: creates grid, displays music credits, keeps score '''
    username = current_user.username
    return render_template('new_play.html', rounds_in_lvl=2 , next_lvl="win", username=username)


# levels w/ specified rounds
@app.route('/play/lvl1/trial<trial_number>')
def lvl1(trial_number):
    mus_name, mus_link = gridfunctions.get_music("random")
    return render_template('new_play.html', rounds_in_lvl=5, next_lvl="lvl2", start_score=0, this_lvl=1,
    music=mus_link, username=current_user.username, mus_name=mus_name, trial_number=trial_number)


@app.route('/play/lvl2/trial<trial_number>')
def lvl2(trial_number):
    mus_name, mus_link = gridfunctions.get_music("random")
    return render_template('new_play.html', rounds_in_lvl=10, next_lvl="lvl3", start_score=5, this_lvl=2,
    music=mus_link, username=current_user.username, mus_name=mus_name, trial_number=trial_number)


@app.route('/play/lvl3/trial<trial_number>')
def lvl3(trial_number):
    mus_name, mus_link = gridfunctions.get_music("random")
    return render_template('new_play.html', rounds_in_lvl=20, next_lvl="lvl4", start_score=15, this_lvl=3,
    music=mus_link, username=current_user.username, mus_name=mus_name, trial_number=trial_number)


@app.route('/play/lvl4/trial<trial_number>')
def lvl4(trial_number):
    mus_name, mus_link = gridfunctions.get_music("random")
    return render_template('new_play.html', rounds_in_lvl=40, next_lvl="lvl5", start_score=35, this_lvl=4,
    music=mus_link, username=current_user.username, mus_name=mus_name, trial_number=trial_number)


@app.route('/play/lvl5/trial<trial_number>')
def lvl5(trial_number):
    mus_name, mus_link = gridfunctions.get_music("random")
    return render_template('new_play.html', rounds_in_lvl=80, next_lvl="win", start_score=75, this_lvl=5,
    music=mus_link, username=current_user.username, mus_name=mus_name, trial_number=trial_number)


@app.route('/get_lvl_data', methods=['POST'])
def get_lvl_data():
    data = request.json
    new_data = json.loads(data)
    return jsonify(data)


@app.route('/play/lvlwin_<my_score>/trial<trial_number>')
def win(my_score, trial_number):
    ''' Displays "win" message with player score, adds new score to data table '''
    old_score = current_user.high_score
    if not old_score:
        old_score = 0
    new_score = int(my_score)
    if new_score > old_score:
        current_user.high_score = my_score
        db.session.commit()
    return render_template('win_lvl.html', my_score=my_score, trial_number=trial_number)


@app.route('/update_score_<my_score>/trial<trial_number>/<status>')
def update_score(my_score, trial_number, status):
    ''' Adds new high score to database if higher than previous stored score , displays or redirects to appropriate page'''
    old_score = current_user.high_score
    if not old_score:
        old_score = 0
    new_score = int(my_score)
    if new_score > old_score:
        current_user.high_score = my_score
        db.session.commit()
    if (trial_number == "4"):
        if (status == "good"):
            return redirect("end_good/" + my_score)
        elif (status == "bad"):
            return redirect("end_bad/" + my_score)
    return render_template('bad_click.html', my_score=my_score, old_score=old_score, trial_number=trial_number)


@app.route('/update_form_filled')
def update_form():
    ''' Updates data table to display if user has filled out the player information form'''
    current_user.form_filled = True
    db.session.commit()
    return redirect('/instructions')


@app.route('/end_good/<player_score>')
def end_good(player_score):
    ''' Displays end of game page after player wins the last trial'''
    return render_template('end_game_good.html', my_score=player_score)


@app.route('/end_bad/<player_score>')
def end_bad(player_score):
    ''' Displays end of game page after player loses in the last trial'''
    return render_template('end_game_bad.html', my_score=player_score)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/welcome')


if __name__ == '__main__':
    app.run()

    
