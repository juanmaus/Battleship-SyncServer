#!/usr/bin/python
# -*- coding: utf-8 -*-
# run.py
import os
from battleshipsync import app

"""
    BattleShip-SyncServer is a REST-Compliant web service for playing Battleships, extending Garnet(https://github.com/OneTesseractInMultiverse/Garnet) as a base.
    Further documentation can be found in the docs folder, on how to use the endpoints.
    Server is based on a owner-player principle, so, in order to make a player, you must first create a account using the instructions below.
"""

__author__ = "To be set"
__version__ = "1.0"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run('127.0.0.1', port)
