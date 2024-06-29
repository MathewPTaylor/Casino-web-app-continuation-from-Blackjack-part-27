from flask import render_template, redirect, url_for, flash, request, jsonify, session
from casinoapp import app, bcrypt, db, socketio
from casinoapp.forms import LoginForm, SignUpForm, ForgotPasswordForm
from casinoapp.models import User, Games, Tables
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send, emit, join_room, leave_room
from casinoapp.gamesandtables import *
import json


###############
# PAGE ROUTES #
###############


@app.route('/')
def index():
    return render_template('index.html', title="Home")


@app.route('/login', methods=["GET", "POST"]) 
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    # creating an instance of the login form
    form = LoginForm()
    
    # checking if the form has been submitted
    if form.validate_on_submit():
        # checking if there is a record with the email that is inputted, will return a User object if there is. Will return None if there is no record with that email
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('logged in bitch')
            flash(form.remember.data)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page if next_page is not None else url_for('index'))
        else:
            flash('Your email or password is incorrect.', 'danger')
    return render_template('login.html', form=form, title="Login")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    # create an instance of the sign up form
    form = SignUpForm()

    # check if the form has been submitted
    if form.validate_on_submit():
        # NOTE: the form classes automatically checks the availability of the username and email

        # add the user to the database
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")

        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # redirecting the user to the login page
        flash("Account created. Please login with your credentials.", 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form, title="Sign Up")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template("about.html", title="About")

@app.route('/account')
@login_required
def account():
    return render_template("account.html", title="Account", user=current_user)


@app.route('/games')
# @login_required
def games():
  return render_template("games.html", title="Games")


@app.route('/findTable/<int:id>', methods=["POST", "GET"])
def find_table_from_id(id):
  # find table and game from the id that is sent
  # redirect user to appropriate url link for the game
  gameindex = (id - 1) // 40  
  print(gameindex, Game.games[gameindex])

  return "<p>{}</p>".format(json.dumps([gameindex, Game.games[gameindex].name]))

@app.route('/Blackjack/<int:id>') # id parameter is the room id of the game
@app.route('/Blackjack')
@app.route('/Blackjack/')
# @login_required
def blackjack_game(id=None):
  # get user and table id
  # check if table id is valid for blackjack
  # if id is valid
    # check if table is available (seats are available at the table)
  
  if id is None:
    return redirect(url_for("games"))

  session["tableid"] = id
  
  table_query = db.select(Tables.id)
  table_ids = list(db.session.scalars(table_query))
  
  if session.get('tableid') not in table_ids:
    return redirect(url_for("games"))

  return render_template('blackjack.html', title="Blackjack Game: {}".format(id), id=id)




@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgot_password():
  form = ForgotPasswordForm()
  return render_template('forgotpassword.html', form=form, title="Forgot Password")


@app.route('/grid')
def grid():
  return render_template('grid.html')


###############
# AJAX ROUTES #
###############

def find_available_tables(objGame, min_bet, max_bet):
  # get tables for the correct game
  # get tables for the correct bet amount
  # get tables for available space (< max players)
  if min_bet is None:
    min_bet = objGame.bet_amounts[0][0]
    
  if max_bet is None:
    max_bet = objGame.bet_amounts[0][1]
  
  table_query = db.select(Tables).where(Tables.game_id == objGame.id).where(Tables.min_bet == min_bet).where(Tables.max_bet == max_bet).where(Tables.no_players < Tables.max_players)

  print(table_query)
  
  tables = db.session.scalars(table_query).all()
  
  tablesList = list(map(lambda x:vars(x), tables))

  game_name = objGame.name

  for table in tablesList:
    del table['_sa_instance_state']
    table['gameName'] = game_name
    
  print(tablesList)

  return tablesList 

@app.route('/select-game-genre', methods=["POST"])
def select_game_genre():
  # game_genre, minbet, maxbet = request.get_json()
  
  frontend_data = request.get_json()
  print("FRONTEND DATA: ", frontend_data)
  
  new_genre, game_genre, game_name, min_bet, max_bet = [frontend_data[key] for key in frontend_data]
  print(game_genre, game_name, min_bet, max_bet)
  
  return_data = {
    "filterDropdown": {
      'BetAmounts': {
        'Options': [],
        'DropdownLabel': 'Bet Amounts'
      }
    },
    "gamesList": [],
    "gameName": ""
  }
  """
  return_data = {
    'filterDropdown': {
      'Games': {
        'Options': [list of subset games],
        'DropdownLabel': 'Games'
      },
      'BetAmounts': {
        'Options': [list of bet amounts],
        'DropdownLabel': 'Bet Amounts'
      }
      
    }
    'gamesList': [list of tables of the games]
  }
  """
  # build the return data, then send it back to the frontend
  # build the data for the dropdown filter i.e. Bet amount dropdown etc.
  # the dropdown will be key value pairs, with the key being the title and the values being the options

  if new_genre: # from the game navigation bar
    if game_genre in Game.subset_games.keys():
      # building the bet amount dropdown
      return_data['filterDropdown']["BetAmounts"]['Options'] = Game.subset_games[game_genre][0].bet_amounts

      # building the subset game dropdown
      return_data['filterDropdown']["Games"] = {}
      return_data['filterDropdown']["Games"]['Options'] = [game.name for game in (Game.subset_games[game_genre])]
      return_data['filterDropdown']["Games"]['DropdownLabel'] = "Games"
      
      # getting the available tables 
      return_data['gamesList'] = find_available_tables(Game.subset_games[game_genre][0], min_bet, max_bet)
    else:
      return_data['filterDropdown']["BetAmounts"]['Options'] = Game.find_game(game_name if game_genre is None else game_genre).bet_amounts
      
      return_data['gamesList'] = find_available_tables(Game.find_game(game_name if game_genre is None else game_genre), min_bet, max_bet)
      
  else: # from filter dropdown
    return_data['filterDropdown']["BetAmounts"]['Options'] = Game.find_game(game_name).bet_amounts # if game_genre is None else game_genre).bet_amounts
    
    return_data['gamesList'] = find_available_tables(Game.find_game(game_name), min_bet, max_bet)
  
  print("THE RETURN DATA", return_data)
  # print(json.dumps(return_data))
  print(jsonify(return_data))
  print(str(jsonify(return_data)))
  print(json)

      
  # build the data for the return
  
  return jsonify(return_data)


@app.route('/getGameNames', methods=['POST'])
def get_game_names():
  print("AJAX WORKED")
  yo = request.form
  print(yo, "YO")
  print("JSON BEFORE", request.get_json(), "JSON")
  print(request.__dir__())
  return jsonify(Game.games)

@app.route('/sockets')
def sockets():
  return render_template("socket.html")

@app.route('/blackjack/<int:id>')
def blackjack(id):
  return render_template("blackjack.html")

################
# SOCKET EMITS #
################

@socketio.on("connect")
def handle_connect(message):
  # add some handle to make the user join the correct room
  print("YOOOO")
  # if not current_user.is_authenticated:

  #   return

  table_query = db.select(Tables.id)
  table_ids = list(db.session.scalars(table_query))
  
  if session.get("tableid") not in table_ids:
    return

  table = Tables.query.get(session.get("tableid"))
  print(table)

  if table.no_players >= table.max_players:
    return


  # join the user to the room
  join_room(session.get("tableid"))
  
  # update players list
  thelist = json.loads(table.current_players)
  print(current_user.__dir__())
  print(current_user.get_id(), "ID")
  thelist.append(current_user.get_id())

  table.current_players = json.dumps(thelist)
  
  # update no players
  table.no_players += 1

  db.session.commit()

  
  # client side will fetch the game state`
  
  
  print("a user is connected.")
  send(f"a user is connected. {session.get('tableid')}", to=session.get("tableid"))
  # send the seat number that the new player will be seated at
  # send the player info 


@socketio.on("disconnect")
def handle_disconnect(message):
  # add some handle to make the user join the correct room
  print("YOOOO")
  # if not current_user.is_authenticated:

  #   return

  table_query = db.select(Tables.id)
  table_ids = list(db.session.scalars(table_query))

  if session.get("tableid") not in table_ids:
    return

  table = Tables.query.get(session.get("tableid"))
  print(table)

  if table.no_players >= table.max_players:
    return


  # join the user to the room
  join_room(session.get("tableid"))

  # update players list
  thelist = json.loads(table.current_players)
  print(current_user.__dir__())
  print(current_user.get_id(), "ID")
  thelist.append(current_user.get_id())

  table.current_players = json.dumps(thelist)

  # update no players
  table.no_players += 1

  db.session.commit()


  # client side will fetch the game state


  print("a user is connected.")
  send(f"a user is connected. {session.get('tableid')}", to=session.get("tableid"))


@socketio.on("message")
def handle_message(message):
  print(message)
  roomid = session.get("talbeid")
  send(message+"yomignajig", broadcast=True, to=roomid)


@socketio.on("fetchGameState")
def fetch_game_state(table_id):
  pass


@socketio.on("BlackjackGetTable")
def get_bj_table():
  pass
  
'''
@app.route('/reset_password/<int: id>')
def reset_password():
  form = ResetPasswordForm()

  return render_template('resetpassword.html', form=form, title="Reset Password")

'''
