from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from flask import Flask, redirect, url_for, request, session, render_template
import logging
from flask_session import Session
import requests
import sys
import os

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
REDIRECT_URI = 'http://127.0.0.1:8000/auth/callback'

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

# Import my package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'gomoku')))

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None

class NewGameModel(BaseModel):
	mode: str
	main_player: str
	IA_suggestion: bool
	options: dict[str, bool]
	opening: str

class MoveModel(BaseModel):
	player_move: dict[str, int]
	pass

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

@app.post("/game/new")
async def new_game(body: NewGameModel):
	return {
		'response': "cool"
	}

@app.post("/game/{game_id}/move")
async def play_move(game_id: int, body: MoveModel):
	pass

@app.post("/game/{game_id}/timeout")
async def timeout(game_id: int, body: TimeoutModel):
	pass

app.mount("/auth", WSGIMiddleware(flask_app))

if __name__ == "__main__":
	from gomoku.main import basic_function
	# import time
	basic_function();
	# for i in range(1200):
	#     print(f"Time : {i}")
	#     time.sleep(1);

