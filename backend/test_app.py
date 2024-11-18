import requests

url = 'http://127.0.0.1:8000/game/new'

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

x = requests.post(url, json = game_new_json)

print(x.json())
