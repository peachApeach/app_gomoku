# Gomoku API Documentation

## Initialize a game

`POST /game/new` \
Body example :
```json
{
   "board_size": 15,
   "options": "standard",
   "difficulty": "medium"
}
```
Response example:
```json
{
   "game_id": "1",
   "board": [[0, 0, 0, ...], [0, 0, 0, ...], ...]
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
   "player_move": {"x": 7, "y": 7},
   "ai_move": {"x": 8, "y": 7},
   "board": [[0, 0, 0, ...], [0, 0, 0, ...], ...],
   "status": "ongoing"
}
```

## Get moves history

`GET /game/{game_id}/moves` \
In chronological order \
Response example:
```json
{
   "moves": [
      {"player": "player", "move": {"x": 7, "y": 7}},
      {"player": "ai", "move": {"x": 8, "y": 7}},
      ...
   ]
}
```