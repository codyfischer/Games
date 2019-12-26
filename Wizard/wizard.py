# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 12:39:26 2019

@author: fis0139
"""
import json

save_games_path = "./Saved_Games/"

def check_int(number):
	try:
		int(number)
		return True
	except ValueError:
		return False

# Get Number of players
def get_players():

	bad_input = True
	while bad_input:

	    players = input("\nSelect number of players: ")

	    if check_int(players):
	    	players = int(players)
	    else:
	    	print("Not an integer, try again")
	    	continue

	    #check good input break
	    if players > 6:
	    	print("Too many players, try again.")
	    elif players < 2:
	    	print("Too few players, try again")
	    else:
	    	bad_input = False

	return players

def get_names(num_players):
	players = {}
	for player in range(num_players):
		players[player] = ""
		players[player] = input("\nInput player " + str(player) +  "'s name: ")

	return players

def get_bids(players):

	print("Bids: ")

	bids = {}
	for row, item in players.items():
		bids[row] = int(input("\t" + item + "'s bid: "))

	return bids

def get_overunder(bids, current_round):

	total_bids = 0
	for row, item in bids.items():
		total_bids += bids[item]

	print("\nOver/Under: " + str(total_bids-(current_round+1))+ "\n")

	return total_bids-(current_round+1)

def get_piles(players):

	print("Piles: ")

	piles = {}
	for row, item in players.items():
		piles[row] = int(input("\t" + item + "'s piles: "))

	return piles

def round_scores(current_round, players):

	scores = {}

	for player, item in players.items():
		if current_round["Bids"][player] == current_round["Piles"][player]:
			scores[player] = 20 + current_round["Piles"][player]*10
		else:
			scores[player] = abs(current_round["Bids"][player] - current_round["Piles"][player])*-10

	return scores

def print_scores(game, players):

	print("\nScores: ")
	for player, item in players.items():
		total = 0
		for count in range(len(game)):
			total += game[count]["Scores"][player]
		
		print("\t" + players[player] + ": " + str(total))

def save_game(game, game_name):
	with open(save_games_path + game_name + '.json', 'w') as outfile:
		json.dump(game, outfile, indent=4)

def open_game(game_name):
	with open(save_games_path + game_name + '.json') as json_file:
		game = json.load(json_file)
	return game
# Program Start

def print_gamestats(game):
	None
	#print(game)


print("/////////////////////////////////")
print("Welcome to Wizard")
print("/////////////////////////////////")
print("")

start = int(input("Press 1 to continue an existing game\nPress 2 to start a new game\n"))

if start == 1:
	game_name = input("Enter Game Name: \n")
	game = open_game(game_name)
	#print(game)


elif start == 2:

	game = {}

	game["Game_Name"] = input("\nEnter Game Name: ")

	num_players = get_players()

	game["Players"] = get_names(num_players)

	game["Rounds"] = []


rounds = int(60/len(game["Players"]))

print("\nGame Start: " + str(len(game["Players"])) + " players, " + str(rounds) + " rounds")

#Loop start:
while len(game["Rounds"]) < rounds:
    current_round = {}
    print("\n\n#########")
    print("Round: " + str(len(game["Rounds"]) + 1) + "/" + str(rounds))
    print("#########" + "\n")

    dealer = len(game["Rounds"]) % len(game["Players"])

    print("Dealer: " + game["Players"][dealer] + "\n")
    
    current_round["Dealer"] = dealer
    
    current_round["Bids"] = get_bids(game["Players"])

    current_round["Over/Under"] = get_overunder(current_round["Bids"], len(game["Rounds"]))
    
    current_round["Piles"] = get_piles(game["Players"])

    current_round["Scores"] = round_scores(current_round, game["Players"])

    game["Rounds"].append(current_round)

    save_game(game, game["Game_Name"])

    print_scores(game["Rounds"], game["Players"])



print("Game Over")
    