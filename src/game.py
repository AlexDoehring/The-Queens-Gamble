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

class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        self.money = 100
        self.shop = ShopUI(self.money)
        self.ai = ChessAI(self.board)
        self.game_over = False
        self.blackjack_ui = BlackjackUI()

        # Preload textures once
        self.texture_cache = {}

        # Inject sample cards for testing visuals
        mock_player = [Card("Hearts", "King"), Card("Spades", "Five"), Card("Diamonds", "Queen")]
        mock_dealer = [Card("Diamonds", "Ace"), Card("Clubs", "Seven"), Card("Hearts", "Jack")]

        self.blackjack_ui.update_hands(mock_player, mock_dealer)

    def load_texture(self, path):
        if path not in self.texture_cache:
            self.texture_cache[path] = pygame.image.load(path)
        return self.texture_cache[path]

    # blit methods

    def show_bg(self, surface):
        theme = self.config.theme
        x_offset = SIDE_PANEL_WIDTH

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

    def show_moves(self, surface):
        theme = self.config.theme
        x_offset = SIDE_PANEL_WIDTH

        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQSIZE + x_offset, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

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

    def show_hover(self, surface):
        x_offset = SIDE_PANEL_WIDTH

        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.col * SQSIZE + x_offset, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def show_side_panels(self, surface):
        left_panel = pygame.Rect(0, 0, SIDE_PANEL_WIDTH, HEIGHT)
        pygame.draw.rect(surface, (30, 30, 30), left_panel)

        # Draw the Blackjack UI panel
        self.blackjack_ui.draw(surface)

        # Title
        title_font = pygame.font.SysFont('monospace', 36, bold=True)
        blackjack_text = title_font.render("Blackjack", True, (255, 255, 255))
        surface.blit(blackjack_text, (20, 20))

        self.shop.draw(surface)

        
            
    def update_money(self):
        self.money = self.shop.get_money()
    
    def get_luck(self):
        luck_upgrade = self.shop.shop.available_upgrades()[0]
        return luck_upgrade.effect()

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

