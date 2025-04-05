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
        self.hit_button = pygame.Rect(210, HEIGHT - 85, 75, 75)
        self.stand_button = pygame.Rect(290, HEIGHT - 85, 100, 75)
        self.input_box = pygame.Rect(120, HEIGHT - 85, 50, 75)
        self.bet_box = pygame.Rect(10, HEIGHT - 85, 190, 75)

        self.player_hand = []
        self.dealer_hand = []

        # Load images
        self.hit_pressed = False
        self.stand_pressed = False

        try:
            image_path = os.path.join("assets", "images", "blackjack", "dealer.png")
            print("Attempting to load dealer image from:", os.path.abspath(image_path))
            self.dealer_img = pygame.image.load(image_path)
            self.dealer_img = pygame.transform.scale(self.dealer_img, (420, 640))
            print("Dealer image loaded successfully.")
        except Exception as e:
            print("Failed to load dealer image:", e)
            self.dealer_img = None

        # This block loads the button images for hit action
        try:
            self.hit_img_rest = pygame.image.load(os.path.join("assets", "images", "blackjack", "hit_rest.png")).convert_alpha()
            self.hit_img_push = pygame.image.load(os.path.join("assets", "images", "blackjack", "hit_push.png")).convert_alpha()
            self.hit_img_rest = pygame.transform.scale(self.hit_img_rest, (self.hit_button.width, self.hit_button.height))
            self.hit_img_push = pygame.transform.scale(self.hit_img_push, (self.hit_button.width, self.hit_button.height))
            print("Hit button images loaded successfully.")
        except Exception as e:
            print("Failed to load hit button images:", e)
            self.hit_img_rest = self.hit_img_push = None

        # This block loads the button images for stand action
        try:
            self.stand_img_rest = pygame.image.load(os.path.join("assets", "images", "blackjack", "stand_rest.png")).convert_alpha()
            self.stand_img_push = pygame.image.load(os.path.join("assets", "images", "blackjack", "stand_push.png")).convert_alpha()
            self.stand_img_rest = pygame.transform.scale(self.stand_img_rest, (self.stand_button.width, self.stand_button.height))
            self.stand_img_push = pygame.transform.scale(self.stand_img_push, (self.stand_button.width, self.stand_button.height))
            print("Stand button images loaded successfully.")
        except Exception as e:
            print("Failed to load stand button images:", e)
            self.stand_img_rest = self.stand_img_push = None

        # This block loads the bet box image
        try:
            bet_img_path = os.path.join("assets", "images", "blackjack", "bet_box.png")
            self.bet_img = pygame.image.load(bet_img_path).convert_alpha()
            self.bet_img = pygame.transform.scale(self.bet_img, (self.bet_box.width, self.bet_box.height))
            print("Bet box image loaded successfully.")
        except Exception as e:
            print("Failed to load bet box image:", e)
            self.bet_img = None

    def draw(self, screen):
        if self.dealer_img:
            screen.blit(self.dealer_img, (-10, 0))

        for i, card in enumerate(self.dealer_hand):
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100 + i * 35, 120, 30, 45))

        for i, card in enumerate(self.player_hand):
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(100 + i * 35, 250, 30, 45))

        if self.bet_img:
            screen.blit(self.bet_img, self.bet_box.topleft)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.bet_box, 2)

        bet_surface = self.font.render(self.bet_amount, True, (0, 0, 0))
        screen.blit(bet_surface, (self.bet_box.x + 100, self.bet_box.y + 5))

        # HIT BUTTON
        # Logic: 
        # If the button is pressed, show the pressed image, otherwise show the rest image
        # If the images are not loaded, draw a rectangle instead
        if self.hit_img_rest and self.hit_img_push:
            image = self.hit_img_push if self.hit_pressed else self.hit_img_rest
            screen.blit(image, self.hit_button.topleft)
        else:
            pygame.draw.rect(screen, (50, 200, 50), self.hit_button)
            screen.blit(self.font.render("HIT", True, (0, 0, 0)), (self.hit_button.x + 15, self.hit_button.y + 5))

        # STAND BUTTON
        # Logic:
        # If the button is pressed, show the pressed image, otherwise show the rest image
        # If the images are not loaded, draw a rectangle instead
        if self.stand_img_rest and self.stand_img_push:
            image = self.stand_img_push if self.stand_pressed else self.stand_img_rest
            screen.blit(image, self.stand_button.topleft)
        else:
            pygame.draw.rect(screen, (200, 50, 50), self.stand_button)
            screen.blit(self.font.render("STAND", True, (0, 0, 0)), (self.stand_button.x + 5, self.stand_button.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.bet_box.collidepoint(event.pos):
                self.active_input = True
            else:
                self.active_input = False

            if self.hit_button.collidepoint(event.pos):
                self.hit_pressed = True
                print("Hit pressed")

            if self.stand_button.collidepoint(event.pos):
                self.stand_pressed = True
                print("Stand pressed")

        if event.type == pygame.MOUSEBUTTONUP:
            self.hit_pressed = False
            self.stand_pressed = False

        if event.type == pygame.KEYDOWN and self.active_input:
            if event.key == pygame.K_BACKSPACE:
                self.bet_amount = self.bet_amount[:-1]
            elif event.unicode.isdigit() or (event.unicode == "." and "." not in self.bet_amount):
                self.bet_amount += event.unicode