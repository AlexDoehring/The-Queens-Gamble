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

def run_blackjack_ui(screen, player_piece, dealer_piece, blackjack_ui):
    bj_game = BlackjackGame()
    ui = blackjack_ui
    ui.reveal_dealer_second = False

    bj_game.start_round(player_piece, dealer_piece)

    # Clear hands before adding animated cards
    ui.player_hand.clear()
    ui.dealer_hand.clear()

    # Add initial cards with animation and game state
    ui.queue_card(bj_game.player_hand.cards[0], to_dealer=False)
    ui.queue_card(bj_game.player_hand.cards[1], to_dealer=False)
    ui.queue_card(bj_game.dealer_hand.cards[0], to_dealer=True)
    ui.queue_card(bj_game.dealer_hand.cards[1], to_dealer=True)

    phase = 'player'
    winner = None

    while True:
        screen.fill((0, 100, 0))
        ui.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ui.hit_button.collidepoint(event.pos) and phase == 'player':
                    new_card = bj_game.deck.draw()
                    bj_game.player_hand.add_card(new_card)
                    ui.queue_card(new_card, to_dealer=False)

                    if bj_game.player_hand.get_value() > 21:
                        winner = 'dealer'
                        phase = 'done'

                elif ui.stand_button.collidepoint(event.pos) and phase == 'player':
                    ui.reveal_dealer_second = True

                    while bj_game.dealer_hand.get_value() < 17:
                        card = bj_game.deck.draw()
                        bj_game.dealer_hand.add_card(card)
                        ui.queue_card(card, to_dealer=True)

                    player_total = bj_game.player_hand.get_value()
                    dealer_total = bj_game.dealer_hand.get_value()

                    if dealer_total > 21 or player_total > dealer_total:
                        winner = 'player'
                    elif dealer_total > player_total:
                        winner = 'dealer'
                    else:
                        winner = 'push'
                    phase = 'done'

        if phase == 'done' and not ui.animating_card:
            pygame.time.wait(1000)
            return winner


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.clock = pygame.time.Clock()  # Limit FPS
    

    

    def show_game_over_screen(self, winner):
        font = pygame.font.SysFont('monospace', 48, bold=True)
        small_font = pygame.font.SysFont('monospace', 36)
        screen = self.screen
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((15, 90, 120, 180))  # black with 70% opacity


        while True:

            screen.blit(overlay, (0, 0))
            message = f"{winner.capitalize()} Wins!"
            msg_text = font.render(message, True, (255, 255, 255))
            play_again_text = small_font.render("Play Again", True, (0, 0, 0))
            exit_text = small_font.render("Exit", True, (0, 0, 0))

            play_again_rect = pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2, 250, 50)
            exit_rect = pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 + 70, 250, 50)

            pygame.draw.rect(screen, (255, 255, 255), play_again_rect)
            pygame.draw.rect(screen, (255, 255, 255), exit_rect)

            screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(play_again_text, (
                play_again_rect.centerx - play_again_text.get_width() // 2,
                play_again_rect.centery - play_again_text.get_height() // 2
            ))
            screen.blit(exit_text, (
                exit_rect.centerx - exit_text.get_width() // 2,
                exit_rect.centery - exit_text.get_height() // 2
            ))


            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_rect.collidepoint(event.pos):
                        self.game.reset()
                        return  # resume mainloop
                    elif exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()


    def mainloop(self):
        # start_time = time.time()

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        # total_time = 0    USED FOR FPS CALCULATION
        # frame_count = 0   USED FOR FPS CALCULATION
        while True:
            screen.fill((0, 0, 0))
            game.show_side_panels(screen)
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                # Let blackjack panel handle its own input
                game.shop.handle_event(event)  # Handle shop UI events
                game.update_game_money()  # Update money in the shop
                

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_x, clicked_y = event.pos
                    if SIDE_PANEL_WIDTH <= clicked_x < SIDE_PANEL_WIDTH + BOARD_WIDTH and 0 <= clicked_y < HEIGHT:
                        clicked_row = clicked_y // SQSIZE
                        clicked_col = (clicked_x - SIDE_PANEL_WIDTH) // SQSIZE

                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)

                elif event.type == pygame.MOUSEMOTION:
                    motion_x, motion_y = event.pos
                    if SIDE_PANEL_WIDTH <= motion_x < SIDE_PANEL_WIDTH + BOARD_WIDTH and 0 <= motion_y < HEIGHT:
                        motion_row = motion_y // SQSIZE
                        motion_col = (motion_x - SIDE_PANEL_WIDTH) // SQSIZE
                        game.set_hover(motion_row, motion_col)
                    else:
                        game.hovered_sqr = None

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_x, released_y = event.pos
                        if SIDE_PANEL_WIDTH <= released_x < SIDE_PANEL_WIDTH + BOARD_WIDTH and 0 <= released_y < HEIGHT:
                            released_row = released_y // SQSIZE
                            released_col = (released_x - SIDE_PANEL_WIDTH) // SQSIZE

                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            if board.valid_move(dragger.piece, move):
                                target_square = board.squares[released_row][released_col]
                                captured = target_square.has_piece()
                                captured_piece = target_square.piece if captured else None

                                # Trigger Blackjack if the captured piece is black (AI-controlled)
                                if captured_piece and captured_piece.color == 'black':
                                    print(f"You are about to capture a {captured_piece.name}. Let's play Blackjack first!")
                                    
                                    result = run_blackjack_ui(self.screen, dragger.piece.name, captured_piece.name, self.game.blackjack_ui)
                                    # result = bj.play_round()

                                    print(f"Blackjack result: {result}")
                                    
                                    if result != 'player':
                                        print("You lost the Blackjack game. Capture is denied.") if result == 'dealer' else print("It's a push. Capture is denied.")
                                        dragger.undrag_piece()       # Return piece to original square
                                        game.next_turn()             # Switch to black's turn
                                    else:
                                        board.move(dragger.piece, move)
                                        board.set_true_en_passant(dragger.piece)
                                        game.play_sound(captured)
                                        game.next_turn()
                                        game.check_king_capture()
                                        print(f"Bounty for piece captured: {captured_piece.bounty}")
                                        game.add_money(captured_piece.bounty)
                                        dragger.undrag_piece()


                                else:
                                    board.move(dragger.piece, move)
                                    board.set_true_en_passant(dragger.piece)
                                    game.play_sound(captured)
                                    game.next_turn()
                                    game.check_king_capture()
                                
                                if game.game_over:
                                    dragger.undrag_piece()
                                    winner = 'white' if game.next_player == 'black' else 'black'
                                    self.show_game_over_screen(winner)
                                    game = self.game
                                    board = game.board
                                    dragger = game.dragger

                            dragger.undrag_piece()
                            
                            # force full re-draw manually
                            screen.fill((0, 0, 0))
                            game.show_side_panels(screen)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)
                            pygame.display.update()

                            pygame.time.wait(1000)

                            if game.next_player == 'black':
                                move_result = game.ai.get_move(board)
                                if move_result is None:
                                    print("AI has no valid moves")
                                else:
                                    piece, move = move_result
                                
                                if piece and move:
                                    #dragger.undrag_piece()
                                    
                                    captured = board.squares[move.final.row][move.final.col].has_piece()
                                    if not captured:
                                        board.move(piece, move)
                                        board.set_true_en_passant(piece)
                                        game.play_sound(captured)
                                        game.next_turn()
                                        game.check_king_capture()
                                        if game.game_over:
                                            dragger.undrag_piece()
                                            winner = 'white' if game.next_player == 'black' else 'black'
                                            self.show_game_over_screen(winner)
                                            game = self.game
                                            board = game.board
                                            dragger = game.dragger     
                                    else:
                                        prob = random.random()
                                        luck = game.get_luck()
                                        newProb = piece.prob - luck
                                        print(f"I WANT TO CAPTURE")
                                        win_capture = True if prob <= newProb else False
                                        # print(f'Luck: {luck}, Probability: {piece.prob}, Random: {prob}, Result: {win_capture}')
                                        # print(f"Adjusted Probability: {newProb}")
                                        if win_capture:
                                            board.move(piece, move)
                                            board.set_true_en_passant(piece)
                                            game.play_sound(captured)
                                            game.next_turn()
                                            game.check_king_capture()
                                            if game.game_over:
                                                dragger.undrag_piece()
                                                winner = 'white' if game.next_player == 'black' else 'black'
                                                self.show_game_over_screen(winner)
                                                game = self.game
                                                board = game.board
                                                dragger = game.dragger
                                        else:
                                            game.next_turn()
                                                                      

                    
                    dragger.undrag_piece()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()

                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            # FPS calculation
            # frame_time = time.time() - start_time
            # total_time += frame_time
            # frame_count += 1

            # Print every 60 frames (~once per second)
            # if frame_count % 60 == 0:
            #    print(f"Average frame time: {total_time / frame_count:.4f} seconds ({1000 * total_time / frame_count:.2f} ms)")

            self.clock.tick(60)  # Cap FPS at 120


main = Main()
main.mainloop()