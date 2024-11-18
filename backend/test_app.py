import requests

url = 'https://www.w3schools.com/python/demopage.php'
myobj = {'somekey': 'somevalue'}

game_new_json = {
	"mode": "hotseat",
	"main_player": "B",
	"IA_suggestion": True,
	"options": {
		"allowed_capture": True,
		# "allowed_b"
	}
}

x = requests.post(url, json = myobj)

print(x.text)
