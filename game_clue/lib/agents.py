from lib.logic import *
from random import choice, shuffle


class Board():

    envelope = list()

    persons = [
        "Miss Scarlet",
        "Mrs. White",
        "Mrs. Peacock",
        "Professor Plum",
        "Reverend Green",
        "Colonel Mustard"
        ]

    tools = [
        "knife",
        "revolver",
        "rope",
        "wrench",
        "candlestick",
        "lead pipe"
        ]
    
    locations = [
        "Ball Room",
        "Billiard Room",
        "Conservatory",
        "Dining Room",
        "Hall",
        "Kitchen",
        "Lounge",
        "Library",
        "Study"
        ]

    # The corresponding logical symbol for the card decks:
    suspects = [Symbol(x) for x in persons]
    weapons = [Symbol(x) for x in tools]
    rooms = [Symbol(x) for x in locations]

    max_players = len(suspects) - 1

class Player(Board):

    def __init__(self, name):
        """
        name = str()
        suspects = list()
        weapons = list()
        rooms = list()
        """

        self.name = name
        self.next = None

        self.hand = {"suspects": list(), "weapons":list(), "rooms":list()}
        self.my_logic_guess = {"suspects": None, "weapons":None, "rooms":None}
        self.performed_guesses = list()


        #### Initial game knowledge representation:
        self.kb = And()
        self.kb.add(Or(*self.suspects))
        self.kb.add(Or(*self.weapons))
        self.kb.add(Or(*self.rooms))

    def knowledge(self):
        return self.kb.formula()

    def add_hand(self, hand):
        """
        Stores cards information received from the game.
        """
        for key in hand.keys():
            self.hand[key].extend(hand[key])
            for i in hand[key]:
                self.kb.add(Not(i))

    def show_hand(self):
        return self.hand

    def guess(self):

        min_history = 1000

        def random_guess(self):
            guess = {
                "suspects": choice(
                    list(set(self.suspects) - set(self.hand["suspects"]))
                    ),
                "weapons": choice(
                    list(set(self.weapons) - set(self.hand["weapons"]))
                    ),
                "rooms": choice(
                    list(set(self.rooms) - set(self.hand["rooms"]))
                )
                }

            return guess

        guess = random_guess(self)

        # Try a guess not the last min_history repeated ones:
        count = 0
        while count > min_history:
            if guess in self.performed_guesses:
                guess = create_guess(self)
            count = count + 1

        return guess

    def logic_guess(self, **kwargs):
        """
        verbose = False 
        Return a randomly picked logic validated guess.
        """
        guess = {"suspects":None, "weapons":None, "rooms":None}
        for key in self.my_logic_guess.keys():
            if self.my_logic_guess[key] is not None:
                guess[key] = self.my_logic_guess[key]
                continue

            if key == "suspects":
                tmp = list(set(self.suspects) - set(self.hand[key]))
                for i in tmp:
                    valid = model_check(self.kb, i)
                    if valid:
                        self.my_logic_guess[key] = i
                    else:
                        guess[key] = choice(tmp)
            if key == "weapons":
                tmp = list(set(self.weapons) - set(self.hand[key]))
                for i in tmp:
                    valid = model_check(self.kb, i)
                    if valid:
                        self.my_logic_guess[key] = i
                    else:
                        guess[key] = choice(tmp)
            if key == "rooms":
                tmp = list(set(self.rooms) - set(self.hand[key]))
                for i in tmp:
                    valid = model_check(self.kb, i)
                    if valid:
                        self.my_logic_guess[key] = i
                    else:
                        guess[key] = choice(tmp)

        print(f"L: {self.my_logic_guess}")
        print(f"G: {guess}")
        return guess

    def check_guess(self, guess, **kwargs):
        """
        Return the card if the player has or None otherwise.
        """
        verbose = False
        if "verbose" in kwargs.keys():
            verbose = kwargs["verbose"]

        for key in guess.keys():
            if guess[key] in self.hand[key]:
                if verbose:
                    print(f"Player {self.name} has {guess[key]}.")
                return {key:guess[key]}
        if verbose:
            print(f"Player {self.name} has no proofs.")
        return None

    def add_clue(self, clue):
        for key in clue.keys():
            self.kb.add(Not(clue[key]))
            self.hand[key].append(clue[key])



class Game(Board):
   
    players = list()
    modes = ["easy", "hard"]

    def __init__(self, players_name, mode):
        """
        players_name = list()
        mode = str()
        """

        # Setting the game mode:
        self.mode = mode
        if self.mode not in self.modes:
            raise Exception(f"Unrecognized mode ({modes}).")
        
        # Setting the players:
        self.players_num = len(players_name)
        if self.players_num > self.max_players:
            raise Exception("Too many players.")
        for name in players_name:
            self.players.append(Player(name))

        # The card decks:
        self.deck_suspects = self.suspects.copy()
        self.deck_weapons = self.weapons.copy()
        self.deck_rooms = self.rooms.copy()

        shuffle(self.deck_suspects)
        shuffle(self.deck_weapons)
        shuffle(self.deck_rooms)

        # Creating the envelope:
        self.envelope = {
            "suspect": self.deck_suspects.pop(0),
            "weapon": self.deck_weapons.pop(0),
            "rooms": self.deck_rooms.pop(0),
        } 

    def deal_cards(self):
        """
        Distribute the cards on the decks for all the players.
        """

        sus_num = len(self.suspects) - 1

        for player in self.players:
            if self.mode == "easy":
                """
                Equal number of cards is taken from all decks.
                More clues in the first round.
                """

                hand = {
                    "suspects": list(),
                    "weapons": list(),
                    "rooms": list()
                    }

                rounds = sus_num // self.players_num
                for i in range(0, rounds):
                    hand["suspects"].append(self.deck_suspects.pop(0))
                    hand["weapons"].append(self.deck_weapons.pop(0))
                    hand["rooms"].append(self.deck_rooms.pop(0))

                player.add_hand(hand) 
        
            if self.mode == "hard":
                """
                Number of cards taken from the deck depends on its size.
                Less clues in the first round.
                """

                hand = {
                    "suspects": list(),
                    "weapons": list(),
                    "rooms": list()
                    }

                rounds = (len(self.suspects) - 1) // self.players_num
                for i in range(0, rounds):
                    hand["suspects"].append(self.deck_suspects.pop(0))
        
                rounds = (len(self.weapons) - 1) // self.players_num
                for i in range(0, rounds):
                    hand["weapons"].append(self.deck_weapons.pop(0))
       
                rounds = (len(self.rooms) - 1) // self.players_num
                for i in range(0, rounds):
                    hand["rooms"].append(self.deck_rooms.pop(0))

            # Inform players about their hands:
            player.add_hand(hand) 

    def flush_deck(self):
        """
        Inform all the players about the not dealt cards.
        """
        
        remaining_cards = {
            "suspects": self.deck_suspects,
            "weapons": self.deck_weapons,
            "rooms": self.deck_rooms
            }

        # Inform players about the clues:
        for player in self.players:
            player.add_hand(remaining_cards)

    def play(self, **kwargs):
        """
        Returns a clue obtained in the specific round.
        """

        smart = None
        if "smart" in kwargs.keys():
            smart = kwargs["smart"]
        verbose = False
        if "verbose" in kwargs.keys():
            verbose = kwargs["verbose"]

        # Defining who's the next to play:
        shuffle(self.players)
        for i in range(0, len(self.players)):
            next_player = i + 1
            if next_player > len(self.players) - 1:
                next_player = len(self.players) - next_player
            self.players[i].next = self.players[next_player]

        round_no = 1
        clue = False
        while clue is not None:

            if verbose:
                print(f"\nRound {round_no}:")
            turn = self.players[0]
            for player in self.players:

                if player.name == smart:
                    guess = player.logic_guess()
                else:
                    guess = player.guess()

                if verbose:
                    print(f"Player {player.name} guess: {guess}")
                for p in self.players:
                    if p == turn:
                        continue
               
                    clue = p.check_guess(guess, verbose=verbose)
                    if clue is None:
                        continue
                    else:
                        break
        
                if clue is None:
                    if verbose:
                        print(f"Player {player.name} wins!")
                    if verbose:
                        print(f"Envelope: {self.envelope}")
                    return player.name
                
                turn = player.next

            if clue is not False:
                for player in self.players:
                    player.add_clue(clue)

            round_no = round_no + 1



