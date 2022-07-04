from lib.logic import *
from random import choice, shuffle
from threading import Thread

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
        """

        self.name = name
        self.next = None

        self.hand = {"suspects": list(), "weapons":list(), "rooms":list()}
        self.my_smart_guess = {"suspects": None, "weapons":None, "rooms":None}
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

    def guess(self, **kwargs):

        verbose = False
        if "verbose" in kwargs.keys():
            verbose = kwargs["verbose"]

        min_history = 100

        def random_guess(self):
            guess = {
                "suspects": choice(
                    list(
                      set(self.suspects) 
                    - set(self.hand["suspects"]))
                    ),
                "weapons": choice(
                    list(
                      set(self.weapons) 
                    - set(self.hand["weapons"]))
                    ),
                "rooms": choice(
                    list(
                      set(self.rooms) 
                    - set(self.hand["rooms"]))
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

        if verbose:
            print(f"Player {self.name} guess: {guess}")

        return guess

    def smart_guess(self, **kwargs):
        """
        verbose = False 
        Return a logic validated guess.
        """
        verbose = False
        if "verbose" in kwargs.keys():
            verbose = kwargs["verbose"]

        def check_symbols(self, key, symbols):
            """ 
            key = str()
            symbols = list()
            """
            for symbol in symbols:
                valid = model_check(self.kb, Or(symbol))
                if valid:
                    self.kb.add(symbol)
                    self.my_smart_guess[key] = symbol
                    break

        # The player knows for sure the answer:
        if not None in self.my_smart_guess.values():
            if verbose:
                print(f"Player {self.name} (smart) guess: {self.my_smart_guess}")
            return self.my_smart_guess
      
        guess = {"suspects": None, "weapons":None, "rooms": None}

        symbols = {
            "suspects": list(
                set(self.suspects) 
                - set(self.hand["suspects"]) 
           ),
            "weapons": list(
              set(self.weapons) 
            - set(self.hand["weapons"]) 
            ),
            "rooms": list(
              set(self.rooms) 
            - set(self.hand["rooms"]) 
            )
        }

        # Smart guess for some items:
        t = dict()
        for key in symbols:
            s = symbols[key]
            if self.my_smart_guess[key] is not None:
                guess[key] = self.my_smart_guess[key]
            else:
                t[key] = Thread(target=check_symbols, args=(self, key, s,))
                t[key].start()

        for key in t.keys():
           t[key].join()

        for key in symbols.keys():
            symbol = self.my_smart_guess[key]
            if symbol is not None:
                guess[key] = symbol
            else:
                guess[key] = choice(symbols[key])
 
        if verbose:
            print(f"Player {self.name} (smart) guess: {guess}")
        
        return guess

    def check_guess(self, guess, **kwargs):
        """
        Return the card if the player has or False otherwise.
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
            print(f"Player {self.name} has no evidence.")

        return False

    def add_clue(self, clue):
        for key in clue.keys():
            self.kb.add(Not(clue[key]))
            
            if self.my_smart_guess[key] == clue[key]:
                self.my_smart_guess[key] = None

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
        if self.players_num < 2:
            raise Exception("Too few players.")

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
            if next_player >= len(self.players):
                next_player = len(self.players) - next_player
            self.players[i].next = self.players[next_player]

        # Running the game round:
        round_no = 1
        player = self.players[0]
        while True:

            if verbose:
                print(f"\nRound {round_no}:")

            # Each player makes a guess:
            for player in self.players:
                if player.name == smart:
                    guess = player.smart_guess(verbose=verbose) 
                else:
                    guess = player.guess(verbose=verbose)

                # The other players check the guess:
                for p in self.players:
                    if p.name == player.name:
                        continue
             
                    guess_checker = list() 
                    # check_guess() returns the "proof" or False:
                    clue = p.check_guess(guess, verbose=verbose)
                    if clue:
                        guess_checker.append("has")
                        # Inform all players about the new clue:
                        for player in self.players:
                            player.add_clue(clue)
                        break
                    else:
                        guess_checker.append("not")
      
                # The game checks if we have a winner:
                if "has" not in guess_checker:
                    if verbose:
                        print(f"Player {player.name} wins!")
                        print(f"Envelope: {self.envelope}")
                    return player.name

            # The next player in turn plays:
            player = player.next
            round_no = round_no + 1



