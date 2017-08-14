# Game Resource (/api/v1/game)

Endpoint: /api/v1/game

## Supported Web Methods

### GET: /api/v1/game/<game_id>

This must be an authenticated request. This operations fetches for the JSON representation of
a game entity. If the provided *game_id* does not exist in the system as a valid/registered
game, then the following structure is returned:

```json

{
  "Error": true,
  "details": "Please enter a valid game id",
  "msg": "Game does not exists"
}

```

### GET: /api/v1/game/

This must be an authenticated request. This operations fetches for the JSON representation of
all availible games:

```json

[
  "b'c5dd52fc-0b5b-42c1-9636-e23cd64c46fd'",
  "b'18f91167-f391-4086-9f56-cf6f4fc713f5'",
  "b'bdee017e-4c43-45b5-b873-c2c9f4156091'",
  "b'49151df3-4786-41da-a001-9c464444f38e'"
]

```

### POST: /api/v1/game/<game_id>/player

This must be an authenticated request. This operations joins a player to a current game using the
following json to join:

```json

{
            "player_type": "HUMAN",
            "board":[
                 [0,0,0,5,5,5,5,5,0,0],
                 [2,2,0,0,0,0,0,0,0,0],
                 [0,0,1,0,0,0,4,0,0,0],
                 [0,0,0,0,0,0,4,0,0,0],
                 [0,0,0,0,0,0,4,0,0,0],
                 [0,0,0,0,0,0,4,0,0,0],
                 [0,0,2,0,1,0,0,0,0,0],
                 [0,0,2,0,0,0,0,0,3,0],
                 [0,0,0,0,0,0,0,0,3,0],
                 [3,3,3,0,0,0,0,0,3,0]
             ]
}

```



The state of this entity is maintained by the sync server and updates to players joining,
game starting, game finishing, etc are managed directly by the backend services which means this is a
read-only entity.


Games are created once a user requests it via the game API.
When registering a new game, the user  must be game type (See game
resource for more details on register new game).