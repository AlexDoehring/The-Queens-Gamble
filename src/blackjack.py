from deck import Deck
from card import Card

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

    def start_round(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.deck.reshuffle()

        self.player_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())

    def play_round(self):
        self.start_round()
        print(f"Dealer shows: {self.dealer_hand.cards[0]}")
        print(f"Player has: {self.player_hand} (Total: {self.player_hand.get_value()})")

        # Player turn
        while self.player_hand.get_value() < 21:
            move = input("Hit or Stand? (h/s): ").strip().lower()
            if move == 'h':
                self.player_hand.add_card(self.deck.draw())
                print(f"Player hits: {self.player_hand} (Total: {self.player_hand.get_value()})")
                if self.player_hand.get_value() > 21:
                    print("Player busts!")
                    return 'dealer'
            else:
                break

        # Dealer turn
        print(f"Dealer reveals: {self.dealer_hand} (Total: {self.dealer_hand.get_value()})")
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.draw())
            print(f"Dealer hits: {self.dealer_hand} (Total: {self.dealer_hand.get_value()})")

        player_total = self.player_hand.get_value()
        dealer_total = self.dealer_hand.get_value()

        if dealer_total > 21:
            print("Dealer busts!")
            return 'player'
        elif player_total > dealer_total:
            print("Player wins!")
            return 'player'
        elif player_total < dealer_total:
            print("Dealer wins!")
            return 'dealer'
        else:
            print("Push!")
            return 'push'

# for testing:
if __name__ == "__main__":
    game = BlackjackGame()
    result = game.play_round()
    print(f"Result: {result}")
