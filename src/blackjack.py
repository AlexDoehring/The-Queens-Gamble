from deck import Deck

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

    def start_round(self, player_card=None, dealer_card=None):
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.deck.reshuffle()

        # Optional: use mapped cards (e.g., from a chess piece capture)
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
                break
            else:
                print("Invalid input. Please type 'h' or 's'.")

        print(f"\nDealer reveals: {self.dealer_hand} (Total: {self.dealer_hand.get_value()})")
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.draw())
            print(f"Dealer hits: {self.dealer_hand} (Total: {self.dealer_hand.get_value()})")

        player_total = self.player_hand.get_value()
        dealer_total = self.dealer_hand.get_value()

        print("\n=== RESULT ===")
        if dealer_total > 21:
            print("Dealer busts! Player wins!")
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
