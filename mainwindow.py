
import random
import csv
import creds # imports the hidden key to encrypt
import tkinter as tk



def initialise_game():
    cards = []
    for colour in ["Red", "Black", "Yellow"]:
        for value in range(1, 11):
            cards.append([colour, value])

    # shuffle the deck of cards to be in a random order

    global player_1
    global player_2
    player_1 = []
    player_2 = []
    
    return random.sample(cards,30)

def deal_cards():
    # gives each player the first card on the 
    # .pop removes the card on top so there are no repeats

    player_1.insert(0,shuffled_cards[0])
    shuffled_cards.pop(0)
    player_2.insert(0,shuffled_cards[0])
    shuffled_cards.pop(0)

def calculate_winner():

    # initialises the same colour to be false so the description will not mention it
    # unless important
    same_colour = False
    player_1_higher_number = False

    # checks if they are the same colour
    if player_1[0][0] == player_2[0][0]:
        same_colour = True

        # checks if player 1's number is larger than player 2's
        if player_1[0][1] > player_2[0][1]:
            player_1_higher_number = True
            player_1_winner = True
        
        # since player 1's number does not equal player 2,
        # player 2's number must be less than player 1
        else:
            player_1_higher_number = False
            player_1_winner = False
    
    # since both cards have different colours, the winner colour is chosen
    # red beats black, black beats yellow, yellow beats red
    if (player_1[0][0] == "Red"):
        if (player_2[0][0] == "Black"):
            player_1_winner = True
        else:
            player_1_winner = False


    if (player_1[0][0] == "Black"):
        if (player_2[0][0] == "Yellow"):
            player_1_winner = True
        else:
            player_1_winner = False

    if (player_1[0][0] == "Yellow"):
        if (player_2[0][0] == "Red"):
            player_1_winner = True
        else:
            player_1_winner = False
    return same_colour, player_1_higher_number, player_1_winner

def get_second_column(row):
    # returns the second item in the row
    return row[1]   

def database_sort():
    # read the csv file into a list of rows
    with open("user profile database.csv", "r") as csvfile:
        rows = list(csv.reader(csvfile, delimiter="|"))
    
    # sorts the rows based on the second column
    sorted_rows = sorted(rows[1:], key=get_second_column, reverse=True)
    # possible alternate solution:
    # sorted_rows = sorted(rows[1:], key=lambda x: x[1], reverse=True)
    with open("user profile database.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter="|")
        writer.writerows([rows[0]] + sorted_rows)

def encrypt_decrypt(password):
    password = password.rstrip('\n')
    result = ""
    for i in range(len(password)):
        result += chr(ord(password[i]) ^ ord(creds.key[i]))
    return result

def check_username_exists(username):
    # takes the username and if the username is found within the database then returns true, otherwise returns false
    with open("authentication database.csv", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter="|")
        for row in reader:
            if (row[0]).lower() == username.lower():
            # if the lowercase of the first value of the table (name) is the same as the lowercase input
                return True
    return False

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



class Window(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Card Game")
        self.geometry("650x600")

        self.home_title_text = tk.Label(self, text="Card Game Program",font=("Arial",18))
        self.home_title_text.pack(pady=2)
        self.home_subtitle_text = tk.Label(self, text="Please Login / Register to play",font=("Arial",12))
        self.home_subtitle_text.pack(pady=2)
        self.home_login_button = tk.Button(self,text="Login",command=self.show_login_page)
        self.home_login_button.pack(pady=2)
        self.home_register_button = tk.Button(self,text="Register",command=self.show_register_page)
        self.home_register_button.pack(pady=2)

        self.error_label = tk.Label(self, text="error", font=("Arial", 12))
        self.space_label = tk.Label(self, text="")


    def hide(self):
        for widget in self.winfo_children():
            widget.pack_forget()


    def show_home_page(self):
        self.hide()

        global player_1_logged_in

        self.home_title_text.pack(pady=2)
        self.home_subtitle_text.pack(pady=2)
        self.home_login_button.pack(pady=2)
        if player_1_logged_in == True:
            self.home_register_button.config(state="disabled")
        else:
            self.home_register_button.config(state="normal")
        self.home_register_button.pack(pady=2)


    def show_login_page(self):
        self.hide()

        self.login_title_text = tk.Label(self, text="Please Login", font=("Arial", 18))
        self.login_title_text.pack(pady=2)

        self.login_username_label = tk.Label(self, text="Username:")
        self.login_username_label.pack(pady=2)
        self.login_username_entry = tk.Entry(self)
        self.login_username_entry.pack(pady=2)

        self.login_password_label = tk.Label(self, text="Password:")
        self.login_password_label.pack(pady=2)
        self.login_password_entry = tk.Entry(self, show="*")
        self.login_password_entry.pack(pady=2)

        self.login_submit_button = tk.Button(self, text="Login", command=self.submit_login)
        self.login_submit_button.pack(pady=2)

        self.space_label.pack(pady=5)

        self.go_back_button = tk.Button(self, text="Go Back", command=self.show_home_page)
        self.go_back_button.pack(pady=2)


    def submit_login(self):
        global player_1_logged_in
        global player_2_logged_in
        global player_1_name
        global player_2_name

        # Get the username and password entered by the user
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        # Check if the account is already logged in
        if username == player_1_name:
            self.error_label.config(text="Account already logged in !")
            self.error_label.pack(pady=2)   
            return

        # Encrypt the password and convert it to hex format
        password = encrypt_decrypt(password).encode().hex()

        # Open the authentication database and check if the username and password match any records
        with open("authentication database.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter="|")
            next(reader) # skip the first row
            username_found = False
            for row in reader:
                if (row[0] == username) and (row[1] == password):
                    username_found = True
                    
                    # If player 1 is already logged in, log in player 2 instead
                    if player_1_logged_in == True:
                        player_2_logged_in = True
                        player_2_name = username

                    # If player 1 is not logged in, log them in
                    if player_1_logged_in == False:
                        player_1_logged_in = True
                        player_1_name = username
                    
                    # Call the show_game_page() function
                    self.show_game_page()

                    
            # If the username and password do not match any records, display an error message
            if username_found == False:
                self.error_label.config(text="Sorry, incorrect credentials !")
                self.error_label.pack(pady=2)


    def show_register_page(self):
        self.hide()

        self.register_title_text = tk.Label(self, text="Please Register", font=("Arial", 18))
        self.register_title_text.pack(pady=2)

        self.register_username_label = tk.Label(self, text="Username:")
        self.register_username_label.pack(pady=2)
        self.register_username_entry = tk.Entry(self)
        self.register_username_entry.pack(pady=2)

        self.register_password_label = tk.Label(self, text="Password:")
        self.register_password_label.pack(pady=2)
        self.register_password_entry = tk.Entry(self, show="*")
        self.register_password_entry.pack(pady=2)

        self.register_submit_button = tk.Button(self, text="Register", command=self.submit_register)
        self.register_submit_button.pack(pady=2)

        self.space_label = tk.Label(self, text="")
        self.space_label.pack(pady=5)

        self.go_back_button = tk.Button(self, text="Go Back", command=self.show_home_page)
        self.go_back_button.pack(pady=2)


    def submit_register(self):
        #Function to handle registration form submission
        
        # Get the username entered by the user
        username = self.register_username_entry.get()

        # Check if the username contains only alphanumeric characters
        # If not, display an error message and return
        if not username.isalnum():
            self.error_label.config(text="Please only use A-Z and 0-9 in your username !")
            self.error_label.pack(pady=2)
            return
        # Check if the username already exists in the database
        # If yes, display an error message and return
        elif check_username_exists(username):
            self.error_label.config(text="Sorry, this username already exists !")
            self.error_label.pack(pady=2)
            return
        # Check if the length of the username is between 3 and 24 characters
        # If not, display an error message and return
        elif (len(username) < 3) or (len(username) > 24):
            self.error_label.config(text="Username must be 3-24 characters long !")
            self.error_label.pack(pady=2)
            return
        # If all checks pass, convert the username to lowercase
        else:
            username.lower()

        # Get the password entered by the user
        password = self.register_password_entry.get()

        # Check if the length of the password is at least 4 characters
        # If not, display an error message and return
        if (len(password) < 4):
            self.error_label.config(text="Password is too short !\nPlease make it more than 3 characters long")
            self.error_label.pack(pady=2)
            return
        # Check if the length of the password is less than 30 characters
        # If not, display an error message and return
        elif (len(password) > 30):
            self.error_label.config(text="Password is too long !\nPlease make it less than 30 characters long")
            self.error_label.pack(pady=2)
            return

        # Encrypt the password using a simple encryption function and encode it as hexadecimal
        password = encrypt_decrypt(password).encode().hex()

        # Create a list of the username and encrypted password
        data = [username,password]

        # Write the data to a CSV file for authentication
        with open("authentication database.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter="|")
            writer.writerow(data)

        # Show the game page
        self.show_game_page()


    def show_game_page(self):
        global player_2_logged_in

        self.hide()

        self.game_title_text = tk.Label(self, text="Welcome to the Card Game !",font=("Arial",18))
        self.game_title_text.pack(pady=2)

        self.game_gameplay_button = tk.Button(self,text="Play Game",command=self.show_gameplay_page)
        self.game_gameplay_button.pack(pady=2)

        if player_2_logged_in == False:
            self.game_addplayer_button = tk.Button(self,text="Add Player 2",command=self.show_home_page)
            self.game_addplayer_button.pack(pady=2)
        elif player_2_logged_in == True:
            self.game_addplayer_button.forget()

        self.game_howtoplay_button = tk.Button(self,text="How to Play",command=self.show_howtoplay_page)
        self.game_howtoplay_button.pack(pady=2)

        self.game_leaderboard_button = tk.Button(self,text="Leaderboard",command=self.show_leaderboard_page)
        self.game_leaderboard_button.pack(pady=2)

        self.space_label.pack(pady=5)

        self.game_logout_button = tk.Button(self,text="Logout",command=self.logout)
        self.game_logout_button.pack(pady=2)


    def logout(self):
        global player_1_logged_in
        global player_2_logged_in
        global player_1_name
        global player_2_name

        player_1_logged_in = False
        player_2_logged_in = False
        player_1_name = ""
        player_2_name = "Computer"
    
        self.show_home_page()


    def show_gameplay_page(self):
        self.hide()

        self.gameplay_cardsleft_text = tk.Label(self, text="Cards left: 30",font=("Arial",18))
        self.gameplay_cardsleft_text.pack(pady=2)
        
        self.gameplay_playerscards_text = tk.Label(self, text="",font=("Arial",18))
        self.gameplay_playerscards_text.pack(pady=2)

        self.gameplay_description_text = tk.Label(self, text="Press Next",font=("Arial",18))
        self.gameplay_description_text.pack(pady=2)

        self.gameplay_update_button = tk.Button(self, text="next", command=self.gameplay_update)
        self.gameplay_update_button.pack(pady=2)
        
        global shuffled_cards    
        
        shuffled_cards = initialise_game()

        self.gameplay_update()


    def gameplay_update(self):

        global shuffled_cards
        global player_1
        global player_2 
        global winner  
        global winning_cards

        if len(shuffled_cards) == 0:
            if len(player_1) > len(player_2):
                winner = player_1_name
                winning_cards = player_1
            else:
                if player_2_name != "Computer":
                    winner = player_2_name
                    winning_cards = player_2
                else:
                    winner = "Computer"
                    winning_cards = player_2
            self.show_end_page()
            return
        
        deal_cards()
        same_colour, player_1_higher_number, player_1_winner = calculate_winner()
        
        description = ""
        if same_colour == True:
            description += "Both cards are the same colour\n"

            if player_1_higher_number == True:
                description += f"{player_1_name} has a higher number"
            else:
                description += f"{player_2_name} has a higher number"
        else:
            if player_1_winner == True:
                description += f"{player_1_name} is the winner\n"

            else:
                description += f"{player_2_name} is the winner\n"

        cards_left = "Cards left: "+ str(len(shuffled_cards))
        if len(shuffled_cards) == 30:
            playerscards = f"{player_1_name} : {player_2_name}\n"
        else:
            playerscards = f"{player_1_name} : {player_2_name}\n{player_1[0][0]} {player_1[0][1]} : {player_2[0][0]} {player_2[0][1]}"

        self.gameplay_description_text.config(text=description)
        self.gameplay_cardsleft_text.config(text=cards_left)
        self.gameplay_playerscards_text.config(text=playerscards)

        if player_1_winner == True:
            player_1.insert(0,player_2[0])
            player_2.pop(0)

        else:
            player_2.insert(0,player_1[0])
            player_1.pop(0)


    def show_end_page(self):
        self.hide()

        global winner
        global winning_cards
        
        self.end_gameplay_description = tk.Label(self,text=f"Congrats {winner}!",font=("Arial",16))
        self.end_gameplay_description.pack(pady=2)

        self.leaderboard_score_text = tk.Label(self, text=f"They scored {len(winning_cards)}\nScroll to see their cards:",font=("Arial",12))
        self.leaderboard_score_text.pack(pady=2)

        listbox = tk.Listbox(self, width=20, height=10)
        for i in winning_cards:
            listbox.insert(tk.END, i)
        listbox.pack()

        self.leaderboard_subtitle_text = tk.Label(self, text="\nHere are the top 5 highest scores:",font=("Arial",12))
        self.leaderboard_subtitle_text.pack(pady=2)

        if winner != "Computer":
            insert_into_database([winner,len(winning_cards),winning_cards])
            database_sort()
        
        with open("user profile database.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter="|")
            next(reader) # skip the first row
            lines = []
            for row in reader:
                lines.append(row)

        rank1 = "1. " + str(lines[0][0]) + ": " + str(lines[0][1]) + "\n"
        rank2 = "2. " + str(lines[1][0]) + ": " + str(lines[1][1]) + "\n"
        rank3 = "3. " + str(lines[2][0]) + ": " + str(lines[2][1]) + "\n"
        rank4 = "4. " + str(lines[3][0]) + ": " + str(lines[3][1]) + "\n"
        rank5 = "5. " + str(lines[4][0]) + ": " + str(lines[4][1]) + "\n"

        leaderboard_ranks = rank1 + rank2 + rank3 + rank4 + rank5

        self.leaderboard_list_text = tk.Label(self, text=leaderboard_ranks, font=("Arial", 20))
        self.leaderboard_list_text.pack(pady=2)

        self.space_label.pack(pady=5)

        self.show_game_page_button = tk.Button(self,text="Play again",command=self.show_game_page)
        self.show_game_page_button.pack(pady=2)

        self.game_logout_button = tk.Button(self,text="Logout",command=self.logout)
        self.game_logout_button.pack(pady=2)


    def show_howtoplay_page(self):
        self.hide()

        self.howtoplay_title_text = tk.Label(self, text="How to Play",font=("Arial",18))
        self.howtoplay_title_text.pack(pady=2)
        self.howtoplay_subtitle_text = tk.Label(self, text="The game has a deck of 30 unique cards.\nThere are 3 card colours (red, black or yellow)\nand each card has a number (1, 2, 3, 4, 5, 6, 7, 8, 9, 10).\nThe 30 cards are then shuffled and stored in the deck.\n\n\nThe rules:\nPlayer 1 takes the top card from the deck\nand Player 2 takes the next card.\n\nIf both players have the same card colour:\nThe player with the highest number wins.\n\nIf both players have different card colours, the winning colour is shown below:\nRED beats BLACK\nYELLOW beats RED\nBLACK beats YELLOW\n\nThe winner of each round keeps both players cards\nand the players keep playing until there are no more cards left",font=("Arial",12))
        self.howtoplay_subtitle_text.pack(pady=2)

        self.space_label.pack(pady=5)

        self.go_back_to_game_button = tk.Button(self, text="Go Back", command=self.show_game_page)
        self.go_back_to_game_button.pack(pady=2)


    def show_leaderboard_page(self):
        self.hide()

        self.leaderboard_title_text = tk.Label(self, text="Leaderboard",font=("Arial",18))
        self.leaderboard_title_text.pack(pady=2)

        self.leaderboard_subtitle_text = tk.Label(self, text="Here are the top 5 highest scores:",font=("Arial",12))
        self.leaderboard_subtitle_text.pack(pady=2)

        with open("user profile database.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter="|")
            next(reader) # skip the first row
            lines = []
            for row in reader:
                lines.append(row)

        rank1 = "1. " + str(lines[0][0]) + ": " + str(lines[0][1]) + "\n"
        rank2 = "2. " + str(lines[1][0]) + ": " + str(lines[1][1]) + "\n"
        rank3 = "3. " + str(lines[2][0]) + ": " + str(lines[2][1]) + "\n"
        rank4 = "4. " + str(lines[3][0]) + ": " + str(lines[3][1]) + "\n"
        rank5 = "5. " + str(lines[4][0]) + ": " + str(lines[4][1]) + "\n"

        leaderboard_ranks = rank1 + rank2 + rank3 + rank4 + rank5

        self.leaderboard_list_text = tk.Label(self, text=leaderboard_ranks, font=("Arial", 20))
        self.leaderboard_list_text.pack(pady=2)


        self.space_label.pack(pady=5)

        self.go_back_to_game_button = tk.Button(self, text="Go Back", command=self.show_game_page)
        self.go_back_to_game_button.pack(pady=2)

# program starts
player_1_logged_in = False
player_2_logged_in = False

player_1_name = ""
player_2_name = "Computer"

window = Window()
window.mainloop()

