import emoji
import random
import time
from random import shuffle

spade = (emoji.emojize(':spades:', language = 'alias'))
club = (emoji.emojize(':clubs:', language = 'alias'))
heart = (emoji.emojize(':hearts:', language = 'alias'))
diamond = (emoji.emojize(':diamonds:', language = 'alias'))

suits = {spade: 1, club: 2, heart: 3, diamond: 4}
ranks = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14} 


player_turn = True #############################################################################



def newgame():
    # Deck
    global deck
    deck = []

    for suit in suits:
        for rank in ranks:
            deck.append(rank + suit)
    
    shuffle(deck)

    #Player's hand
    global playerhand
    playerhand = []
    
    for num in range(1, 9):
        playerhand.append(deck[0])
        deck.pop(0)

    playerspade = []
    playerclub = []
    playerheart = []
    playerdiamond = []

    for card in playerhand:
        if card[-1] == spade:
            playerspade.append(card)
        
        elif card[-1] == club:
            playerclub.append(card)

        elif card[-1] == heart:
            playerheart.append(card)

        else:
            playerdiamond.append(card)


    playerhand = playerspade + playerheart + playerclub + playerdiamond

    #Bot's hand
    global bothand
    bothand = []
    
    for num in range(1, 9):
        bothand.append(deck[0])
        deck.pop(0)

    botspade = []
    botclub = []
    botheart = []
    botdiamond = []

    for card in bothand:
        if card[-1] == spade:
            botspade.append(card)
        
        elif card[-1] == club:
            botclub.append(card)

        elif card[-1] == heart:
            botheart.append(card)

        else:
            botdiamond.append(card)

    bothand = botspade + botheart + botclub + botdiamond

    #Trump
    global trumpsuit

    trumpcard = deck[0]
    trumpsuit = trumpcard[-2]
    deck.pop(0)

    


playedcards = []
attackingcards = []
defendingcards = []

def display():
    print(f"\nCards left: {len(deck)}")
    print(f"Trump suit: {trumpsuit}")
    print(f"Bot's hand: {len(bothand)}")
    print(f"Player's hand: {(playerhand)}\n")
    print(f'Attacking cards: {attackingcards}')
    print(f'Defending cards: {defendingcards}')


def playerattack():
    global playedcards
    global attackingcards
    global defendingcards

    global player_turn


    while True:
        display()

        attackingcard_index = input("Type in an index of a card in order to play that card: ")
        if attackingcard_index.isdigit() == True:

            if int(attackingcard_index) in range(len(playerhand)):

                attackingcard = playerhand[int(attackingcard_index)]
                playerhand.pop(int(attackingcard_index))
                playedcards.append(attackingcard)
                attackingcards.append(attackingcard)
                break
    


    while True:
        defendingcard = "none"

        for botcard in bothand:
            if botcard[-2] == attackingcard[-2]:

                if ranks[botcard[0:-2]] > ranks[attackingcard[0:-2]]:
                    defendingcard = botcard
                    bothand.remove(botcard)
                    playedcards.append(defendingcard)
                    defendingcards.append(defendingcard)

                    display()

                    break
                
                else:
                    continue
        


        if defendingcard == "none":

            for botcardtrump in bothand:

                if botcardtrump[-2] == trumpsuit:

                    if attackingcard[-2] == trumpsuit:
                        
                        if ranks[botcardtrump[0:-2]] > ranks[attackingcard[0:-2]]:

                            defendingcard = botcardtrump
                            bothand.remove(botcardtrump)
                            playedcards.append(defendingcard)
                            defendingcards.append(defendingcard)

                            display()
                            break

                        else:
                            defendingcard = "none"

                    else:
                        defendingcard = botcardtrump
                        bothand.remove(botcardtrump)
                        playedcards.append(defendingcard)
                        defendingcards.append(defendingcard)

                        display()
                        break

        else:
            pass




        if defendingcard == "none":
            print("\nBot does not have cards to defend itself")
            player_turn = True

            for playedcard in playedcards:
                bothand.append(playedcard)

            for i in range(len(playerhand), 8):
                if len(deck) == 0:
                    break

                else:
                    playerhand.append(deck[0])
                    deck.pop(0)

            playedcards = []
            attackingcards = []
            defendingcards = []

            display()

            break


        else:
            # Checking whether the user wants to attack
            samerank = []

            for cards in playedcards:

                for playercard in playerhand:

                    if ranks[playercard[:-2]] == ranks[cards[:-2]]:
                        samerank.append(playercard)

            if samerank == []:
                print("\nYour turn has ended\n")
                player_turn = False

                for i in range(len(playerhand), 8):

                    if len(deck) == 0:
                        break
                    else:
                        playerhand.append(deck[0])
                        deck.pop(0)

                for i in range(len(bothand), 8):
                    if len(deck) == 0:
                        break

                    else:
                        bothand.append(deck[0])
                        deck.pop(0)

                attackingcards = []
                defendingcards = []
                playedcards = []

                display()

                break

            else:
                while True:
                    print(f"\n{samerank}")
                    samerank_index = input("You have at least one card of the same rank. Enter the index of your desired card: ")

                    if samerank_index.isdigit() == True:
                        samerank_index = int(samerank_index)

                        if samerank_index in range(len(samerank)):
                            break

                initiate_atk = input("Would you like to attack with that card? ")

                if initiate_atk in ['Y', 'y', 'yes', 'Yes', "YES", "si", 'si por favor']:
                    attackingcard = samerank[samerank_index]
                    playerhand.remove(attackingcard)
                    attackingcards.append(attackingcard)
                    playedcards.append(attackingcard)
                    samerank = []
                    continue

                elif initiate_atk in ["N", "n", "no", "No", "NO", "non", "nyet"]:
                    print("\nYour turn has ended")
                    player_turn = False

                    for i in range(len(playerhand), 8):
                        if len(deck) == 0:
                            break

                        else:
                            playerhand.append(deck[0])
                            deck.pop(0)

                    for i in range(len(bothand), 8):
                        if len(deck) == 0:
                            break
                        
                        else:
                            bothand.append(deck[0])
                            deck.pop(0)

                    attackingcards = []
                    defendingcards = []
                    playedcards = []

                    display()

                    break
                





def botattack():
    global attackingcards
    global defendingcards
    global playedcards

    global trumpsuit

    global playerhand
    global bothand

    global player_turn

    possible_defendingcards = []

    bot_attackingcard = bothand[random.randint(0, len(bothand) - 1)]

    bothand.remove(bot_attackingcard)
    attackingcards.append(bot_attackingcard)
    playedcards.append(bot_attackingcard)

    while True:


        for card in playerhand:

            if bot_attackingcard[-2] == trumpsuit:

                if card[-2] == trumpsuit:

                    if ranks[card[0:-2]] > ranks[bot_attackingcard[0:-2]]:

                        possible_defendingcards.append(card)

            else:

                if card[-2] == trumpsuit:
                    possible_defendingcards.append(card)

                else:
                    if card[-2] == bot_attackingcard[-2]:

                        if ranks[card[:-2]] > ranks[bot_attackingcard[0:-2]]:
                            possible_defendingcards.append(card)

        display()
        print(f"\nPossible defending cards: {possible_defendingcards}")

        if possible_defendingcards == []:
            print("\nYou have no cards to defend yourself")
            player_turn = False

            for card in playedcards:
                playerhand.append(card)

            attackingcards = []
            defendingcards = []
            playedcards = []
                            
            for i in range(len(bothand), 8):
                if len(deck) == 0:
                    break

                else:
                    bothand.append(deck[0])
                    deck.pop(0)

            display()
            break

        else:

            while True:
                defendingcard_index = input("\nEnter the index of your desired card: ")

                if defendingcard_index.isdigit() == True:

                    defendingcard_index = int(defendingcard_index)

                    if defendingcard_index in range(len(possible_defendingcards)):

                        defendingcard = possible_defendingcards[defendingcard_index]

                        playerhand.remove(defendingcard)
                        defendingcards.append(defendingcard)
                        playedcards.append(defendingcard)

                        possible_defendingcards = []

                        break

            bot_samerank = []

            for card in playedcards:

                for botcard in bothand:

                    if ranks[botcard[:-2]] == ranks[card[:-2]]:

                        bot_samerank.append(botcard)


            if bot_samerank == []:
                print("\nBot's turn has ended")
                player_turn = True

                for i in range(len(bothand), 8):
                    if len(deck) == 0:
                        break

                    else:
                        bothand.append(deck[0])
                        deck.pop(0)

                for i in range(len(playerhand), 8):
                    if len(deck) == 0:
                        break

                    else:
                        playerhand.append(deck[0])
                        deck.pop(0)

                attackingcards = []
                defendingcards = []
                playedcards = []

                display()
                break

            else:

                bot_attackingcard = bot_samerank[random.randint(0, len(bot_samerank) - 1)]

                attackingcards.append(bot_attackingcard)
                playedcards.append(bot_attackingcard)

                bothand.remove(bot_attackingcard)

                continue



    
newgame()

while True:
    try:
        playerhand[0]
        bothand[0]
    except:
        break

    time.sleep(5)

    if player_turn == True:
        playerattack()


    else:
        botattack()

if len(playerhand) == 0:
    print("\nPlayer won! Bot is a durak")

elif len(bothand) == 0:
    print("\nBot won! You are a durak")