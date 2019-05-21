import random
import os
import sys

#a hand class to store each hand, and has built in functionality
class Hand:
	def __init__(self, whosHand):
		self.cur_hand = []
		self.person = whosHand

	def hitMe(self, cards):
		newCard, cards = draw_card(cards)
		self.cur_hand.append(newCard)
		return cards
		

	def printHand(self, standing):
		if self.person == 'dealer' and standing:
			print('Dealer cards: [{}] ({})'.format(']['.join(self.cur_hand), calc_hand(self.cur_hand)))
		elif self.person == 'dealer' and not standing:
			print('Dealer cards: [{}][?]'.format(self.cur_hand[0]))
		elif self.person == 'player':
			print('Player cards: [{}] ({})'.format(']['.join(self.cur_hand), calc_hand(self.cur_hand)))

	def handTotal(self):
		return calc_hand(self.cur_hand)

#starts a new set of hands over
def start_game(cards):
	dealerSet = Hand('dealer')
	cards = dealerSet.hitMe(cards)
	cards = dealerSet.hitMe(cards)
	playerList = []
	playerList.append(Hand('player'))
	cards = playerList[0].hitMe(cards)
	cards = playerList[0].hitMe(cards)
	return playerList, dealerSet, cards

#takes the current deck in, tests if it needs to be remade, returns a card and the deck
def draw_card(cards):
	if len(cards) < 1:
		cards = init_deck()
	
	tempCard = cards.pop()
	return tempCard, cards
	
	
#calculates the value of hand
#aces are 11, or 1 if being 11 would cause a bust
def calc_hand(hand):
	sum = 0
	#puts all aces in one list, and none aces in another
	non_aces = [card for card in hand if card != 'A']
	aces = [card for card in hand if card == 'A']
		
	#adds face value or 10 if a J,Q,K
	for card in non_aces:
		if card in 'JQK':
			sum+=10
		else:
			sum+=int(card)
	
	#tests to add either 1 or 11 per ace
	for card in aces:
		if sum <= 10:
			sum+=11
		else:
			sum+=1
	
	return sum

#creates a new shuffled deck to return
def init_deck():
	newDeck = [
			'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
			'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
			'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
			'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
		]
	random.shuffle(newDeck)
	return newDeck

#helper function to determine if bet is ok or not
def valid_bet(curBet, curBalance):
	tempVal = -3 #default value, -3 exits with error
	try:
		tempVal = int(curBet)
		if tempVal > int(curBalance) or tempVal < 1:
			tempVal = -1
	except ValueError:
		if curBet == 'Leave' or curBet == 'leave':
			print('Have a great day!')
			sys.exit()
		else:
			tempVal = -1 #not an int, but also not leave

	if tempVal == -3:
		print('Error in valid_bet')
		sys.exit()
	return tempVal

def split_hand():
	print('#todo')
	return 0

def valid_choice():
	print('#todo')
	return 0

#prints all hands
def printAll(dealer, player, standing):
	dealer.printHand(standing)
	for curHand in player:
		curHand.printHand(standing)
	

balance = 500
cards = []
while True:
	standing = False
	player_hands = 1
	cur_hand = 1
	start_hand = True

	if balance < 1:
		print('You\'re broke!')
		break
	
	print('Current balance: {}'.format(balance))
	bet = input('Place your bet, or exit the game with "Leave": ')
	while valid_bet(bet, balance) == -1:
		bet = input('Please enter a valid bet (greater than 0, at most balance) or leave the game with "Leave": ')


	player, dealer, cards = start_game(cards)
	while True:
		os.system('cls' if os.name == 'nt' else 'clear')
	

		if standing:
			printAll(dealer, player, standing)
			if dealer.handTotal() > 21:
				print('Dealer busted, you win!')
				balance = int(bet) + int(balance)
			elif player[0].handTotal() == dealer.handTotal():
				print('Push! No one wins!')
			elif player[0].handTotal() > dealer.handTotal():
				print('You win!')
				balance = int(bet) + int(balance)
			else:
				print('You lose')
				balance = int(balance) - int(bet)

			break
	
	
		if player[0].handTotal() > 21:
			print('You busted!')
			balance = int(balance) - int(bet)
			break
		
		if start_hand and player[0].handTotal() == 21:
			balance = int(balance) + 1.5*int(bet)
			print('Blackjack, you win!')
			break

		while cur_hand <= player_hands:
			if player[cur_hand-1].handTotal() < 22:
				printAll(dealer, player, standing)
				start_hand = False
				print('What would you like to do?')
				print('[1] Hit')
				print('[2] Stand')
				print('[3] Double Down')
				choice = input('Your choice: ')
		
				while choice != '1' and choice != '2' and choice != '3' or choice == '3' and int(balance) < int(bet) *2:
					print('Please enter a valid choice (you may only double down if you have enough chips!)')
					print('[1] Hit')
					print('[2] Stand')
					print('[3] Double Down')
					choice = input('Your choice: ')	
				if choice == '1':
					player[cur_hand-1].hitMe(cards)
				elif choice == '2':
					print('Standing')
					standing = True
					while dealer.handTotal() <= 16:
						dealer.hitMe(cards)
				elif choice == '3':
					standing = True
					player[cur_hand-1].hitMe(cards)
					bet = int(bet) * 2
					while dealer.handTotal() <= 16:
						dealer.hitMe(cards)
				
			cur_hand+=1
	
		
