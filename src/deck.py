from card import Card
import random

# Deck class
# This class represents a standard deck of playing cards.
# It provides methods to shuffle the deck, draw cards, and reshuffle when the deck is empty.
# It also allows for drawing specific cards if they are available in the deck.
# The deck is initialized with 52 cards, and the drawn cards are tracked separately.
# The reshuffle method returns the drawn cards back to the deck and shuffles it.
# The draw method allows for drawing a specific card or the top card from the deck.
class Deck:
    def __init__(self):
        ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        self.drawn_cards = []

    def reshuffle(self):
        while len(self.drawn_cards) > 1:
            temp = self.drawn_cards.pop()
            self.cards.append(temp)
        random.shuffle(self.cards)

    def draw(self, card=None):
        if len(self.cards) < 1:
            self.reshuffle()
            
        # If a specific card is requested, check if it's in the deck
        # and move it to drawn cards if it is.    
        if card is not None:
            if card in self.cards:
                self.cards.remove(card)
                self.drawn_cards.append(card)
                return card
            else:
                raise ValueError("Card not found in the deck.")
        # If no specific card is requested, draw the top card
        value = self.cards.pop()
        return value

    def __str__(self):
        return f"Deck of {len(self.cards)} cards"

    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"
