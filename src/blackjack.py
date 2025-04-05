import pygame
from deck import Deck
from card import Card
from const import SIDE_PANEL_WIDTH, HEIGHT
import os

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

class BlackjackUI:
    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 22, bold=True)
        self.bet_amount = ""
        self.active_input = False
        self.hit_button = pygame.Rect(50, HEIGHT - 60, 80, 35)
        self.stand_button = pygame.Rect(150, HEIGHT - 60, 100, 35)
        self.input_box = pygame.Rect(10, HEIGHT - 60, 35, 35)

        self.player_hand = []
        self.dealer_hand = []

        try:
            image_path = os.path.join("assets", "images", "blackjack", "dealer.png")
            print("Attempting to load dealer image from:", os.path.abspath(image_path))
            self.dealer_img = pygame.image.load(image_path)
            self.dealer_img = pygame.transform.scale(self.dealer_img, (400, 400))
            print("Dealer image loaded successfully.")
        except Exception as e:
            print("Failed to load dealer image:", e)
            self.dealer_img = None

    def draw(self, screen):
        # Panel background should be drawn in game.py before calling this method

        if self.dealer_img:
            # Draw the dealer image on the left side of the panel
            screen.blit(self.dealer_img, (10, 10))

        for i, card in enumerate(self.dealer_hand):
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100 + i * 35, 120, 30, 45))

        for i, card in enumerate(self.player_hand):
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(100 + i * 35, 250, 30, 45))

        pygame.draw.rect(screen, (255, 255, 255), self.input_box, 2)
        txt_surface = self.font.render(self.bet_amount, True, (255, 255, 255))
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

        pygame.draw.rect(screen, (50, 200, 50), self.hit_button)
        screen.blit(self.font.render("HIT", True, (0, 0, 0)), (self.hit_button.x + 15, self.hit_button.y + 5))

        pygame.draw.rect(screen, (200, 50, 50), self.stand_button)
        screen.blit(self.font.render("STAND", True, (0, 0, 0)), (self.stand_button.x + 5, self.stand_button.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active_input = True
            else:
                self.active_input = False

            if self.hit_button.collidepoint(event.pos):
                print("Hit pressed")

            if self.stand_button.collidepoint(event.pos):
                print("Stand pressed")

        if event.type == pygame.KEYDOWN and self.active_input:
            if event.key == pygame.K_BACKSPACE:
                self.bet_amount = self.bet_amount[:-1]
            elif event.unicode.isdigit() or (event.unicode == "." and "." not in self.bet_amount):
                self.bet_amount += event.unicode
