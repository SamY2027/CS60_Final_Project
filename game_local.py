# Setup for tesing game_logic module functionality separate from the network
# P1 used asd controls, p2 used jkl (left, attack, right)
# Also good demonstration of how to setup, get controller input from, and close down pygame
# as well as how to use game_logic functions and classes

import pygame
import game_logic

# Testing
if __name__ == "__main__":
    
    pygame.init()

    window = pygame.display.set_mode((game_logic.WINDOW_WIDTH, game_logic.WINDOW_HEIGHT))

    pygame.display.set_caption("Fighting Squares")

    clock = pygame.time.Clock()

    game_state = game_logic.GameState(p1_x=100, p2_x=700)

    p1_control_state = game_logic.ControlState() # Game starts with no controls pressed
    p2_control_state = game_logic.ControlState() # Game starts with no controls pressed

    # Game Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: # a moves p1 left
                    p1_control_state.mv_l = True
                elif event.key == pygame.K_d: # d moves p1 right
                    p1_control_state.mv_r = True
                elif event.key == pygame.K_s: # s is p1's attack
                    p1_control_state.atk = True
                elif event.key == pygame.K_j: # j moves p2 left
                    p2_control_state.mv_l = True
                elif event.key == pygame.K_l: # l moves p2 right
                    p2_control_state.mv_r = True
                elif event.key == pygame.K_k:
                    p2_control_state.atk = True # k is p2's attack

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a: # a moves p1 left
                    p1_control_state.mv_l = False
                elif event.key == pygame.K_d: # d moves p1 right
                    p1_control_state.mv_r = False
                elif event.key == pygame.K_s: # s is p1's attack
                    p1_control_state.atk = False
                elif event.key == pygame.K_j: # j moves p2 left
                    p2_control_state.mv_l = False
                elif event.key == pygame.K_l: # l moves p2 right
                    p2_control_state.mv_r = False
                elif event.key == pygame.K_k:
                    p2_control_state.atk = False # k is p2's attack

        game_logic.render_frame(game_state, window)
        game_state = game_logic.update_state(game_state, p1_control_state, p2_control_state)

        clock.tick(30) # Lock the game at 30fps, all timings are based on framerate, so this controls run speed
    
    # Quit Pygame
    pygame.quit()
    
