import random

# initialise the player's total cards as 0
player_1 = []
player_2 = []

# initialise the deck of cards
cards = [
    ["Red",1],["Red",2],["Red",3],["Red",4],["Red",5],["Red",6],["Red",7],["Red",8],["Red",9],["Red",10],
    ["Black",1],["Black",2],["Black",3],["Black",4],["Black",5],["Black",6],["Black",7],["Black",8],["Black",9],["Black",10],
    ["Yellow",1],["Yellow",2],["Yellow",3],["Yellow",4],["Yellow",5],["Yellow",6],["Yellow",7],["Yellow",8],["Yellow",9],["Yellow",10]
]

# shuffle the deck of cards to be in a random order
shuffled_cards = random.sample(cards,30)

def deal_cards():
    # gives each player the first card on the 
    # .pop removes the card on top so there are no repeats

    player_1.insert(0,shuffled_cards[0])
    shuffled_cards.pop(0)
    player_2.insert(0,shuffled_cards[0])
    shuffled_cards.pop(0)

def player_1_win():
    # takes the card from player 2 and puts it into player 1's deck
    # then it removes player 2's card
    player_1.insert(0,player_2[0])
    player_2.pop(0)
    print("Player 1 is the winner !")

def player_2_win():
    # takes the card from player 1 and puts it into player 2's deck
    # then it removes player 1's card
    player_2.insert(0,player_1[0])
    player_1.pop(0)
    print("Player 2 is the winner !")

def calculate_winner():
    #calculates who won the current round

    # checks if they are the same colour
    if player_1[0][0] == player_2[0][0]:
        print("They are the same colour !")

        # checks if player 1's number is larger than player 2's
        if player_1[0][1] > player_2[0][1]:
            print("Player 1's card is higher than Player 2's !")
            player_1_win()
            return
        
        # since player 1's number does not equal player 2,
        # player 2's number must be less than player 1
        else:
            print("Player 2's card is higher than Player 1's !")
            player_2_win()
            return
    
    # since both cards have different colours, the winner colour is chosen
    # red beats black, black beats yellow, yellow beats red
    if (player_1[0][0] == "Red"):
        if (player_2[0][0] == "Black"):
            player_1_win()
            return
        else:
            player_2_win()
            return

    if (player_1[0][0] == "Black"):
        if (player_2[0][0] == "Yellow"):
            player_1_win()
            return
        else:
            player_2_win()
            return

    if (player_1[0][0] == "Yellow"):
        if (player_2[0][0] == "Red"):
            player_1_win()
            return
        else:
            player_2_win()
            return

# while the deck of cards is not empty
while shuffled_cards != []:
    # give the players all the cards
    deal_cards()
    print("player 1's card: ",player_1[0])
    print("player 2's card: ",player_2[0])
    calculate_winner()
    wait = input("press 'enter' to continue")

# prints the length of both players cards so they can see
print("Player 1 has cards",len(player_1),"cards\n",player_1)
print("Player 2 has cards",len(player_2),"cards\n",player_2)

# if the length of player 1's is greater than player 2 then player 1 wins
if len(player_1) > len(player_2):
    print("PLAYER 1 WINS !!!")
    print(player_1)
else:
    # since the game cannot be drawn, if player 1 has lost then player 2 has won
    # (there are 15 turns and 2 points awarded each turn, meaning someone will always win)
    print("PLAYER 2 WINS !!!")
    print(player_2)
