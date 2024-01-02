import random
import os
# creates the game, shuffles the deck
class Game:
    uno_deck = [
        ('🟥🟥', 0), ('🟥🟥', 1), ('🟥🟥', 2), ('🟥🟥', 3), ('🟥🟥', 4), ('🟥🟥', 5), ('🟥🟥', 6), ('🟥🟥', 7), ('🟥🟥', 8),
        ('🟥🟥', 9),
        ('🟥🟥', 'Skip'), ('🟥🟥', 'Reverse'), ('🟥🟥', 'Draw Two'),
        ('🟨🟨', 0), ('🟨🟨', 1), ('🟨🟨', 2), ('🟨🟨', 3), ('🟨🟨', 4), ('🟨🟨', 5), ('🟨🟨', 6),
        ('🟨🟨', 7), ('🟨🟨', '8'), ('🟨🟨', 9),
        ('🟨🟨', 'Skip'), ('🟨🟨', 'Reverse'), ('🟨🟨', 'Draw Two'),
        ('🟩🟩', 0), ('🟩🟩', 1), ('🟩🟩', 2), ('🟩🟩', 3), ('🟩🟩', 4), ('🟩🟩', 5), ('🟩🟩', '6'), ('🟩🟩', 7), ('🟩🟩', 8),
        ('🟩🟩', 9),
        ('🟩🟩', 'Skip'), ('🟩🟩', 'Reverse'), ('🟩🟩', 'Draw Two'),
        ('🟦🟦', 0), ('🟦🟦', 1), ('🟦🟦', 2), ('🟦🟦', 3), ('🟦🟦', 4), ('🟦🟦', 5), ('🟦🟦', '6'), ('🟦🟦', 7), ('🟦🟦', 8),
        ('🟦🟦', 9),
        ('🟦🟦', 'Skip'), ('🟦🟦', 'Reverse'), ('🟦🟦', 'Draw Two'),
        ('🌈',), ('🌈',), ('🌈',), ('🌈+4',), ('🌈+4',), ('🌈+4',), ('🌈+4',),
    ]
    random.shuffle(uno_deck)
    players = []
    currentTurn = 0
    currentColor = random.choice(['🟥🟥', '🟨🟨', '🟩🟩', '🟦🟦'])
    currentNumber = random.choice(range(10))
    # clockwise to start the game
    direction = 1
    
    # removes the card from the deck and returns it
    @staticmethod
    def takeCard():
        card = Game.uno_deck[0]
        Game.uno_deck.pop(0)
        return card
    
    # plays the card: removes card from players hand then makes the current color and current number that card
    @staticmethod
    def playCard(player, card_index):
        played_card = player.hand.cards.pop(card_index)
        Game.currentColor, Game.currentNumber = played_card

    # checks to see if the attempted play is valid
    @staticmethod
    def is_valid_play(card):
        if not Game.currentColor or not Game.currentNumber:
            return True
        color, number = card
        return color == Game.currentColor or number == Game.currentNumber

    # changes the turn game direction comes in handy here with reverse cards
    @staticmethod
    def next_turn():
        Game.currentTurn = (Game.currentTurn + Game.direction) % len(Game.players)

    # reverse card action
    @staticmethod
    def reverse_direction():
        Game.direction *= -1

# initializes the hand, and adds 7 cards
class Hand:
    def __init__(self):
        self.cards = []
        for i in range(7):
            self.cards.append(Game.takeCard())

#initializes player setting its name and giving it a hand of cards
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        
    # prints all the players cards in hand
    def show_hand(self):
        print(f"{self.name}'s Hand:")
        for card in self.hand.cards:
            if len(card) == 1:
                print(f"{card[0]}", end=' ')
            else:
                print(f"{card[0]}{card[1]}", end=' ')

# starting screen
print("Welcome to Uno")
player_num = int(input("Enter Player Amount: "))

# creates a player for the desired amount
for i in range(player_num):
    name = input(f"Enter player {i+1}'s Name:")
    player_create = Player(name)
    Game.players.append(player_create)

#clears the console
os.system("cls")

while True:
    current_player = Game.players[Game.currentTurn]# Establish current player
    print(f"{current_player.name}'s Turn")
    print(f"Current Card: {Game.currentColor}, {Game.currentNumber}")
    current_player.show_hand()
    valid_play = False
    # runs until the index selection is valid
    while not valid_play:
        if any(Game.is_valid_play(card) for card in current_player.hand.cards):
            card_index = int(input("Enter the index of the card you want to play (0-6): "))
            if 0 <= card_index < len(current_player.hand.cards):
                selected_card = current_player.hand.cards[card_index]
                if Game.is_valid_play(selected_card):
                    Game.playCard(current_player, card_index)
                    valid_play = True
                else:
                    print("Invalid play")
            else:
                print("Invalid index")
        else:
            print(f"{current_player.name} no valid cards- drawing a card.") # draws a card if player has no valid turn
            current_player.hand.cards.append(Game.takeCard())
    #if there is no longer cards in the players hand that player wins!
    if not current_player.hand.cards:
        print(f"{current_player.name} wins!")
        break
    # checks for action card
    action_card = Game.currentNumber in ['Skip', 'Reverse', 'Draw Two', '🌈+4']
    if action_card:
        if Game.currentNumber == 'Skip':
            Game.next_turn()
        elif Game.currentNumber == 'Reverse':
            Game.reverse_direction()
        elif Game.currentNumber == 'Draw Two':
            next_player = Game.players[(Game.currentTurn + Game.direction) % len(Game.players)]
            for i in range(2):
                next_player.hand.cards.append(Game.takeCard())
            Game.next_turn()
        elif Game.currentNumber == '🌈+4':
            next_player = Game.players[(Game.currentTurn + Game.direction) % len(Game.players)]
            for i in range(4):
                next_player.hand.cards.append(Game.takeCard())
            Game.next_turn()
    else:
        Game.next_turn()

    input("Press Enter to end turn")
    os.system("cls")# clear console once turn finished
