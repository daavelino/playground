from lib.logic import *
from random import shuffle

from lib.agents import Player, Game, Board

"""
game Clue
https://gamerules.com/rules/clue-board-game/

"""

def play():

    players_name = [
       "1",
       "2",
       "3",
       "4",
       "5",
       ]

    mode = "easy"
    game = Game(players_name, mode)
    game.deal_cards()
    game.flush_deck()
    winner = game.play(smart="1", verbose=True)
#    winner = game.play(verbose=True)
#    winner = game.play()

    print(f"winner: {winner}")

    return winner
    

if __name__=="__main__":
   play()

