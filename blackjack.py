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

	def splitAdd(self, new_card):
		self.cur_hand.append(new_card)

	def splitDelete:
		return self.cur_hand.pop()

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
			'2\u2663', '3\u2663', '4\u2663', '5\u2663', '6\u2663', '7\u2663', '8\u2663', '9\u2663', '10\u2663', 'J\u2663', 'Q\u2663', 'K\u2663', 'A\u2663',
			'2\u2660', '3\u2660', '4\u2660', '5\u2660', '6\u2660', '7\u2660', '8\u2660', '9\u2660', '10\u2660', 'J\u2660', 'Q\u2660', 'K\u2660', 'A\u2660',
			'2\u2666', '3\u2666', '4\u2666', '5\u2666', '6\u2666', '7\u2666', '8\u2666', '9\u2666', '10\u2666', 'J\u2666', 'Q\u2666', 'K\u2666', 'A\u2666',
			'2\u2665', '3\u2665', '4\u2665', '5\u2665', '6\u2665', '7\u2665', '8\u2665', '9\u2665', '10\u2665', 'J\u2665', 'Q\u2665', 'K\u2665', 'A\u2665'
		]
	random.shuffle(newDeck)
	return newDeck

#helper function to determine if bet[0] is ok or not
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
		print('Error in valid_bet[0]')
		sys.exit()
	return tempVal

def split_hand(player, cards, this_hand, total_hands):
	player.append(Hand('player'))
	total_hands+=1
	player[total_hands-1].splitAdd(player[this_hand-1].splitDelete())
	player[total_hands-1].hitMe(cards)
	player[this_hand-1].hitMe(cards)
	return player, cards, total_hands

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
	
	bet = []
	print('Current balance: {}'.format(balance))
	bet.append(input('Place your bet, or exit the game with "Leave": '))
	while valid_bet(bet[0], balance) == -1:
		bet[0] = input('Please enter a valid bet[0] (greater than 0, at most balance) or leave the game with "Leave": ')


	player, dealer, cards = start_game(cards)
	while True:
		os.system('cls' if os.name == 'nt' else 'clear')
	

		if standing:
			printAll(dealer, player, standing)
			if dealer.handTotal() > 21:
				print('Dealer busted, you win!')
				balance = int(bet[0]) + int(balance)
			elif player[0].handTotal() == dealer.handTotal():
				print('Push! No one wins!')
			elif player[0].handTotal() > dealer.handTotal():
				print('You win!')
				balance = int(bet[0]) + int(balance)
			else:
				print('You lose')
				balance = int(balance) - int(bet[0])

			break
	
	
		if player[0].handTotal() > 21:
			print('You busted!')
			balance = int(balance) - int(bet[0])
			break
		
		if start_hand and player[0].handTotal() == 21:
			balance = int(balance) + 1.5*int(bet[0])
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
				print('[4] Split')
				choice = input('Your choice: ')
		
				while choice != '1' and choice != '2' and choice != '3' and choice != '4' or choice == '4' and int(balance) < (int(totalBet) + int(bet[cur_hand-1])) or choice == '3' and int(balance) < int(bet[cur_hand-1]) *2:
					print('Please enter a valid choice (you may only double down if you have enough chips!)')
					print('[1] Hit')
					print('[2] Stand')
					print('[3] Double Down')
					print('[4] Split')
					choice = input('Your choice: ')	
				if choice == '1':
					player[cur_hand-1].hitMe(cards)
					break
				elif choice == '2':
					print('Standing')
					standing = True
					while dealer.handTotal() <= 16:
						dealer.hitMe(cards)
					break
				elif choice == '3':
					standing = True
					player[cur_hand-1].hitMe(cards)
					bet[cur_hand-1] = int(bet[cur_hand-1]) * 2
					while dealer.handTotal() <= 16:
						dealer.hitMe(cards)
					break
				elif choice == '4':
					print('Split detected')

					break
					
				
			cur_hand+=1
	
		
