# Gomoku API Documentation

## Initialize a game

`POST /game/new` \
Body example :
```json
// 1v1 between 2 players with an IA assistant.
{
   "mode": "hotseat",
   "who_start": "B", // or "W"
   "IA_suggestion": True,
   "options": {
      "allowed_capture": True,
      "allowed_win_by_capture": True,
      "allowed_double_three": False
   },
   "opening": "standard",
   "difficulty": "medium"
}

// 1v1 against a bot
{
   "mode": "ia",
   "who_start": "B",
   "IA_suggestion": False,
   "options": {
      "allowed_capture": True,
      "allowed_win_by_capture": True,
      "allowed_double_three": False
   },
   "opening": "pro",
   "difficulty": "hard"
}

```
Response example:
```json
{
   "game_id": "1",
   "player_turn": "W",
   "IA": True,
   "IA_suggestion": False,
   "board": [
      [' ', ' ', ' ', ...],
      [' ', ' ', ' ', ...],
      ...
   ],
   "message": "..."
}
```

## Play a move

`POST /game/{game_id}/move` \
Body example :
```json
{
   "player_move": {"x": 7, "y": 7}
}
```
Response example:
```json
{
   "player_turn": "B",
   "IA_suggestion": null, // {"x": 8, "y": 7}
   "IA_move": {"x": 8, "y": 7},
   "IA_duration": 99,//xp streamez Jolagreen23
   "board": [
      ["W", "B", " ", ...],
      [" ", " ", " ", ...],
      ...
   ],
   "black_capture": 2,
   "white_capture": 1,
   "message": null,
   "status": "playing"
}
```

## Get moves history

`GET /game/{game_id}/moves` \
In chronological order \
Response example:
```json
{
   "moves": [
      {"player": "B", "move": {"x": 7, "y": 7}, "duration": 4213},
      {"player": "W", "move": {"x": 8, "y": 7}, "duration": 99},
      {"player": "B", "move": {"x": 6, "y": 7}, "duration": 1406},
      {"player": "W", "move": {"x": 1, "y": 8}, "duration": 333},
      ...
   ]
}
```
