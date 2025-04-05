import pygame
import os
from const import SIDE_PANEL_WIDTH, HEIGHT

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

        # Eye positions
        self.eye_left_center = (155, 112)
        self.eye_right_center = (242, 112)
        self.eye_radius = 20
        self.pupil_radius = 8

        # Button state
        self.hit_pressed = False
        self.stand_pressed = False

        # Load images
        try:
            image_path = os.path.join("assets", "images", "blackjack", "dealer.png")
            self.dealer_img = pygame.image.load(image_path)
            self.dealer_img = pygame.transform.scale(self.dealer_img, (420, 640))
        except Exception as e:
            print("Failed to load dealer image:", e)
            self.dealer_img = None

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

    def update_hands(self, player_cards, dealer_cards):
        self.player_hand = player_cards
        self.dealer_hand = dealer_cards

    def set_bet_amount(self, amount):
        self.bet_amount = amount

    def draw(self, screen):
        if self.dealer_img:
            screen.blit(self.dealer_img, (-10, 0))

        # Draw eyes that follow the cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for center in [self.eye_left_center, self.eye_right_center]:
            # pygame.draw.circle(screen, (255, 255, 255), center, self.eye_radius)
            dx = mouse_x - center[0]
            dy = mouse_y - center[1]
            dist = max((dx**2 + dy**2) ** 0.5, 1)
            max_offset = self.eye_radius - self.pupil_radius - 2
            offset_x = int((dx / dist) * max_offset)
            offset_y = int((dy / dist) * max_offset)
            pupil_pos = (center[0] + offset_x, center[1] + offset_y)
            pygame.draw.circle(screen, (0, 0, 0), pupil_pos, self.pupil_radius)

        for i, card in enumerate(self.dealer_hand):
            rect = pygame.Rect(100 + i * 35, 120, 60, 90)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            text = self.font.render(str(card.getRank()[0]), True, (0, 0, 0))
            screen.blit(text, (rect.x + 5, rect.y + 5))

        for i, card in enumerate(self.player_hand):
            rect = pygame.Rect(100 + i * 35, 250, 60, 90)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            text = self.font.render(str(card.getRank()[0]), True, (0, 0, 0))
            screen.blit(text, (rect.x + 5, rect.y + 5))

        if self.bet_img:
            screen.blit(self.bet_img, self.bet_box.topleft)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.bet_box, 2)

        bet_surface = self.font.render(self.bet_amount, True, (0, 0, 0))
        screen.blit(bet_surface, (self.bet_box.x + 100, self.bet_box.y + 5))

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
