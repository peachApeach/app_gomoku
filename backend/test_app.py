import requests
import time
import datetime

url_new_game = 'http://127.0.0.1:8000/game/new'
# url_move = 'http://127.0.0.1:8000/'

game_new_json = {
	"mode": "hotseat",
	"main_player": "B",
	"IA_suggestion": True,
	"options": {
		"allowed_capture": True,
		"allowed_win_by_capture": True,
		"allowed_double_three": False
	},
	"opening": "standard"
}

game1 = requests.post(url_new_game, json = game_new_json)

print(f"Status : {game1.status_code}")
print(f"Response :")
print(game1.json())
game_id = game1.json()['game_id']

game2 = requests.post(f"http://127.0.0.1:8000/game/{game_id}/move", json={
	"player_move": {"x": 12, "y": 15}
})

print(f"Status : {game2.status_code}")
print(f"Response :")
print(game2.json())
