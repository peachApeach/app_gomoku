from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, status, HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, request, make_response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from flask import Flask, redirect, url_for, request, session, render_template
import logging
from flask_session import Session
from gomoku.srcs.Gomoku import Gomoku
from gomoku.srcs.algorithms.gomoku_state import terminate_state
from gomoku.srcs.utils.little_gomoku_utils import convert_to_little_gomoku
from gomoku.srcs.algorithms.gomoku_algorithm import minimax
from gomoku.srcs.utils.MeasureTime import MeasureTime
from gomoku.srcs.rules.GomokuSettings import GomokuSettings
import requests
import sys
import os
import time
import random

load_dotenv()

flask_app = Flask(__name__)

logging.basicConfig(filename='flask.log', level=logging.DEBUG)

flask_app.config['SESSION_TYPE'] = 'filesystem'
flask_app.config['TEMPLATES_AUTO_RELOAD'] = True

flask_app.config['SESSION_COOKIE_SECURE'] = True
flask_app.config['SESSION_COOKIE_SAMESITE'] = 'None'

Session(flask_app)

CLIENT_ID = os.getenv('UID')
CLIENT_SECRET = os.getenv('SECRET_TOKEN')
REDIRECT_URI = 'http://127.0.0.1:4000/auth/callback'

@flask_app.route('/')
def index():
	flask_app.logger.info('This is info output')
	if 'token' in session and session['token'] is not None:
		url = 'https://api.intra.42.fr/v2/me'
		headers = {
			'Authorization': f'Bearer {session["token"]}'
		}
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			resultat = response.json()
			data = {
				'login': resultat['login']
			}
			flask_app.logger.info('before redirect')
			return redirect("http://localhost:5173/#/")
			# else:
			#     return render_template('whitelist.html')
		else:
			return render_template('login.html', error="Unable to fetch data from API")
	# else:
	#     return render_template('login.html')

@flask_app.route('/login')
def login():
	auth_url = f'https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code'
	return redirect(auth_url)

@flask_app.route('/callback')
def auth_callback():
	flask_app.logger.info('This is info output')
	code = request.args.get('code')
	if not code:
		return 'No code provided', 400

	token_url = 'https://api.intra.42.fr/oauth/token'
	token_data = {
		'grant_type': 'authorization_code',
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'code': code,
		'redirect_uri': REDIRECT_URI
	}

	token_response = requests.post(token_url, data=token_data)
	if token_response.status_code != 200:
		return f"Error fetching token: {token_response.text}", token_response.status_code
	token_json = token_response.json()

	try:
		flask_app.logger.info('Add session cookie')
		session['token'] = token_json['access_token']
	except KeyError:
		return 'Access token not found in the response', 500
	return redirect(url_for('index'))

@flask_app.route('/logout')
def logout():
	session.pop('token', None)
	return redirect(url_for('ranking'))

load_dotenv()

flask_app = Flask(__name__)

logging.basicConfig(filename='flask.log', level=logging.DEBUG)

flask_app.config['SESSION_TYPE'] = 'filesystem'

flask_app.config['TEMPLATES_AUTO_RELOAD'] = True
# flask_app.config['SESSION_COOKIE_SECURE'] = True
# flask_app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

Session(flask_app)

CLIENT_ID = os.getenv('UID')
CLIENT_SECRET = os.getenv('SECRET_TOKEN')
REDIRECT_URI = 'http://127.0.0.1:4000/auth/callback'

@flask_app.route('/')
def index():
    flask_app.logger.info('This is info output')
    if 'token' in session and session['token'] is not None:
        url = 'https://api.intra.42.fr/v2/me'
        headers = {
            'Authorization': f'Bearer {session["token"]}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            resultat = response.json()
            data = {
                'login': resultat['login']
            }
            flask_app.logger.info('before redirect')
            resp = make_response(redirect('http://localhost:5173/#/'))
            resp.set_cookie('token', session['token'], secure=False)
            return resp
            # return redirect('http://localhost:5173/#/')
            # else:
            #     return render_template('whitelist.html')
        # else:
        #     return render_template('login.html', error="Unable to fetch data from API")
    # else:
    #     return render_template('login.html')

@flask_app.route('/login')
def login():
    auth_url = f'https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code'
    return redirect(auth_url)

@flask_app.route('/callback')
def auth_callback():
    flask_app.logger.info('This is info output')
    code = request.args.get('code')
    if not code:
        return 'No code provided', 400

    token_url = 'https://api.intra.42.fr/oauth/token'
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    token_response = requests.post(token_url, data=token_data)
    if token_response.status_code != 200:
        return f"Error fetching token: {token_response.text}", token_response.status_code
    token_json = token_response.json()

    try:
        flask_app.logger.info('Add session cookie')
        session['token'] = token_json['access_token']
    except KeyError:
        return 'Access token not found in the response', 500
    return redirect(url_for('index'))

@flask_app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('ranking'))

@flask_app.route('/get-cookie/')
def get_cookie():
    if 'token' in session:
        return 'token'
    else:
        return 'notfound'

# Import my package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'gomoku')))

class NewGameModel(BaseModel):
	mode: str
	main_player: str
	IA_suggestion: bool
	options: dict[str, bool]
	opening: str
	difficulty: str

class MoveModel(BaseModel):
	player_move: dict[str, int]

class TimeoutModel(BaseModel):
	who_timeout: str


app = FastAPI()
router = APIRouter()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=['GET', 'POST'],
	allow_headers=["*"],
)

# @app.get("/")
# async def root():
# 	return {
# 		"response": 200,
# 		"message": "API is working !"
# 	}


all_games: dict[str, Gomoku] = {}

@app.post("/game/new")
async def new_game(body: NewGameModel):
	game_id = str(int(time.time()))
	while all_games.get(game_id) != None:
		game_id += str(random.randint(0, 9))
	print(game_id)
	IA = True if body.mode == "ia" else False
	opts = body.options

	allowed_capture = opts.get("allowed_capture")
	allowed_win_by_capture = opts.get("allowed_win_by_capture")
	allowed_double_three = opts.get("allowed_double_three")

	if allowed_capture is None or allowed_win_by_capture is None or allowed_double_three is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provided options are invalid. Please check the format and try again.")

	if IA == False:
		main_player = "B"
	else:
		main_player = body.main_player

	all_games[game_id] = Gomoku(
		IA=IA,
		IA_suggestion=body.IA_suggestion,
		settings=GomokuSettings(
			allowed_capture=allowed_capture,
			allowed_win_by_capture=allowed_win_by_capture,
			allowed_double_three=allowed_double_three
		),
		main_player=main_player,
		IA_DIFFICULTY=body.difficulty
	)

	board, IA_duration = all_games[game_id].run()
	if board == None:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Sorry, the IA cannot continue the game, you win by forfeit...")

	gomoku = all_games[game_id]
	# board = [
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," ","W"," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," ","W","B"," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," ","W"," ","B","W","W","W","W"," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," ","W","B","B","B","B","W"," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," ","B","B","B","B","B","W"," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," ","W"," "," ","B","B"," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," ","W"," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	# ]
	# gomoku.board = board
	# gomoku.player_turn = "W"
	if gomoku.IA == True:
		message = f"It's your turn !"
	else:
		message = f"It's {'white' if gomoku.get_player_turn() == 'W' else 'black'} turn !"

	if gomoku.IA_suggestion:
		_, move = minimax(gomoku=convert_to_little_gomoku(gomoku), MAX_DEPTH=gomoku.IA_MAX_DEPTH)
		IA_suggestion = (move[1], move[0])
	else:
		IA_suggestion = None


	isPausedPlayer1 = None
	isPausedPlayer2 = None
	if gomoku.IA == True and gomoku.main_player == "W":
		isPausedPlayer1 = False if gomoku.player_turn == "W" else True
		isPausedPlayer2 = False if gomoku.player_turn == "B" else True
	else:
		isPausedPlayer1 = False if gomoku.player_turn == "B" else True
		isPausedPlayer2 = False if gomoku.player_turn == "W" else True
	return {
		"game_id": game_id,
		"player_turn": gomoku.player_turn,
		"isPausedPlayer1": isPausedPlayer1,
		"isPausedPlayer2": isPausedPlayer2,
		"IA_suggestion": IA_suggestion,
		"IA_duration": IA_duration,
		"board": board,
		"black_capture": gomoku.black_capture,
		"white_capture": gomoku.white_capture,
		"player1_capture": gomoku.black_capture if gomoku.main_player == 'B' else gomoku.white_capture,
		"player2_capture": gomoku.black_capture if gomoku.main_player == 'W' else gomoku.white_capture,
		"player1_color": gomoku.main_player,
		"player2_color": "W" if gomoku.main_player == "B" else "B",
		"message": message,
		"difficulty": gomoku.IA_DIFFICULTY
	}


@app.post("/game/{game_id}/IA_response", status_code=status.HTTP_200_OK)
async def IA_response(game_id: str):
	gomoku = all_games[game_id]
	if gomoku is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provided game id is invalid. Please check the game_id and try again.")

	try:
		after_move_dict = gomoku.handle_ia_response()
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

	isPausedPlayer1 = None
	isPausedPlayer2 = None
	if gomoku.IA == True and gomoku.main_player == "W":
		isPausedPlayer1 = False if gomoku.player_turn == "W" else True
		isPausedPlayer2 = False if gomoku.player_turn == "B" else True
	else:
		isPausedPlayer1 = False if gomoku.player_turn == "B" else True
		isPausedPlayer2 = False if gomoku.player_turn == "W" else True
	return {
		"player_turn": gomoku.player_turn,
		"isPausedPlayer1": isPausedPlayer1,
		"isPausedPlayer2": isPausedPlayer2,
		"IA_suggestion": after_move_dict['IA_suggestion'],
		"IA_duration": after_move_dict['IA_duration'],
		"board": gomoku.board,
		"black_capture": gomoku.black_capture,
		"white_capture": gomoku.white_capture,
		"player1_color": gomoku.main_player,
		"player2_color": "W" if gomoku.main_player == "B" else "B",
		"message": after_move_dict['message'],
		"status": after_move_dict['status'],
	}


@app.post("/game/{game_id}/move", status_code=status.HTTP_200_OK)
async def play_move(game_id: str, body: MoveModel):
	gomoku = all_games[game_id]
	if gomoku is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provided game id is invalid. Please check the game_id and try again.")


	x = body.player_move.get("x")
	y = body.player_move.get("y")

	if x is None or y is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provided coordinates are invalid. Please check the coordinates and try again.")

	try:
		after_move_dict = gomoku.apply_move(x, y)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

	isPausedPlayer1 = None
	isPausedPlayer2 = None
	if gomoku.IA == True and gomoku.main_player == "W":
		isPausedPlayer1 = False if gomoku.player_turn == "W" else True
		isPausedPlayer2 = False if gomoku.player_turn == "B" else True
	else:
		isPausedPlayer1 = False if gomoku.player_turn == "B" else True
		isPausedPlayer2 = False if gomoku.player_turn == "W" else True
	return {
		"player_turn": gomoku.player_turn,
		"isPausedPlayer1": isPausedPlayer1,
		"isPausedPlayer2": isPausedPlayer2,
		"IA_suggestion": after_move_dict['IA_suggestion'],
		"IA_duration": after_move_dict['IA_duration'],
		"board": gomoku.board,
		"black_capture": gomoku.black_capture,
		"white_capture": gomoku.white_capture,
		"player1_color": gomoku.main_player,
		"player2_color": "W" if gomoku.main_player == "B" else "B",
		"message": after_move_dict['message'],
		"status": after_move_dict['status'],
		"IA_response": after_move_dict['IA_response'],
	}

@app.post("/game/{game_id}/timeout")
async def timeout(game_id: str, body: TimeoutModel):
	gomoku = all_games[game_id]
	if gomoku is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provided game id is invalid. Please check the game_id and try again.")
	try:
		timeout_dict = gomoku.timeout(body.who_timeout)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


	isPausedPlayer1 = None
	isPausedPlayer2 = None
	if gomoku.IA == True and gomoku.main_player == "W":
		isPausedPlayer1 = False if gomoku.player_turn == "W" else True
		isPausedPlayer2 = False if gomoku.player_turn == "B" else True
	else:
		isPausedPlayer1 = False if gomoku.player_turn == "B" else True
		isPausedPlayer2 = False if gomoku.player_turn == "W" else True

	return {
		"player_turn": gomoku.player_turn,
		"isPausedPlayer1": isPausedPlayer1,
		"isPausedPlayer2": isPausedPlayer2,
		"IA_suggestion": timeout_dict['IA_suggestion'],
		"IA_duration": timeout_dict['IA_duration'],
		"board": gomoku.board,
		"black_capture": gomoku.black_capture,
		"white_capture": gomoku.white_capture,
		"player1_color": gomoku.main_player,
		"player2_color": "W" if gomoku.main_player == "B" else "B",
		"message": timeout_dict['message'],
		"status": timeout_dict['status'],
		"IA_response": timeout_dict['IA_response'],
	}

@app.post("/game/{game_id}/countdown")
async def countdown(game_id: str, body: TimeoutModel):
	gomoku = all_games[game_id]
	if gomoku is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provided game id is invalid. Please check the game_id and try again.")
	final_dict = gomoku.countdown(body.who_timeout)
	return {
		"player_turn": gomoku.player_turn,
		"board": gomoku.board,
		"black_capture": gomoku.black_capture,
		"white_capture": gomoku.white_capture,
		"player1_color": gomoku.main_player,
		"player2_color": "W" if gomoku.main_player == "B" else "B",
		"message": final_dict['message'],
		"status": final_dict['status']
	}

app.mount("/auth", WSGIMiddleware(flask_app))

if __name__ == "__main__":
	from gomoku.main import basic_function
	# import time
	basic_function();
	# for i in range(1200):
	#     print(f"Time : {i}")
	#     time.sleep(1);

