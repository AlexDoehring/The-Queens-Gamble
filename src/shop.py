import pygame
import os
from upgrade import Upgrade
from powerup import PowerUp
from const import *
import sys
import math


class Shop:
    def __init__(self):
        self.upgrades = [
            Upgrade("Luck", "decreases opponents chance of capturing a piece", 5),
            Upgrade("Bounty", "increases reward of each piece's capture", 10)
        ]
        
        self.powerups = [
            PowerUp("T8kBack", "allows you to take back a move", 5),
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
        
                
class ShopUI:
    def __init__(self, money):
        self.shop = Shop()
        self.upgrade_buttons = []
        self.powerup_buttons = []
        self.money = money
        self.buttons_pressed = [False for _ in range(len(self.shop.available_upgrades()) + len(self.shop.available_powerups()))]
        self.info_button = None
        self.popup_visible = False

        try:
            image_path = os.path.join("assets", "images", "shop", "button.png")
            self.button_img = pygame.image.load(image_path)
            self.button_img = pygame.transform.scale(self.button_img, (SIDE_PANEL_WIDTH - 220, 38))
            image_path = os.path.join("assets", "images", "shop", "info_popup.png")
            self.info_img = pygame.image.load(image_path).convert_alpha()
            self.info_img = pygame.transform.scale(self.info_img, (425, 516))
            image_path = os.path.join("assets", "images", "shop", "buttonPressed.png")
            self.button_pressed_img = pygame.image.load(image_path)
            self.button_pressed_img = pygame.transform.scale(self.button_pressed_img, (SIDE_PANEL_WIDTH - 220, 38))
            self.luckPressed = False
            self.bountyPressed = False
        except Exception as e:
            print("Failed to load shop buttons:", e)
            self.dealer_img = None
        
    def draw(self, surface):
        right_panel_x = SIDE_PANEL_WIDTH + BOARD_WIDTH
        right_panel = pygame.Rect(right_panel_x, 0, SIDE_PANEL_WIDTH, HEIGHT)
        pygame.draw.rect(surface, (13, 46, 75), right_panel)
        font = pygame.font.SysFont('monospace', 24, bold=True)
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
            if self.button_pressed_img and self.buttons_pressed[self.shop.available_upgrades().index(upgrade)]:
                surface.blit(self.button_pressed_img, (right_panel_x + 10, 195 + self.shop.available_upgrades().index(upgrade) * 50))  
            elif self.button_img:
                surface.blit(self.button_img, (right_panel_x + 10, 195 + self.shop.available_upgrades().index(upgrade) * 50))              
            upgrade_text = font.render(f"{upgrade.name}: ${upgrade.cost}", True, (9, 48, 78))
            level_text = font.render(f"Lvl: {upgrade.level}", True, (247, 163, 19))
            surface.blit(level_text, (right_panel_x + 240, 200 + self.shop.available_upgrades().index(upgrade) * 50))
            surface.blit(upgrade_text, (right_panel_x + 25, 200 + self.shop.available_upgrades().index(upgrade) * 50))
            left_button_rect = pygame.Rect(right_panel_x + 15, 195 + self.shop.available_upgrades().index(upgrade) * 50, SIDE_PANEL_WIDTH - 230, 35)
            self.upgrade_buttons.append(left_button_rect)
            
            # right_button_rect = pygame.Rect(right_panel_x + 190, 195 + self.shop.available_upgrades().index(upgrade) * 40, SIDE_PANEL_WIDTH - 230, 35)
            # pygame.draw.rect(surface, (255, 255, 255), left_button_rect, width=2, border_radius=5)
            # pygame.draw.rect(surface, (255, 255, 255), right_button_rect, width=2, border_radius=5)
        btn_offset = len(self.shop.available_upgrades())
        powerup_title = subtitle_font.render("Power-Ups", True, (255, 255, 255))
        surface.blit(powerup_title, (right_panel_x + 20, 340))
        pygame.draw.line(surface, (255, 255, 255), (right_panel_x + 20, 380), (right_panel_x + SIDE_PANEL_WIDTH - 20, 380), 2)
        for pup in self.shop.available_powerups():
            # print(f'index: {self.shop.available_powerups().index(pup)}')
            # print(f'pup: {pup}')
            if self.button_pressed_img and self.buttons_pressed[btn_offset + self.shop.available_powerups().index(pup)]:
                surface.blit(self.button_pressed_img, (right_panel_x + 10, 395 + self.shop.available_powerups().index(pup) * 50))  
            elif self.button_img:
                surface.blit(self.button_img, (right_panel_x + 10, 395 + self.shop.available_powerups().index(pup) * 50))
            powerup_text = font.render(f"{pup.name}: ${pup.cost}", True, (9, 48, 78))
            amount_text = font.render(f"Qty: {pup.amount_left}", True, (247, 163, 19))
            surface.blit(amount_text, (right_panel_x + 240, 400 + self.shop.available_powerups().index(pup) * 50))
            surface.blit(powerup_text, (right_panel_x + 25, 400 + self.shop.available_powerups().index(pup) * 50))
            left_button_rect = pygame.Rect(right_panel_x + 15, 395 + self.shop.available_powerups().index(pup) * 50, SIDE_PANEL_WIDTH - 230, 35)
            self.powerup_buttons.append(left_button_rect)

        #get font for "i"
        font = pygame.font.SysFont("Courier New", 25, bold=True)

        self.circle_radius = 15
        self.info_center = (1400,40)
        # Render "i"
        text = font.render("i", True, 'WHITE')
        text_rect = text.get_rect(center=self.info_center)
        
        self.info_button = pygame.draw.circle(surface, 'BLACK', self.info_center, self.circle_radius)
        # Blit the "i"
        surface.blit(text, text_rect)
        #surface.blit(self.info_img, (200, 100))

        if self.popup_visible:
            #pygame.draw.rect(surface, (255, 255, 255), (200, 100, 200, 150))  # white background for contrast
            surface.blit(self.info_img, (1030,70))

            
    def get_money(self):
        return self.money
    
    def set_money(self, money):
        self.money = money
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.info_button.collidepoint(event.pos):
                self.popup_visible = not self.popup_visible
            for i in range(len(self.shop.available_upgrades())):
                button = self.upgrade_buttons[i]
                upgrade = self.shop.available_upgrades()[i]
                if button.collidepoint(event.pos):
                    self.buttons_pressed[i] = True
                    if upgrade.level == 5:
                        print(f"{upgrade.name} is already at max level.")
                    elif self.money >= upgrade.cost:
                        self.money -= upgrade.cost
                        upgrade.level += 1
                        print(f"Purchased {upgrade.name}. New level: {upgrade.level}. Remaining money: {self.money}")
                    else:
                        print(f"Not enough money to purchase {upgrade.name}.")
            for i in range(len(self.shop.available_powerups())):
                button = self.powerup_buttons[i]
                powerup = self.shop.available_powerups()[i]
                if button.collidepoint(event.pos):
                    self.buttons_pressed[i + len(self.shop.available_upgrades())] = True
                    if powerup.amount_left == 0:
                        print(f"{powerup.name} is out of stock.")
                    elif self.money >= powerup.cost:
                        self.money -= powerup.cost
                        powerup.amount_left -= 1
                        print(f"Purchased {powerup.name}. Remaining quantity: {powerup.amount_left}. Remaining money: {self.money}")
                    else:
                        print(f"Not enough money to purchase {powerup.name}.")
        
        if event.type == pygame.MOUSEBUTTONUP:
            for i in range(len(self.buttons_pressed)):
                self.buttons_pressed[i] = False


    """def call_popup(self):
        surface.blit(self.info_img, (200, 100))"""
