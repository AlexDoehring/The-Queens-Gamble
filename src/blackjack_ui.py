import pygame
import os
from const import SIDE_PANEL_WIDTH, HEIGHT

class BlackjackUI:
    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 22, bold=True)
        self.bet_amount = ""
        self.active_input = False
        self.reveal_dealer_second = False

        self.hit_button = pygame.Rect(210, HEIGHT - 85, 75, 75)
        self.stand_button = pygame.Rect(290, HEIGHT - 85, 100, 75)
        self.input_box = pygame.Rect(120, HEIGHT - 85, 50, 75)
        self.bet_box = pygame.Rect(10, HEIGHT - 85, 190, 75)
        self.confirm_bet_box = pygame.Rect(10, HEIGHT - 85, 80, 75)
        self.plus_box = pygame.Rect(self.bet_box.x + 155, self.bet_box.y + 20, 20, 20)
        self.minus_box = pygame.Rect(self.bet_box.x + 155, self.bet_box.y + 37, 20, 20)
        
        self.betnumbertext = None
        self.bet_number = 0

        self.player_hand = []
        self.dealer_hand = []

        self.dealer_y = 300
        self.player_y = 440
        self.card_spacing = 30

        # Eye positions
        self.eye_left_center = (155, 112)
        self.eye_right_center = (242, 112)
        self.eye_radius = 20
        self.pupil_radius = 10

        # Button state
        self.hit_pressed = False
        self.stand_pressed = False

        # Animation state
        self.animating_card = False
        self.card_queue = []

        # Dialogue and result tracking
        self.dealer_message = "Let's play a fair hand!"
        self.exit_button = pygame.Rect(1100, 550, 150, 60)
        self.player_score = 0
        self.dealer_score = 0
        self.win_history = []

        # Load images
        try:
            image_path = os.path.join("assets", "images", "blackjack", "dealer.png")
            self.dealer_img = pygame.image.load(image_path)
            self.dealer_img = pygame.transform.scale(self.dealer_img, (420, 640))
        except Exception as e:
            print("Failed to load dealer image:", e)
            self.dealer_img = None

        try:
            deck_path = os.path.join("assets", "images", "blackjack", "deck.png")
            self.deck_img = pygame.image.load(deck_path)
            self.deck_img = pygame.transform.scale(self.deck_img, (130, 140))
        except Exception as e:
            print("Failed to load deck image:", e)
            self.deck_img = None

        try:
            self.hit_img_rest = pygame.image.load(os.path.join("assets", "images", "blackjack", "hit_rest.png")).convert_alpha()
            self.hit_img_push = pygame.image.load(os.path.join("assets", "images", "blackjack", "hit_push.png")).convert_alpha()
            self.hit_img_rest = pygame.transform.scale(self.hit_img_rest, (self.hit_button.width, self.hit_button.height))
            self.hit_img_push = pygame.transform.scale(self.hit_img_push, (self.hit_button.width, self.hit_button.height))
        except Exception as e:
            print("Failed to load hit button images:", e)
            self.hit_img_rest = self.hit_img_push = None

        try:
            self.stand_img_rest = pygame.image.load(os.path.join("assets", "images", "blackjack", "stand_rest.png")).convert_alpha()
            self.stand_img_push = pygame.image.load(os.path.join("assets", "images", "blackjack", "stand_push.png")).convert_alpha()
            self.stand_img_rest = pygame.transform.scale(self.stand_img_rest, (self.stand_button.width, self.stand_button.height))
            self.stand_img_push = pygame.transform.scale(self.stand_img_push, (self.stand_button.width, self.stand_button.height))
        except Exception as e:
            print("Failed to load stand button images:", e)
            self.stand_img_rest = self.stand_img_push = None

        try:
            bet_img_path = os.path.join("assets", "images", "blackjack", "bet_box.png")
            self.bet_img = pygame.image.load(bet_img_path).convert_alpha()
            self.bet_img = pygame.transform.scale(self.bet_img, (self.bet_box.width, self.bet_box.height))
        except Exception as e:
            print("Failed to load bet box image:", e)
            self.bet_img = None
        
        try:
            back_path = os.path.join("assets", "images", "blackjack", "backface.png")
            self.card_back_img = pygame.image.load(back_path).convert_alpha()
            self.card_back_img = pygame.transform.scale(self.card_back_img, (100, 140))
        except Exception as e:
            print("Failed to load card back image:", e)
            self.card_back_img = None

        try:
            bg_path = os.path.join("assets", "images", "blackjack", "background.png")
            self.background_img = pygame.image.load(bg_path).convert()
            self.background_img = pygame.transform.scale(self.background_img, (1440, HEIGHT))
        except Exception as e:
            print("Failed to load blackjack background:", e)
            self.background_img = None

    def update_hands(self, player_cards, dealer_cards):
        self.player_hand = player_cards
        self.dealer_hand = dealer_cards

    def set_bet_amount(self, amount):
        self.bet_amount = amount

    def queue_card(self, card, to_dealer=False):
        self.card_queue.append((card, to_dealer))
        self.animating_card = True

    def render_card(self, screen, card, x, y):
        rect = pygame.Rect(x, y, 70, 105)
        pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=6)

        rank = str(card.getValue()) if card.getRank() not in ["Ace", "Jack", "Queen", "King"] else card.getRank()
        suit = card.getSuit()
        suit_symbols = {
            "Hearts": "♥",
            "Diamonds": "♦",
            "Clubs": "♣",
            "Spades": "♠"
        }
        symbol = suit_symbols.get(suit, "?")
        label = f"{rank[0]}{symbol}" if rank != "10" else f"10{symbol}"

        color = (200, 0, 0) if suit in ["Hearts", "Diamonds"] else (0, 0, 0)
        text = self.font.render(label, True, color)
        screen.blit(text, (rect.x + 8, rect.y + 10))

    def draw(self, screen):
        if self.background_img:
            screen.blit(self.background_img, (0, 0))
        else:
            screen.fill((0, 100, 0))

        if self.dealer_img:
            screen.blit(self.dealer_img, (-10, 0))

        if self.deck_img:
            screen.blit(self.deck_img, (265, self.dealer_y + 95))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for center in [self.eye_left_center, self.eye_right_center]:
            dx = mouse_x - center[0]
            dy = mouse_y - center[1]
            dist = max((dx**2 + dy**2) ** 0.5, 1)
            max_offset = self.eye_radius - self.pupil_radius - 2
            offset_x = int((dx / dist) * max_offset)
            offset_y = int((dy / dist) * max_offset)
            pupil_pos = (center[0] + offset_x, center[1] + offset_y)
            pygame.draw.circle(screen, (0, 0, 0), pupil_pos, self.pupil_radius)

        for i, card in enumerate(self.dealer_hand):
            x = 80 + i * self.card_spacing
            if i == 1 and not self.reveal_dealer_second:
                if self.card_back_img:
                    screen.blit(self.card_back_img, (x, self.dealer_y - 10))
                else:
                    pygame.draw.rect(screen, (120, 120, 120), pygame.Rect(x, self.dealer_y, 70, 105))
            else:
                self.render_card(screen, card, x, self.dealer_y)

        for i, card in enumerate(self.player_hand):
            self.render_card(screen, card, 80 + i * self.card_spacing, self.player_y)

        if self.bet_img:
            screen.blit(self.bet_img, self.bet_box.topleft)
            screen.blit(self.bet_img, self.confirm_bet_box.topleft)
            # pygame.draw.rect(screen, (255, 255, 255), self.confirm_bet_box, 2)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.bet_box, 2)

        bet_surface = self.font.render(self.bet_amount, True, (0, 0, 0))
        screen.blit(bet_surface, (self.bet_box.x + 100, self.bet_box.y + 5))
        
        plusminusfont = pygame.font.SysFont('monospace', 30, bold=True)
        plustext = plusminusfont.render("+", True, (255, 255, 255))
        minustext = plusminusfont.render("-", True, (255, 255, 255))
        screen.blit(plustext, (self.bet_box.x + 155, self.bet_box.y + 15))
        screen.blit(minustext, (self.bet_box.x + 155, self.bet_box.y + 32))
        # pygame.draw.rect(screen, (255, 255, 255), self.plus_box, 1)
        # pygame.draw.rect(screen, (255, 255, 255), self.minus_box, 1)
        
        betnumberfont = pygame.font.SysFont('monospace', 50, bold=True)
        self.betnumbertext = betnumberfont.render(str(self.bet_number), True, (255, 255, 255))
        screen.blit(self.betnumbertext, (self.bet_box.x + 120, self.bet_box.y + 12))
    

        if self.hit_img_rest and self.hit_img_push:
            image = self.hit_img_push if self.hit_pressed else self.hit_img_rest
            screen.blit(image, self.hit_button.topleft)
        else:
            pygame.draw.rect(screen, (50, 200, 50), self.hit_button)
            screen.blit(self.font.render("HIT", True, (0, 0, 0)), (self.hit_button.x + 15, self.hit_button.y + 5))

        if self.stand_img_rest and self.stand_img_push:
            image = self.stand_img_push if self.stand_pressed else self.stand_img_rest
            screen.blit(image, self.stand_button.topleft)
        else:
            pygame.draw.rect(screen, (200, 50, 50), self.stand_button)
            screen.blit(self.font.render("STAND", True, (0, 0, 0)), (self.stand_button.x + 5, self.stand_button.y + 5))

        if self.animating_card and self.card_queue:
            card, to_dealer = self.card_queue.pop(0)
            if to_dealer:
                self.dealer_hand.append(card)
            else:
                self.player_hand.append(card)
            pygame.time.wait(300)
            if not self.card_queue:
                self.animating_card = False

        # Draw green panel UI
        pygame.draw.rect(screen, (20, 100, 20), (1025, 0, 400, HEIGHT))

        dialogue_font = pygame.font.SysFont("monospace", 24)
        dialogue_lines = self.dealer_message.split('\n')
        for i, line in enumerate(dialogue_lines):
            line_surf = dialogue_font.render(line, True, (255, 255, 255))
            screen.blit(line_surf, (1050, 40 + i * 30))

        pygame.draw.rect(screen, (255, 255, 255), self.exit_button, border_radius=8)
        exit_font = pygame.font.SysFont("monospace", 22, bold=True)
        exit_text = exit_font.render("EXIT", True, (0, 0, 0))
        screen.blit(exit_text, (
            self.exit_button.centerx - exit_text.get_width() // 2,
            self.exit_button.centery - exit_text.get_height() // 2
        ))
        
        
    # def update_bet_number(self, screen, amount):
    #     print("Updating bet number to:", amount)
    #     betnumberfont = pygame.font.SysFont('monospace', 70, bold=True)
    #     self.betnumbertext = betnumberfont.render(str(amount), True, (255, 255, 255))
    #     screen.blit(self.betnumbertext, (self.bet_box.x + 120, self.bet_box.y + 12))    
