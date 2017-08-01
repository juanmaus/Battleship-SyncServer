# Player resource (/api/v1/player)

Endpoint: /api/v1/player

## Supported Web Methods

### GET: /api/v1/player/<player_id>

This must be an authenticated request. This operations fetches for the JSON representation of
a player entity. If the provided *player_id* does exist in the system as a valid/registered
player, then the following structure is returned:

```json

{
  "player_id":"b2853511-abd7-44a1-bd17-3747041bb31d",
  "player_type":"human",
  "member_since":"2012-04-23T18:25:43.511Z",
  "name": "John",
  "lastname": "Doe",
  "games_played":5,
  "global_ranking_index":4,
  "total_accumulated_points":76
}

```

The state of this entity is maintained by the sync server and updates to ranking positions,
games played, etc are managed directly by the backend services which means this is a 
read-only entity. 


Players are created automatically every time a new user is registered using the account API. 
When registering a new user, the user type (human or computer) must be specified (See account
resource for more details on regis new users). 