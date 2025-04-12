import pygame
import sys
from blackjack import BlackjackGame
import random
from blackjack_ui import BlackjackUI
from const import *
from game import Game
from square import Square
from move import Move
import time


class RunBlackjack:
    
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.bj_game = BlackjackGame()

# This function handles the Blackjack UI and game logic.
# It initializes the game, manages the betting phase, and handles player actions (hit/stand).
# It also manages the dealer's actions and determines the winner of the round.
# The function takes the screen, game instance, player and dealer pieces, and the Blackjack UI as parameters.
# The function returns the result of the round (player, dealer, or push).
# It uses the BlackjackGame class to manage the game state and the BlackjackUI class to handle the UI elements.
# The function also handles the animation of cards being dealt and the display of the player's and dealer's hands.
# It uses the Pygame library for rendering and event handling.

    def run_blackjack_ui(self, screen, game, player_piece, dealer_piece, blackjack_ui):
        bj_game = self.bj_game
        ui = blackjack_ui
        ui.reveal_dealer_second = False

        bj_game.start_round(player_piece, dealer_piece)

        # Clear hands before adding animated cards
        ui.player_hand.clear()
        ui.dealer_hand.clear()
        
        ui.bet_number = 0
        betted_money = 0
        
        # Bet loop
        phase = 'bet'
        screen.fill((0, 100, 0))
        ui.draw(screen)
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if ui.plus_box.collidepoint(event.pos):
                        ui.bet_number += 1
                        ui.draw(screen)
                        pygame.display.flip()
                    elif ui.minus_box.collidepoint(event.pos):
                        if ui.bet_number > 0:
                            ui.bet_number -= 1
                            ui.draw(screen)
                            pygame.display.flip()
                    elif ui.confirm_bet_box.collidepoint(event.pos):
                        print("Confirm button Pressed")
                        if ui.bet_number <= game.money:
                            betted_money = ui.bet_number
                            game.money -= ui.bet_number
                            game.update_shop_money()
                            
                            phase = 'done'
                        else:
                            print("Not enough money to place bet")
                if phase == 'done' and not ui.animating_card:
                    running = False
                    # pygame.time.wait(1000)
                    break
                
        print("Betting phase done")
        
        # Screen fill used to clear the screen before drawing the cards
        screen.fill((0, 100, 0))
        ui.draw(screen)
        pygame.display.flip()
        running = True

        # Add initial cards with animation and game state
        ui.queue_card(bj_game.player_hand.cards[0], to_dealer=False)
        ui.queue_card(bj_game.player_hand.cards[1], to_dealer=False)
        ui.queue_card(bj_game.dealer_hand.cards[0], to_dealer=True)
        ui.queue_card(bj_game.dealer_hand.cards[1], to_dealer=True)

        phase = 'player'
        winner = None
        
        if len(bj_game.player_hand.get_value()) > 1:
            ui.total_number = str(bj_game.player_hand.get_value()[0]) + "/" + str(bj_game.player_hand.get_value()[1])
        else:
            ui.total_number = str(bj_game.player_hand.get_value()[0])
        ui.draw(screen)
        pygame.display.flip()
        
        # if len(bj_game.dealer_hand.get_value()) > 1:
        #     ui.dealer_number = str(bj_game.dealer_hand.get_value()[0]) + "/" + str(bj_game.dealer_hand.get_value()[1])
        # else:
        #     ui.dealer_number = str(bj_game.dealer_hand.get_value()[0])

        # Game loop for player actions (hit/stand)
        # The player can hit (draw a card) or stand (end their turn).
        while True:
            screen.fill((0, 100, 0))
            ui.draw(screen)
            pygame.display.flip()
            running = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    playerAce = True if len(bj_game.player_hand.get_value()) > 1 else False
                    dealerAce = True if len(bj_game.dealer_hand.get_value()) > 1 else False
                    if ui.hit_button.collidepoint(event.pos) and phase == 'player':
                        new_card = bj_game.deck.draw()
                        bj_game.player_hand.add_card(new_card)
                        ui.queue_card(new_card, to_dealer=False)
                        
                        handVal = bj_game.player_hand.get_value()[0] if len(bj_game.player_hand.get_value()) < 1 else min(bj_game.player_hand.get_value())
                        playerAce = True if len(bj_game.player_hand.get_value()) > 1 else False
                        
                        if playerAce:
                            ui.total_number = str(bj_game.player_hand.get_value()[0]) + "/" + str(bj_game.player_hand.get_value()[1])
                        else:
                            ui.total_number = str(bj_game.player_hand.get_value()[0])
                        ui.draw(screen)
                        pygame.display.flip()
                        
                        if handVal > 21:
                            winner = 'dealer'
                            phase = 'done'

                    elif ui.stand_button.collidepoint(event.pos) and phase == 'player':
                        ui.reveal_dealer_second = True
                        pygame.time.wait(1000)
                        if dealerAce:
                            while max(bj_game.dealer_hand.get_value()) < 17 or (max(bj_game.dealer_hand.get_value()) > 21 and min(bj_game.dealer_hand.get_value()) < 17):
                                pygame.time.wait(1000)
                                card = bj_game.deck.draw()
                                ui.queue_card(card, to_dealer=True)
                                ui.dealer_number = str(bj_game.dealer_hand.get_value()[0]) + "/" + str(bj_game.dealer_hand.get_value()[1])
                                ui.draw(screen)
                                pygame.display.flip()
                                bj_game.dealer_hand.add_card(card)
                                
                            ui.dealer_number = str(bj_game.dealer_hand.get_value()[0]) + "/" + str(bj_game.dealer_hand.get_value()[1])
                            ui.draw(screen)
                            pygame.display.flip()
                            min_hand = min(bj_game.dealer_hand.get_value())
                            max_hand = max(bj_game.dealer_hand.get_value())
                            dealer_total = min_hand if max_hand > 21 else max_hand
                        else:
                            while bj_game.dealer_hand.get_value()[0] < 17:
                                pygame.time.wait(1000)
                                card = bj_game.deck.draw()
                                ui.queue_card(card, to_dealer=True)
                                ui.dealer_number = str(bj_game.dealer_hand.get_value()[0])
                                ui.draw(screen)
                                pygame.display.flip()
                                bj_game.dealer_hand.add_card(card)
                            
                            ui.dealer_number = str(bj_game.dealer_hand.get_value()[0])
                            ui.draw(screen)
                            pygame.display.flip()
                            dealer_total = bj_game.dealer_hand.get_value()[0]

                        # player total logic
                        if playerAce:
                            min_hand = min(bj_game.player_hand.get_value())
                            max_hand = max(bj_game.player_hand.get_value())
                            player_total = min_hand if max_hand > 21 else max_hand
                        else:
                            player_total = bj_game.player_hand.get_value()[0]

                        # Winner Logic
                        if dealer_total > 21 or player_total > dealer_total:
                            winner = 'player'
                            game.money += betted_money * 2
                            game.update_shop_money()
                        elif dealer_total > player_total:
                            winner = 'dealer'
                        else:
                            winner = 'push'
                        pygame.time.wait(2000)
                        ui.bet_number = 0
                        ui.total_number = "0"
                        ui.dealer_number = "0"
                        ui.draw(screen)
                        pygame.display.flip()
                        phase = 'done'

            if phase == 'done' and not ui.animating_card:
                pygame.time.wait(1000)
                return winner

