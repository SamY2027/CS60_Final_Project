# Game that works very well for saving state and stepping forward, super deterministic, no floats!

import pygame
import copy
from math import sin, cos, radians

# Captures the state of game at any given frame
class GameState:
    def __init__(self, p1_x=0, p1_hp=100, p1_atk_frame=0, p2_x=0, p2_hp=100, p2_atk_frame=0, game_state_list=None):
        if game_state_list == None:
            self.p1_x = p1_x
            self.p1_hp = p1_hp
            self.p1_atk_frame = p1_atk_frame
            self.p2_x = p2_x
            self.p2_hp = p2_hp
            self.p2_atk_frame = p2_atk_frame
        else:
            self.load_from_list(game_state_list)

    # Readable string summary of the current game state
    def __str__(self):
        summary = ("p1_x: " + str(self.p1_x) + "\n"
                 + "p1_hp: " + str(self.p1_hp) + "\n"
                 + "p1_atk_frame: " + str(self.p1_atk_frame) + "\n"
                 + "p2_x: " + str(self.p2_x) + "\n"
                 + "p2_hp: " + str(self.p2_hp) + "\n"
                 + "p2_atk_frame: " + str(self.p2_atk_frame))
        
        return summary
    
    # Store each game state variable in a list
    def make_list(self) -> list:
        return [self.p1_x, self.p1_hp, self.p1_atk_frame, self.p2_x, self.p2_hp, self.p2_atk_frame]
    
    # Load the game state from a list in the format ouput by make_list
    def load_from_list(self, game_state_list):
        self.p1_x = game_state_list[0]
        self.p1_hp = game_state_list[1]
        self.p1_atk_frame = game_state_list[2]
        self.p2_x = game_state_list[3]
        self.p2_hp = game_state_list[4]
        self.p2_atk_frame = game_state_list[5]
    
    

# Class captures state of controller at any given frame
class ControlState:
    def __init__(self, p1_mv_l=False, p1_mv_r=False, p1_atk=False, p2_mv_l=False, p2_mv_r=False, p2_atk=False, control_state_list=None):
        if control_state_list == None:
            self.p1_mv_l = p1_mv_l
            self.p1_mv_r = p1_mv_r
            self.p1_atk = p1_atk
            self.p2_mv_l = p2_mv_l
            self.p2_mv_r = p2_mv_r
            self.p2_atk = p2_atk
        else:
            self.load_from_list(control_state_list)

    # Readable string summary of stored control state
    def __str__(self):
        summary = ("p1_mv_l: " + str(self.p1_mv_l) + "\n"
                 + "p1_mv_r: " + str(self.p1_mv_r) + "\n"
                 + "p1_atk: " + str(self.p1_atk) + "\n"
                 + "p2_mv_l: " + str(self.p2_mv_l) + "\n"
                 + "p2_mv_r: " + str(self.p2_mv_r) + "\n"
                 + "p2_atk: " + str(self.p2_atk))
        
        return summary
    
    # Store each control input state in a list
    def make_list(self) -> list:
        return [self.p1_mv_l, self.p1_mv_r, self.p1_atk, self.p2_mv_l, self.p2_mv_r, self.p2_atk]

    # Load a controller state from a list in the format output by make_list
    def load_from_list(self, control_state_list):
        self.p1_mv_l = control_state_list[0]
        self.p1_mv_r = control_state_list[1]
        self.p1_atk = control_state_list[2]
        self.p2_mv_l = control_state_list[3]
        self.p2_mv_r = control_state_list[4]
        self.p2_atk = control_state_list[5]
        self.control_state_list = None
        

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

PLAYER_SIZE = 50

PLAYER_SPEED = 10

ATTACK_FRAMES = 15
ATTACK_RANGE = 50
SWORD_THICKNESS = 5

BACKGROUND_COLOR = pygame.Color("white")
P1_COLOR = pygame.Color("blue")
P2_COLOR = pygame.Color("green")
SWORD_COLOR = pygame.Color("black")


def render_frame(game_state: GameState, window):
    # Clear Background
    window.fill(pygame.Color("white"))

    # Draw Player 1 (location is center of square)
    pygame.draw.rect(window, P1_COLOR, [game_state.p1_x - (PLAYER_SIZE / 2), WINDOW_HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE], 0)

    # Draw player 1 sword (if an attack is active)
    # Sword starts out pointing 45 degrees backwards out of player and moves to straigt forward over length of attack
    if game_state.p1_atk_frame != 0:
        
        p1_center = [game_state.p1_x, WINDOW_HEIGHT - (PLAYER_SIZE / 2)]

        angle = (135 / ATTACK_FRAMES) * (ATTACK_FRAMES - game_state.p1_atk_frame)

        sword_tip_offset = [cos(radians(angle)) * ATTACK_RANGE, sin(radians(angle)) * ATTACK_RANGE] # Think in regular coordinates, we fix later for screen coords

        pygame.draw.line(window, SWORD_COLOR, p1_center, [p1_center[0] + sword_tip_offset[0], p1_center[1] - sword_tip_offset[1]], SWORD_THICKNESS)

    # Draw Player 2 (location is center of square)
    pygame.draw.rect(window, P2_COLOR, [game_state.p2_x - (PLAYER_SIZE / 2), WINDOW_HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE], 0)

    # Draw player 2 sword (if an attack is active)
    # Sword starts out pointing 45 degrees backwards out of player and moves to straigt forward over length of attack
    if game_state.p2_atk_frame != 0:
        
        p2_center = [game_state.p2_x, WINDOW_HEIGHT - (PLAYER_SIZE / 2)]

        angle = 45 + ((135 / ATTACK_FRAMES) * game_state.p2_atk_frame)

        sword_tip_offset = [cos(radians(angle)) * ATTACK_RANGE, sin(radians(angle)) * ATTACK_RANGE] # Think in regular coordinates, we fix later for screen coords

        pygame.draw.line(window, SWORD_COLOR, p2_center, [p2_center[0] + sword_tip_offset[0], p2_center[1] - sword_tip_offset[1]], SWORD_THICKNESS)

    # Display text of all game state information (usefull for debugging)


    pygame.display.update()

# Takes a game state and input state and returns a NEW game state which is next frame based on those inputs
def update_state(current_game_state: GameState, control_state: ControlState) -> GameState:
    new_game_state = copy.deepcopy(current_game_state) # Copy current game state but with independent values

    # Move Player 1
    if control_state.p1_mv_l and not control_state.p1_mv_r: # Will not move if both move controls pressed!
        new_game_state.p1_x -= PLAYER_SPEED

    elif control_state.p1_mv_r and not control_state.p1_mv_l:
        new_game_state.p1_x += PLAYER_SPEED

    # Process Player 1's attack
    if current_game_state.p1_atk_frame == 0: # p1 has not started an attack
        if control_state.p1_atk: # Start an attack if the control is pressed
            new_game_state.p1_atk_frame += 1

    elif current_game_state.p1_atk_frame < ATTACK_FRAMES: # p1's attack is in progress
        new_game_state.p1_atk_frame += 1

    elif current_game_state.p1_atk_frame == ATTACK_FRAMES: # p1 has just completed an attack
        pass # Process potential damage to p2 then potential victory
        new_game_state.p1_atk_frame = 0 # reset p1's attack

    # Move Player 2
    if control_state.p2_mv_l and not control_state.p2_mv_r: # Will not move if both move controls pressed!
        new_game_state.p2_x -= PLAYER_SPEED

    elif control_state.p2_mv_r and not control_state.p2_mv_l:
        new_game_state.p2_x += PLAYER_SPEED

    # Process Player 2's attack
    if current_game_state.p2_atk_frame == 0: # p2 has not started an attack
        if control_state.p2_atk: # Start an attack if the control is pressed
            new_game_state.p2_atk_frame += 1

    elif current_game_state.p2_atk_frame < ATTACK_FRAMES: # p2's attack is in progress
        new_game_state.p2_atk_frame += 1

    elif current_game_state.p2_atk_frame == ATTACK_FRAMES: # p2 has just completed an attack
        pass # Process potential damage to p1 then potential victory
        new_game_state.p2_atk_frame = 0 # reset p2's attack

    return new_game_state
        

# Testing
if __name__ == "__main__":
    
    pygame.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Fighting Squares")

    clock = pygame.time.Clock()

    default_font = pygame.font.Font("freesansbold.ttf", 20) # This font ships with pygame

    game_state = GameState(p1_x=100, p2_x=700)

    control_state = ControlState() # Game starts with no controls pressed

    # Game Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: # a moves p1 left
                    control_state.p1_mv_l = True
                elif event.key == pygame.K_d: # d moves p1 right
                    control_state.p1_mv_r = True
                elif event.key == pygame.K_s: # s is p1's attack
                    control_state.p1_atk = True
                elif event.key == pygame.K_j: # j moves p2 left
                    control_state.p2_mv_l = True
                elif event.key == pygame.K_l: # l moves p2 right
                    control_state.p2_mv_r = True
                elif event.key == pygame.K_k:
                    control_state.p2_atk = True # k is p2's attack

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a: # a moves p1 left
                    control_state.p1_mv_l = False
                elif event.key == pygame.K_d: # d moves p1 right
                    control_state.p1_mv_r = False
                elif event.key == pygame.K_s: # s is p1's attack
                    control_state.p1_atk = False
                elif event.key == pygame.K_j: # j moves p2 left
                    control_state.p2_mv_l = False
                elif event.key == pygame.K_l: # l moves p2 right
                    control_state.p2_mv_r = False
                elif event.key == pygame.K_k:
                    control_state.p2_atk = False # k is p2's attack

        render_frame(game_state, window)
        game_state = update_state(game_state, control_state)

        clock.tick(60) # Lock the game at 30fps, all timings are based on framerate, so this controls run speed
    
    # Quit Pygame
    pygame.quit()
    
