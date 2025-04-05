import pygame

from upgrade import Upgrade
from powerup import PowerUp
from const import *

class Shop:
    def __init__(self, money=0):
        self.money = money
        self.upgrades = [
            Upgrade("Luck", "decreases opponents chance of capturing a piece", 5),
            Upgrade("Bounty", "increases reward of each piece's capture", 10)
        ]
        
        self.powerups = [
            PowerUp("Takeback", "allows you to take back a move", 5),
            PowerUp("Redo", "allows you to redo a lost Blackjack game", 10),
            PowerUp("Skip", "allows you to skip the opponent's turn", 15)
        ]

        self.available = True
        
    def available_upgrades(self):
        return self.upgrades
    
    def available_powerups(self):
        return self.powerups
    
    def is_available(self):
        return self.available 
    
    def change_availability(self):
        self.available = not self.available
        

class ShopHandler:
    def __init__(self, money=0):
        self.money = money
        
    def handle_event(self, event): #CHANGE
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
                
class ShopUI:
    def __init__(self, money=0):
        self.money = money
        self.shop = Shop(self.money)
        self.shop_handler = ShopHandler(self.money)
        
    def draw(self, surface):
        right_panel_x = SIDE_PANEL_WIDTH + BOARD_WIDTH
        right_panel = pygame.Rect(right_panel_x, 0, SIDE_PANEL_WIDTH, HEIGHT)
        pygame.draw.rect(surface, (60, 60, 60), right_panel)
        font = pygame.font.SysFont('monospace', 24)
        title_font = pygame.font.SysFont('monospace', 36, bold=True)  # Larger font for the title
        subtitle_font = pygame.font.SysFont('monospace', 28, bold=True)
        
        shop_text = title_font.render("Shop", True, (255, 255, 255))
        balance_text = font.render(f"Money: ${self.money}", True, (255, 255, 255))
        upgrades_title = subtitle_font.render("Upgrades", True, (255, 255, 255))
        
        
        surface.blit(shop_text, (right_panel_x + 20, 20))
        pygame.draw.line(surface, (255, 255, 255), (right_panel_x + 20, 70), (right_panel_x + SIDE_PANEL_WIDTH - 20, 70), 2)
        surface.blit(balance_text, (right_panel_x + 20, 80))
        surface.blit(upgrades_title, (right_panel_x + 20, 140))
        pygame.draw.line(surface, (255, 255, 255), (right_panel_x + 20, 180), (right_panel_x + SIDE_PANEL_WIDTH - 20, 180), 2)
        
        for upgrade in self.shop.available_upgrades():
            upgrade_text = font.render(f"{upgrade.name}: ${upgrade.cost}", True, (255, 255, 255))
            level_text = font.render(f"Level: {upgrade.level}", True, (255, 255, 255))
            surface.blit(level_text, (right_panel_x + 200, 200 + self.shop.available_upgrades().index(upgrade) * 40))
            surface.blit(upgrade_text, (right_panel_x + 20, 200 + self.shop.available_upgrades().index(upgrade) * 40))
            left_button_rect = pygame.Rect(right_panel_x + 15, 195 + self.shop.available_upgrades().index(upgrade) * 40, SIDE_PANEL_WIDTH - 230, 35)
            right_button_rect = pygame.Rect(right_panel_x + 190, 195 + self.shop.available_upgrades().index(upgrade) * 40, SIDE_PANEL_WIDTH - 230, 35)
            pygame.draw.rect(surface, (255, 255, 255), left_button_rect, width=2, border_radius=5)
            pygame.draw.rect(surface, (255, 255, 255), right_button_rect, width=2, border_radius=5)