# Aleksander Nowicki and Samuel Young
# Dartmouth CS60 25F Final Project
# 11/21/2025
# Delay Netcode Module
#
# Functions to run game from game_logic with a delay based netcode
# The game will wait to receive inputs from the remote player before advancing the frame

import game_logic
import socket
import time
import random
import pygame
import json

# Constant - indicates whether player 2's connection is bad (simulated)
BAD_CONNECTION = False

# Returns byte message in format FS|frame_number|control_state|\n
def encode_control_message(frame_number, control_state):
    try:
        message = "FS" + "|" + str(frame_number) + "|" + json.dumps(control_state.make_list()) + "|\n"
        return message.encode()
    except Exception as e:
        print(f"The following error occured trying to encode the message: {e}")
        raise Exception("Message Encoding Error")

# Decode the first message in the buffer, returning frame_number and control_state from that message + rest of buffer
def decode_buffer_first_message(buffer):
    try:
        message = buffer.decode()
        #print(message)
        split_message = message.split("|") # Can't be typical , because json
        frame_number = int(split_message[1])
        control_state_list = json.loads(split_message[2])
        control_state = game_logic.ControlState(control_state_list=control_state_list)

        remaining_buffer = (message.partition("|\n")[2]).encode()

        return frame_number, control_state, remaining_buffer
    except Exception as e:
        print(f"The following error occured trying to decode the received message: {e}")
        raise Exception("Message Decoding Error")


# Main game setup / loop
def run_game(player_number, remote_socket):
    # First time only setup code
    pygame.init()

    window = pygame.display.set_mode((game_logic.WINDOW_WIDTH, game_logic.WINDOW_HEIGHT))

    pygame.display.set_caption(game_logic.GAME_NAME)

    clock = pygame.time.Clock()

    game_state = game_logic.GameState(p1_x=100, p2_x=700)

    local_control_state = game_logic.ControlState() # Game starts with no controls pressed
    remote_control_state = game_logic.ControlState() # Game starts with no controls pressed

    # Game Loop
    frame_number = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if player closed game window
                running = False

            # Get local input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: # a moves player left
                    local_control_state.mv_l = True
                elif event.key == pygame.K_d: # d moves player right
                    local_control_state.mv_r = True
                elif event.key == pygame.K_s: # s is player's attack
                    local_control_state.atk = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a: # a moves player left
                    local_control_state.mv_l = False
                elif event.key == pygame.K_d: # d moves player right
                    local_control_state.mv_r = False
                elif event.key == pygame.K_s: # s is players's attack
                    local_control_state.atk = False

        
        
        # Introduce random delay to simulate bad network connection if that mode is enabled
        if player_number == 2 and BAD_CONNECTION:
            time.sleep(0.1*random.random())

        # Transmit our control state, then wait for other player's controls, may block here indefinetely
        remote_socket.send(encode_control_message(frame_number, local_control_state))

        # Buffer for received messages
        buffer = b""

        # Keep trying to receive inputs until it gets valid inputs
        while True:
            try:
                #remote_frame_number, remote_control_state = decode_control_message(remote_socket.recv(1024))
                buffer += remote_socket.recv(1024)
                remote_frame_number, remote_control_state, buffer = decode_buffer_first_message(buffer)

                break
            except Exception as e:
                print(f"Exception when receiving packet: {e}")
                continue

        game_logic.render_frame(game_state, window)

        # Player 1 is left, player 2 right
        if player_number == 1:
            game_state = game_logic.update_state(game_state, local_control_state, remote_control_state)
        elif player_number == 2:
            game_state = game_logic.update_state(game_state, remote_control_state, local_control_state)

        frame_number += 1

        clock.tick(30) # Lock the game at 30fps, all timings are based on framerate, so this controls run speed
    
    # Quit Pygame
    pygame.quit()

    # Finished successfully
    return 0

