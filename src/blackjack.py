from deck import Deck
from card import Card
from piece import Piece
import random
import time

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        total = sum(card.getValue() for card in self.cards)
        aces = sum(1 for card in self.cards if card.getRank() == 'Ace')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def start_round(self, player_piece=None, dealer_piece=None):
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.deck.reshuffle()

        # Optional: use mapped cards (e.g., from a chess piece capture)
        suit = random.choice(['Hearts', 'Diamonds', 'Clubs', 'Spades'])
        match player_piece:
            case 'pawn':
                player_card = random.choice([Card(suit, "Four"), Card(suit, "Five"), Card(suit, "Six")])
            case 'knight':
                player_card = random.choice([Card(suit, "Two"), Card(suit, "Three"), Card(suit, "Seven")])
            case 'bishop':
                player_card = random.choice([Card(suit, "Two"), Card(suit, "Three"), Card(suit, "Seven")])
            case 'rook':
                player_card = random.choice([Card(suit, "Eight"), Card(suit, "Nine")])
            case 'queen':
                player_card = random.choice([Card(suit, "Ten"), Card(suit, "Jack"), Card(suit, "Queen"), Card(suit, "King")])
            case 'king':
                player_card = Card(suit, "Ace")
            case _:
                raise ValueError("Invalid piece type")
            
        suit = random.choice(['Hearts', 'Diamonds', 'Clubs', 'Spades'])
        match dealer_piece:
            case 'pawn':
                dealer_card = random.choice([Card(suit, "Four"), Card(suit, "Five"), Card(suit, "Six")])
            case 'knight':
                dealer_card = random.choice([Card(suit, "Two"), Card(suit, "Three"), Card(suit, "Seven")])
            case 'bishop':
                dealer_card = random.choice([Card(suit, "Two"), Card(suit, "Three"), Card(suit, "Seven")])
            case 'rook':
                dealer_card = random.choice([Card(suit, "Eight"), Card(suit, "Nine")])
            case 'queen':
                dealer_card = random.choice([Card(suit, "Ten"), Card(suit, "Jack"), Card(suit, "Queen"), Card(suit, "King")])
            case 'king':
                dealer_card = Card(suit, "Ace")
            case _:
                raise ValueError("Invalid piece type")
            
        
        self.player_hand.add_card(player_card or self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(dealer_card or self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())

    def play_round(self, player_card=None, dealer_card=None):
        self.start_round(player_card, dealer_card)
        print("\n=== BLACKJACK ROUND ===")
        print(f"Dealer shows: {self.dealer_hand.cards[0]}")
        print(f"Player has: {self.player_hand} (Total: {self.player_hand.get_value()})")

        while self.player_hand.get_value() < 21:
            move = input("Hit or Stand? (h/s): ").strip().lower()
            if move == 'h':
                self.player_hand.add_card(self.deck.draw())
                print(f"Player hits: {self.player_hand} (Total: {self.player_hand.get_value()})")
                if self.player_hand.get_value() > 21:
                    print("Player busts!")
                    return 'dealer'
            elif move == 's':
                time.sleep(1)   # WAIT
                print("Player stands.")
                break
            else:
                print("Invalid input. Please type 'h' or 's'.")

        print(f"\nDealer reveals: {self.dealer_hand} (Total: {self.dealer_hand.get_value()})")
        time.sleep(1)   # WAIT
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.draw())
            print(f"Dealer hits: {self.dealer_hand} (Total: {self.dealer_hand.get_value()})")
            time.sleep(1)   # WAIT

        player_total = self.player_hand.get_value()
        dealer_total = self.dealer_hand.get_value()

        print("\n=== RESULT ===")
        if dealer_total > 21:
            print("Dealer busts! Player wins!")
            time.sleep(1)   # WAIT
            return 'player'
        elif player_total > dealer_total:
            print("Player wins!")
            time.sleep(1)   # WAIT
            return 'player'
        elif player_total < dealer_total:
            print("Dealer wins!")
            time.sleep(1)   # WAIT
            return 'dealer'
        else:
            print("Push!")
            time.sleep(1)   # WAIT
            return 'push'
