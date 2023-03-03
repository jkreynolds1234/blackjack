"""Runs Blackjack program"""
import random
import time
from deck_blackjack import deck, ascii_cards

def deal_card(indeck, hand, hidden):
    """Selects random card from a deck, removes it from the deck,
    and returns the card's value."""
    card = random.choice(indeck)
    card.hidden = hidden
    hand.append(card)
    indeck.remove(card)
    return card.card_value

def blackjack():
    """Classic blackjack game. Dealer will always hit if score if 15 or below."""

    player_cards = []
    dealer_cards = []
    player_score = 0
    dealer_score = 0

    def print_cards(persons_cards, persons_score, person, display_score = True):
        """Prints a person's hand and score"""
        print("\n".join(ascii_cards(persons_cards)))
        if display_score is True:
            print(f"{person} total: {persons_score}")

    def deal_dealer_hidden(dealer_cards, dealer_score):
        """Deals the dealer's hand where the
        first card is displayed as hidden."""
        hidden = True
        if len(dealer_cards) > 0:
            hidden = False
        dealer_score += deal_card(deck, dealer_cards, hidden)
        return dealer_cards, dealer_score

    def flip_dealer_print_both():
        """Flips over the dealer's first card
        and prints the player's hand and the dealer's hand."""
        print_cards(player_cards, player_score, "Player")
        # Flip over dealer's first card
        dealer_cards[0].hidden = False
        print_cards(dealer_cards, dealer_score, "Dealer")

    def second_deal(persons_cards, persons_score, person, hit):
        """Deals the person's second hand and handles Ace values dynamically."""
        # Search to see if hand includes an Ace, return all indices of Aces
        indices_ace = [i for i, card in enumerate(persons_cards) if card.value == "A"]

        # Search to see if hand includes card with a value of 11
        indices_eleven = [i for i, card in enumerate(persons_cards) if card.card_value == 11]

        # Get list of indices in indices_ace where the Aces have values of 11:
        value_eleven = [i for i, el in enumerate(indices_ace) if el in indices_eleven]

        # If player score > 21 and there are Aces in the player's hand with values of 11:
        if persons_score > 21 and len(value_eleven) > 0:
            persons_cards[indices_ace[value_eleven[0]]].card_value = 1
            persons_score -= 10
            print_cards(persons_cards, persons_score, person)
            if person == "Player":
                hit = input("Do you want to hit? Type 'y' for yes or 'n' for no: ")
            else:
                time.sleep(1)
        elif persons_score > 21 and len(value_eleven) == 0:
            if person == "Player":
                flip_dealer_print_both()
                print("You busted.\nYOU LOSE :(")
                hit = "n"
            else:
                flip_dealer_print_both()
                print("The dealer busted.\nYOU WIN!")
        elif player_score == 21:
            if person == "Player":
                flip_dealer_print_both()
                print("YOU WIN!")
                hit = "n"
            else:
                flip_dealer_print_both()
                print("The dealer won.\nYOU LOSE :(")
                # So it doesn't hit the condition at the end of the code where dealer_score <= 21
                return None, None, None
        else:
            print_cards(persons_cards, persons_score, person)
            if person == "Player":
                hit = input("Do you want to hit? Type 'y' for yes or 'n' for no: ")
            else:
                time.sleep(1)
        return persons_cards, persons_score, hit

    # First deal
    while len(player_cards) < 2:
        # Dealer hand and score
        dealer_cards, dealer_score = deal_dealer_hidden(dealer_cards, dealer_score)
        # Player hand and score
        player_score += deal_card(deck, player_cards, False)

    print_cards(player_cards, player_score, "Player")
    print_cards(dealer_cards, dealer_score, "Dealer", False)

    # Second deal
    if player_score == 21:
        flip_dealer_print_both()
        print("YOU WIN!")
        return
    else:
        # Player's hits
        hit = input("Do you want to hit? Type 'y' for yes or 'n' for no: ")
        while hit == "y":
            player_score += deal_card(deck, player_cards, False)
            player_cards, player_score, hit = second_deal(player_cards, player_score, "Player", hit)
        # Dealer's hits
        if player_score < 21:
            while dealer_score <= 15:
                dealer_cards, dealer_score = deal_dealer_hidden(dealer_cards, dealer_score)
                dealer_cards, dealer_score, hit = second_deal(dealer_cards, dealer_score, "Dealer", hit)
            if player_score > dealer_score:
                flip_dealer_print_both()
                print("YOU WIN!")
            elif player_score < dealer_score <= 21:
                flip_dealer_print_both()
                print("YOU LOSE :(")
            elif player_score == dealer_score:
                flip_dealer_print_both()
                print("TIE GAME.")

blackjack()
