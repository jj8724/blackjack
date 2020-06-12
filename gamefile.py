import random

# define tuples for suits and ranks, dictionary for values
suits = ('Spades','Clubs','Hearts','Diamonds')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,
          'Queen':10,'King':10,'Ace':11}

# for while loop later
playing = True

# define Card class consisting of a suit and rank
class Card:
    
    def __init__(self,suit,rank):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

# define a deck class consisting of cards
class Deck:
    
    # create a card for each rank in each suit and add it to a list
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deckstr = ''
        for item in self.deck:
            deckstr += '\n'+item.__str__()
        return 'The deck contains:'+deckstr
    
    # shuffle the deck
    def shuffle(self):
        random.shuffle(self.deck)
        
    # deal a card and remove it from the list of cards
    def deal(self):
        single_card = self.deck.pop()
        return single_card

# define a hand class for each player consisting of a list of cards, the value and a counter for number of aces
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    # adjust the value of ace from 11 to 1 if more than one ace, update number of aces that are still valued at 11
    def adjust_for_ace(self):
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

# define chips class consisting of a total pot and a bet
class Chips:
    
    def __init__(self,total,bet=0):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = bet
    
    # update total pot for win
    def win_bet(self):
        self.total += self.bet
    
    # update total pot for lose
    def lose_bet(self):
        self.total -= self.bet

# ask for a bet, check that input is an integer and that bet < total
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('Enter your bet: '))
        except:
            print('Please enter an integer')
        else:
            if chips.bet > chips.total:
                print('You do not have enough chips!')
            else:
                print(f'You have bet {chips.bet}\n')
                break

# add a new card to a specific hand
def hit(deck,hand):
    newcard = deck.deal()
    hand.add_card(newcard)

# ask player to hit or stand, continue to be dealt cards util they select stand
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        move = input('\nDo you want to hit or stand? ' )
        if move[0].lower() == 'h':
            hit(deck,hand)
            print('\nYou have chosen to hit!')
        elif move[0].lower() == 's':
            playing = False
            print('\nYou have chosen to stand!')
        else:
            print('Please enter hit or stand')
            continue
        break

# OBSOLETE: show dealer card face down, show all player's cards
def show_some(player,dealer):
    print("\nDealer's hand:")
    ncards = len(dealer.cards)
    if len == 1:
        print('--Face down--')
    else:
        print('   --Face down--')
        for i in range(1,ncards):
            print('  ',dealer.cards[i])    
    print("\nPlayer's hand:")
    for card in player.cards:
        print('  ',card)

# OBSOLETE: show all cards for dealer and player
def show_all(player,dealer):
    print("\nDealer's hand:")
    for card in dealer.cards:
        print('  ',card)
    print(f"Dealer's hand = {dealer.value}")
    print("\nPlayer's hand:")
    for card in player.cards:
        print('  ',card)
    print(f"Player's hand = {player.value}")

# OBSOLETE
def show_player(player):
    for card in player.cards:
        print('  ',card)

# show some of the dealer hand list - update needed for logic with user defined number of players
def show_some_dealer(dealer):
    print("\nDealer's hand:")
    ncards = len(dealer.cards)
    if len == 1:
        print('--Face down--')
    else:
        print('   --Face down--')
        for i in range(1,ncards):
            print('  ',dealer.cards[i])

# show all cards in dealer hand list - update needed for logic with user defined number of players
def show_all_dealer(dealer):
    print("\nDealer's hand:")
    for card in dealer.cards:
        print('  ',card)
    print(f"Dealer's hand = {dealer.value}")

# show all cards in player hand list - update needed for logic with user defined number of players
def show_all_player(player):
    print("Player's hand:")
    for card in player.cards:
        print('  ',card)
    print(f"Player's hand = {player.value}")
    
# outcome scenarios
def player_busts(player,dealer,chips):
    chips.lose_bet()
    print('Player busts!')

def player_wins(player,dealer,chips):
    chips.win_bet()
    print('Player wins!')

def dealer_busts(player,dealer,chips):
    chips.win_bet()
    print('Dealer busts!')
    
def dealer_wins(player,dealer,chips):
    chips.lose_bet()
    print('Dealer wins!')
    
def push(player,dealer):
    print('Its a tie!')
    hand.adjust_for_ace()

# define new list of starting chips for each player - uses previous values if not the first hand
startchips = []

# Print an opening statement
print('Welcome to Blackjack!')
print('Get as close to 21 without busting.')
print('Dealer hits until they reach 17.')
print('Aces 11 or 1.')
print("Good luck! Let's play blackjack!\n")

# ask for number of players
numplay = int(input('How many players? '))
print('\n')

# set starting chips to 100 for the first hands
for i in range(numplay):
    startchips.append(100)

while True:
    
    # if both players bust at the end of the hand break from the loop, else play
    if numplay == 0:
        break
    else:
        # Create & shuffle the deck
        game_deck = Deck()
        game_deck.shuffle()

        # create list of player hands
        playerhandlist = []
        for i in range(numplay):
            playerhandlist.append(Hand())

        #create dealer hand
        dealer_hand = Hand()
        
        # deal one card to each player and then the dealer (do this twice)
        for playerhand in playerhandlist:
            playerhand.add_card(game_deck.deal())
        dealer_hand.add_card(game_deck.deal())
        for playerhand in playerhandlist:
            playerhand.add_card(game_deck.deal())
        dealer_hand.add_card(game_deck.deal())

        # Create a list of player chips
        playerchipslist = []
        for i in range(numplay):
            playerchipslist.append(Chips(startchips[i]))

        # loop through the players and print their pots
        j = 1
        for playerchips in playerchipslist:
            print(f'Player {j} pot: {playerchips.total} chips\n')
            j += 1

        # Prompt each player for their bet
        k = 1
        for playerchips in playerchipslist:
            print(f'Player {k}\n')
            take_bet(playerchips)
            k += 1

        # show some of the dealer cards
        show_some_dealer(dealer_hand)
        
        # loop through players and print their initial hands
        t = 1
        for playerhand in playerhandlist:
            print(f"\nPlayer {t}'s hand:")
            show_player(playerhand)
            t += 1

        # for each player...
        m = 1
        for playerhand in playerhandlist:

            print(f'\nPlayer {m}:')

            playing = True

            while playing:

                # Prompt for Player to Hit or Stand
                hit_or_stand(game_deck,playerhand)

                # Show cards (but keep one dealer card hidden)
                show_some_dealer(dealer_hand)
                print(f"\nPlayer {m} hand:")
                show_player(playerhand)

                # If player's hand exceeds 21, inform player and break out of loop
                # cannot run player_busts() as it needs to be run later
                if playerhand.value > 21:
                    print('Player busts!')
                    #player_busts(playerhand,dealer_hand,playerchipslist[m-1])
                    break                
            m += 1


        # Setup counter for player busts, loop through players and add 1 if a player has busted
        notbust = 0
        for playerhand in playerhandlist:
            if playerhand.value <= 21:
                notbust += 1
        
        # if at least 1 Player has not busted, play Dealer's hand until Dealer reaches 17
        if notbust > 0:
            while dealer_hand.value < 17:
                dealer_hand.add_card(game_deck.deal())
                
        print('\n****  Final hands  ****')

        # Show all cards
        show_all_dealer(dealer_hand)

        s = 1
        for playerhand in playerhandlist:
            print(f'\nPlayer {s}')
            show_all_player(playerhand)
            s += 1
            
        print('\n****  Results  ****')

        # Run different winning scenarios for each player

        p = 1
        for playerhand in playerhandlist:
            print(f'\nPlayer {p}:')
            if playerhand.value > 21:
                player_busts(playerhand,dealer_hand,playerchipslist[p-1])
            elif playerhand.value > dealer_hand.value:
                player_wins(playerhand,dealer_hand,playerchipslist[p-1])
            elif dealer_hand.value > 21:
                dealer_busts(playerhand,dealer_hand,playerchipslist[p-1])
            elif playerhand.value < dealer_hand.value:
                dealer_wins(playerhand,dealer_hand,playerchipslist[p-1])
            else:
                push(playerhand,dealer_hand)
            p += 1

        # Inform each player of their chips total
        q = 1
        for playerchips in playerchipslist:
            print(f'\nPlayer {q} pot: {playerchips.total}')
            q += 1

        # Ask to play again

        r = 1
        for playerchips in playerchipslist:
            if playerchips.total > 0:
                answer = input(f'Player {r}, do you want to play another hand? (Yes/No)')
                if answer[0].lower()=='y':
                    startchips[r-1] = playerchips.total
                    r += 1
                    continue
                else:
                    print(f'See ya Player {r}!')
                    numplay -= 1
                    r += 1
                    continue
            else:
                print(f'Player {r} out of chips, see ya!')
                numplay -= 1
                r += 1
            break
