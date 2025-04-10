import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square
from ai import ChessAI
from piece import King
from shop import ShopUI
from upgrade import Upgrade
from powerup import PowerUp
from blackjack_ui import BlackjackUI
from blackjack import BlackjackGame
from card import Card
from speech_bubble import SpeechBubble

# Game class
# This class is responsible for managing the game state, including the chessboard, pieces, and game logic.
# It handles user input, updates the game state, and renders the game to the screen.
# It also manages the side panels for the Blackjack mini-game and the shop UI.
# The game logic is separated from the UI logic, allowing for better organization and maintainability.
# The game class also handles the speech bubble for player interactions and messages.
# It initializes the game with a new board, pieces, and other necessary components.
class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        self.money = 15
        self.shop = ShopUI(self.money)
        self.ai = ChessAI(self.board)
        self.game_over = False
        self.blackjack_ui = BlackjackUI()
        self.speech_bubble = SpeechBubble()

        # Start screen Bubble
        self.speech_bubble.say("Blackjack Burt is online.")

        # Preload textures once
        self.texture_cache = {}

    def load_texture(self, path):
        if path not in self.texture_cache:
            self.texture_cache[path] = pygame.image.load(path)
        return self.texture_cache[path]

    # blit methods

    def show_bg(self, surface):
        theme = self.config.theme
        x_offset = SIDE_PANEL_WIDTH

        # Draw the background squares
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQSIZE + x_offset, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (400, 5 + row * SQSIZE)
                    surface.blit(lbl, lbl_pos)

                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + x_offset + SQSIZE - 20, HEIGHT - 20)
                    surface.blit(lbl, lbl_pos)

    # Draw the pieces on the board
    # This method iterates through the board squares and blits the pieces to the screen.
    def show_pieces(self, surface):
        x_offset = SIDE_PANEL_WIDTH
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = self.load_texture(piece.texture)
                        img_center = col * SQSIZE + x_offset + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    # Draw the moves available for the piece being dragged
    # This method highlights the squares where the piece can move.
    def show_moves(self, surface):
        theme = self.config.theme
        x_offset = SIDE_PANEL_WIDTH

        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQSIZE + x_offset, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    # Draw the last move made on the board
    # This method highlights the squares where the last move was made.
    def show_last_move(self, surface):
        theme = self.config.theme
        x_offset = SIDE_PANEL_WIDTH

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE + x_offset, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    # Draw the hover effect on the square being hovered over
    # This method highlights the square where the mouse is currently hovering.
    # It provides visual feedback to the user about where they are pointing.
    def show_hover(self, surface):
        x_offset = SIDE_PANEL_WIDTH

        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.col * SQSIZE + x_offset, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    # Draw the side panels for the Blackjack mini-game and the shop UI
    # This method draws the left panel for the Blackjack game and the right panel for the shop UI.
    # It also draws the dealer image and the speech bubble for player interactions.
    def show_side_panels(self, surface):
        left_panel = pygame.Rect(0, 0, SIDE_PANEL_WIDTH, HEIGHT)
        pygame.draw.rect(surface, (30, 30, 30), left_panel)

        # Draw dealer image (Blackjack Burt)
        if self.blackjack_ui and self.blackjack_ui.dealer_img:
            surface.blit(self.blackjack_ui.dealer_img, (-10, 0))

        # Draw the Blackjack UI panel
        if self.blackjack_ui:
            self.blackjack_ui.draw(surface)

        # Draw speech bubble OVER the robot
        self.speech_bubble.draw(surface)

        # Title
        title_font = pygame.font.SysFont('monospace', 18, bold=True)
        blackjack_text = title_font.render("Blackjack Burt", True, (211, 65, 21))
        surface.blit(blackjack_text, (123, 23))

        self.shop.draw(surface)

    # Various methods to handle game logic and player interactions
    
    def update_speech_bubble(self, dt):
        self.speech_bubble.update(dt)

    def say_to_player(self, message, duration=None):
        self.speech_bubble.say(message)
    
    def add_money(self, amount):
        self.money += amount
        self.update_shop_money()
        
    def sub_money(self, amount):
        self.money -= amount
        self.update_shop_money()

    def update_shop_money(self):
        self.shop.set_money(self.money)
            
    def update_game_money(self):
        self.money = self.shop.get_money()
    
    def get_luck(self):
        luck_upgrade = self.shop.shop.available_upgrades()[0]
        return luck_upgrade.effect()
    
    def get_bounty(self):
        bounty_upgrade = self.shop.shop.available_upgrades()[1]
        return bounty_upgrade.effect()

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()

    def check_king_capture(self):
        king_count = 0
        for row in self.board.squares:
            for square in row:
                if isinstance(square.piece, King):
                    king_count += 1
        if king_count < 2:
            print("Game Over! A king has been captured.")
            self.game_over = True

