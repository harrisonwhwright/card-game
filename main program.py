# THINGS I NEED TO ADD:
# DATABASE TO HOLD USERNAME AND PASSWORD RATHER THAN STORING IT IN THE DATABSE !!
# CHECK IN register() TO SEE IF A USERNAME IS ALREADY TAKEN
# insert password into AUTH database

import random
import csv
import hashlib
import creds # imports the hidden key to encrypt

def print_border():
    print("+=--- --+-- ---=+")

def login():
    username = ""
    password = ""
    while username == "":
        username = input("What is your username ? ")
    while password == "":
        password = input("What is your password ? ")
        password = encrypt_decrypt(password).encode().hex()
    print("\n")
    return username

def register():
    username = ""
    password = ""
    while username == "":
        username = input("What is your username ? ")
    while password == "":
        password = input("What is your password ? ")
        password = encrypt_decrypt(password).encode().hex()
    print("\n")
    
    data = [username,password]
    print(data)
    with open("authentication database.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter="|")
        writer.writerow(data)

    return username

def insert_into_database(data):
    with open("user profile database.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter="|")
        writer.writerow(data)

    with open("user profile database.csv", 'r') as f:
        lines = f.readlines()
    rows = [line.strip().split('|') for line in lines]
    sorted_rows = sorted(rows[1:], key=lambda row: row[2], reverse=True)
    sorted_lines = [rows[0]] + sorted_rows
    sorted_contents = ['|'.join(row) + '\n' for row in sorted_lines]
    with open("user profile database.csv", 'w') as f:
        f.writelines(sorted_contents)

def display_leaderboard():
    print_border()
    print("LEADERBOARD:")
    with open("user profile database.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter="|")
        next(reader) # skip the first row
        lines = []
        for row in reader:
            lines.append(row)
        for i in range (0,5):
            print(str(lines[i][0])+":",lines[i][2])
    print_border()
    print()

def encrypt_decrypt(password):
    password = password.rstrip('\n')
    result = ""
    for i in range(len(password)):
        result += chr(ord(password[i]) ^ ord(creds.key[i]))
    return result

#to decrypt the password
#password = bytes.fromhex(password)
#password = password.decode()
#encrypt_decrypt(password)
#print(password)

def initialise_deck():
    
    # initialise the player's total cards as 0
    global player_1
    global player_2
    player_1 = []
    player_2 = []

    # initialise the deck of cards
    cards = [
    ["Red",1],["Red",2],["Red",3],["Red",4],["Red",5],["Red",6],["Red",7],["Red",8],["Red",9],["Red",10],
    ["Black",1],["Black",2],["Black",3],["Black",4],["Black",5],["Black",6],["Black",7],["Black",8],["Black",9],["Black",10],
    ["Yellow",1],["Yellow",2],["Yellow",3],["Yellow",4],["Yellow",5],["Yellow",6],["Yellow",7],["Yellow",8],["Yellow",9],["Yellow",10]
    ]

    # shuffle the deck of cards to be in a random order
    return random.sample(cards,30)

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
    print(f"{player_1_name} is the winner !")

def player_2_win():
    # takes the card from player 1 and puts it into player 2's deck
    # then it removes player 1's card
    player_2.insert(0,player_1[0])
    player_1.pop(0)
    print(f"{player_2_name} is the winner !")

def calculate_winner():
    #calculates who won the current round

    # checks if they are the same colour
    if player_1[0][0] == player_2[0][0]:
        print("They are the same colour !")

        # checks if player 1's number is larger than player 2's
        if player_1[0][1] > player_2[0][1]:
            print(f"{player_1_name}'s card is higher than {player_2_name}'s !")
            player_1_win()
            return
        
        # since player 1's number does not equal player 2,
        # player 2's number must be less than player 1
        else:
            print(f"{player_2_name}'s card is higher than {player_1_name}'s !")
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

def start_game():
    display_leaderboard()

    global shuffled_cards
    shuffled_cards = initialise_deck()

    # while the deck of cards is not empty
    while shuffled_cards != []:
        # give the players all the cards
        deal_cards()
        print(f"{player_1_name}'s card: ",player_1[0][0],player_1[0][1])
        print(f"{player_2_name}'s card: ",player_2[0][0],player_2[0][1])
        calculate_winner()
        input("press 'enter' to continue\n")

    # prints the length of both players cards so they can see
    print(f"{player_1_name} has ",len(player_1),"cards\n")
    print(f"{player_2_name} has ",len(player_2),"cards\n")

    # if the length of player 1's is greater than player 2 then player 1 wins
    if len(player_1) > len(player_2):
        print(f"{player_1_name} WINS !!!")
        insert_into_database([player_1_name,len(player_1),player_1])
    else:
        # since the game cannot be drawn, if player 1 has lost then player 2 has won
        # (there are 15 turns and 2 points awarded each turn, meaning someone will always win)
        print(f"{player_2_name} WINS !!!")
        if num_players == 2:
            insert_into_database([player_2_name,len(player_2),player_2])

    print("Would you like to play again?\n(Y/N)")
    answer = input()
    if answer.lower() == "y":
        start_game()
    else:
        print("Goodbye !!")


# THIS IS THE START OF THE PROGRAM !!!

num_players = 0
while (num_players < 1) or (num_players > 2):
    num_players = int(input("How many players are playing? (1-2): "))

print("login or register?")
answer = input()
if answer.lower() == "login":
    player_1_name= login()
elif answer.lower() == "register":
    player_1_name = register()
player_2_name = "Computer"
if num_players == 2:
    print("PLAYER 2 please login")
    player_2_name = login()
start_game()
