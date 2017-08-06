# Battleship SyncServer Documentation
=======

## General
------

Every game is represented as an instance of a class that contains the following attributes:


* The game mode: 2-players or 4-players mode expressed as an integer value (2 -> 2-player-mode, 4 -> 4-player-mode)

* Timestamp: When the game was created.

* Current *game_status* -> (*ACTIVE*, *FINISHED*, *WAITING FOR PLAYERS*)

* A list of players containing: the *user_id* of the player, the player's *stats* (points accumulated, current ranking, etc.),
their current map state represented as an integer matrix of fixed dimensions.

* Which user should move next *moves_next*. The order is determined by the order in which each player joins the game.

* (Add other attributes here...)

Since game instance has to be persistent across multiple requests, the game is persisted as a data-structure in REDIS. Each
game can be modified once started, only the user holding the next-player id. This works as a semaphore preventing concurrent
updates of a single resource and as the main synchronization mechanism. A *@check_turn* decorator can be used to decorate
routes + web-method combinations that modify game's state in order to validate and enforce synchronized access to game's state.

[More will be added soon...]

## Server capabilities
------

Battleship SyncServer exposes a set of REST APIs and persistence services that provide the following capabilities:

* Registration of new players in the system

* Authentication of players that allow them to get a JWT access token that most be included in the Authorization header in order to
  send authenticated requests to protected resources.

* Creation of new games in 2-player or 4-player mode.

* List games that are awaiting for players.

* Join games that are awaiting for players.

* Fetch current game's state (update game state and synchronize state across game clients) with simple HTTP GET.

* Perform game actions such as shooting to a specific set of coordinates in a given opponent's board.

* [More will be added soon...]
