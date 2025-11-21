# Module to implement the core functionality of a two-player fighting game.
# Classes to conveniently handle storing variables for state of game and players' 
# control inputs. 
# Functions to update game state based on controls and to render the game.
# Game rendering is independent of the simulation, ideal for netcode experiments.

import pygame
import copy
from math import sin, cos, radians

# Game Name
GAME_NAME = "Fighting Squares"

# Game Window Size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

PLAYER_SIZE = 50

PLAYER_SPEED = 10

# Player Attack Constants
ATTACK_FRAMES = 60
ATTACK_RANGE = 50
ATTACK_DAMAGE = 5

# Visual Constants
SWORD_THICKNESS = 5
BACKGROUND_COLOR = pygame.Color("white")
P1_COLOR = pygame.Color("blue")
P2_COLOR = pygame.Color("green")
SWORD_COLOR = pygame.Color("black")

# Captures the state of game at any given frame
# Maintains record of both players' locations, health points and current frame in attack (0 for none ongoing)

class GameState:
    def __init__(self, p1_x=100, p1_hp=100, p1_atk_frame=0, p2_x=700, p2_hp=100, p2_atk_frame=0, game_state_list=None):
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
    
    

# Class captures state of one player's controls on a given frame
class ControlState:
    def __init__(self, mv_l=False, mv_r=False, atk=False, control_state_list=None):
        if control_state_list == None:
            self.mv_l = mv_l
            self.mv_r = mv_r
            self.atk = atk

        else:
            self.load_from_list(control_state_list)

    # Readable string summary of stored control state
    def __str__(self):
        summary = ("mv_l: " + str(self.mv_l) + "\n"
                 + "mv_r: " + str(self.mv_r) + "\n"
                 + "atk: " + str(self.atk))
        
        return summary
    
    # Store each control input state in a list
    def make_list(self) -> list:
        return [self.mv_l, self.mv_r, self.atk]

    # Load a controller state from a list in the format output by make_list
    def load_from_list(self, control_state_list):
        self.mv_l = control_state_list[0]
        self.mv_r = control_state_list[1]
        self.atk = control_state_list[2]
        self.control_state_list = None


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
    default_font = pygame.font.Font("freesansbold.ttf", 20) # Load default font shipped with pygame

    # Player 1 stats in formatted string
    p1_stats = f"Player 1 HP: {game_state.p1_hp}\r\nPlayer 1 X: {game_state.p1_x}\r\nP1 Attack Frame: {game_state.p1_atk_frame}"

    # Player 2 stats in formatted string
    p2_stats = f"Player 2 HP: {game_state.p2_hp}\r\nPlayer 2 X: {game_state.p2_x}\r\nP2 Attack Frame: {game_state.p2_atk_frame}"

    p1_text = default_font.render(p1_stats, True, (0, 0, 0))
    p2_text = default_font.render(p2_stats, True, (0, 0, 0))

    p1_textRect = p1_text.get_rect()
    p1_textRect.center = (100, 50)

    p2_textRect = p2_text.get_rect()
    p2_textRect.center = (WINDOW_WIDTH - 100, 50)

    window.blit(p1_text, p1_textRect)
    window.blit(p2_text, p2_textRect)

    pygame.display.update()

# Takes a game state and input state and returns a NEW game state which is next frame based on those inputs
def update_state(current_game_state: GameState, p1_control_state: ControlState, p2_control_state: ControlState) -> GameState:
    new_game_state = copy.deepcopy(current_game_state) # Copy current game state but with independent values

    # Move Player 1
    if p1_control_state.mv_l and not p1_control_state.mv_r: # Will not move if both move controls pressed!
        new_game_state.p1_x -= PLAYER_SPEED
        # Check left wall collision
        if new_game_state.p1_x < PLAYER_SIZE // 2:
            new_game_state.p1_x = PLAYER_SIZE // 2

    elif p1_control_state.mv_r and not p1_control_state.mv_l:
        new_game_state.p1_x += PLAYER_SPEED
        # Check right wall collision
        if new_game_state.p1_x > WINDOW_WIDTH - (PLAYER_SIZE // 2):
            new_game_state.p1_x = WINDOW_WIDTH - (PLAYER_SIZE // 2)

    # Process Player 1's attack
    if current_game_state.p1_atk_frame == 0: # p1 has not started an attack
        if p1_control_state.atk: # Start an attack if the control is pressed
            new_game_state.p1_atk_frame += 1

    elif current_game_state.p1_atk_frame < ATTACK_FRAMES: # p1's attack is in progress
        new_game_state.p1_atk_frame += 1

    elif current_game_state.p1_atk_frame == ATTACK_FRAMES: # p1 has just completed an attack
        # Process potential damage to p2
        # Player is damaged if standing within attack range + half of player size, but ahead of p1's center
        player_distance = new_game_state.p2_x - new_game_state.p1_x
        if player_distance <= ATTACK_RANGE + (PLAYER_SIZE // 2) and player_distance >= 0:
            new_game_state.p2_hp -= ATTACK_DAMAGE
        new_game_state.p1_atk_frame = 0 # reset p1's attack

    # Move Player 2
    if p2_control_state.mv_l and not p2_control_state.mv_r: # Will not move if both move controls pressed!
        new_game_state.p2_x -= PLAYER_SPEED
        # Check left wall collision
        if new_game_state.p2_x < PLAYER_SIZE // 2:
            new_game_state.p2_x = PLAYER_SIZE // 2

    elif p2_control_state.mv_r and not p2_control_state.mv_l:
        new_game_state.p2_x += PLAYER_SPEED
        # Check right wall collision
        if new_game_state.p2_x > WINDOW_WIDTH - (PLAYER_SIZE // 2):
            new_game_state.p2_x = WINDOW_WIDTH - (PLAYER_SIZE // 2)

    # Process Player 2's attack
    if current_game_state.p2_atk_frame == 0: # p2 has not started an attack
        if p2_control_state.atk: # Start an attack if the control is pressed
            new_game_state.p2_atk_frame += 1

    elif current_game_state.p2_atk_frame < ATTACK_FRAMES: # p2's attack is in progress
        new_game_state.p2_atk_frame += 1

    elif current_game_state.p2_atk_frame == ATTACK_FRAMES: # p2 has just completed an attack
        # Process potential damage to p1
        # Player is damaged if standing within attack range + half of player size, but ahead of p2's center
        player_distance = new_game_state.p2_x - new_game_state.p1_x
        if player_distance <= ATTACK_RANGE + (PLAYER_SIZE // 2) and player_distance >= 0:
            new_game_state.p1_hp -= ATTACK_DAMAGE
        
        new_game_state.p2_atk_frame = 0 # reset p2's attack

    return new_game_state