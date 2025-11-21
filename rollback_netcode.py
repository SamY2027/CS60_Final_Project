"""
Functions to run game from game_logic with rollback based netcode
The game moves on with solely the local player's input, 
listening on another thread, and if it receives a packet late it will
simulate the game state to catch up


TODO: currently getting desync errors where one computer gets ahead of another, need to probably rapidly simulate the game state and send packets in that case I guess
TODO: Also getting bug where local player moves with remote player's input - idk why, adding in checks for the sender didn't fix it
"""

import game_logic
import socket
import threading
import pygame
import copy
import json




# Globals - just have the list of inputs/game states

# List of dictionaries with keys: local_input, remote_input, game_state_str
rollback_list = []

# lock to make sure there's nothing weird
lock = threading.Lock()

# Number of frames back to to render
DELAY = 1

# Store player num for simulation

# Returns byte message in format FS,frame_number,control_state
def encode_control_message(frame_number, control_state):
    if player_num == 1:
        message = "FS1" + "|" + str(frame_number) + "|" + json.dumps(control_state.make_list())
    else:
        message = "FS2" + "|" + str(frame_number) + "|" + json.dumps(control_state.make_list())
    return message.encode()

# Returns frame_number, control_state, given bytes produced by encode_control_message
def decode_control_message(raw_bytes):
    message = raw_bytes.decode()
    message = message.split("|") # Can't be typical , because json
    if player_num == 1 and message[0] == "FS1":
        #received own message - discard
        print(message[0])
        raise Exception("wrong sender")
    if player_num == 2 and message[0] == "FS2":
        #received own message - discard
        raise Exception("wrong sender")

    frame_number = int(message[1])
    control_state_list = json.loads(message[2])
    control_state = game_logic.ControlState(control_state_list=control_state_list)
    return frame_number, control_state

def listen_thread(remote_socket):

    while True:
        try:
            remote_frame_number, remote_control_state = decode_control_message(remote_socket.recv(1024))
        except Exception:
            continue

        with lock:
            if frame_number == remote_frame_number:
                # Best case scenario - packet received on time
                # print("Packet received on time")
                    # check if local already appended its input
                if len(rollback_list) == frame_number:
                        # Not yet, append a new dictionary
                    rollback_list.append({
                            "local_input": copy.deepcopy(rollback_list[-1]["local_input"]),
                            "remote_input": remote_control_state.make_list(),
                            "game_state_list":None
                        
                    })
                elif len(rollback_list) > frame_number:
                    rollback_list[remote_frame_number]["remote_input"] = remote_control_state.make_list()
            elif frame_number > remote_frame_number:
                # print("packet received late")

                if rollback_list[remote_frame_number]["remote_input"] != remote_control_state.make_list():
                    # Overwrite the previous input and re-simulate game state
                    rollback_list[remote_frame_number]["remote_input"] = remote_control_state.make_list()

                    # Go up until the previous frame, since that'll be rendered
                    for i in range(remote_frame_number, frame_number):
                        if player_num == 1:
                            sim_game_state = game_logic.update_state(
                                game_logic.GameState(game_state_list=rollback_list[i-1]["game_state_list"]),
                                game_logic.ControlState(control_state_list=rollback_list[i]["local_input"]),
                                game_logic.ControlState(control_state_list=rollback_list[i]["remote_input"])

                            )
                        else:
                            sim_game_state = game_logic.update_state(
                                game_logic.GameState(game_state_list=rollback_list[i-1]["game_state_list"]),
                                game_logic.ControlState(control_state_list=rollback_list[i]["remote_input"]),
                                game_logic.ControlState(control_state_list=rollback_list[i]["local_input"])
                            )

                        if sim_game_state.make_list() == rollback_list[i]["game_state_list"]:
                            # end early - new input inconsequential
                            break
                        rollback_list[i]["game_state_list"] = sim_game_state.make_list()




            elif frame_number < remote_frame_number:
                # Worst case scenario - computers desynced/ running diff rates
                # Speed up to catch up to the remote
                print("running slow - desynced")


        # now handle the game state updates in the main loop

def run_game(player_number, remote_socket):
    # First time only setup code
    global player_num

    player_num = player_number

    pygame.init()

    window = pygame.display.set_mode((game_logic.WINDOW_WIDTH, game_logic.WINDOW_HEIGHT))

    pygame.display.set_caption(game_logic.GAME_NAME)

    clock = pygame.time.Clock()

    game_state = game_logic.GameState(p1_x=100, p2_x=700)

    local_control_state = game_logic.ControlState() # Game starts with no controls pressed
    remote_control_state = game_logic.ControlState() # Game starts with no controls pressed

    listener = threading.Thread(target=listen_thread, args=(remote_socket,), daemon=True)
    # Game Loop
    global frame_number # Mark as global to check against elsewhere
    frame_number = 0

    # Append frame zero's inputs (nothing) to the list
    # prevents index errors hopefully
    with lock:
        rollback_list.append({
                             "local_input": local_control_state.make_list(),
                             "remote_input": remote_control_state.make_list(),
                             "game_state_list":game_state.make_list()
        })
    running = True
    remote_socket.send(b'starting game')
    print(remote_socket.recv(1024))

    with lock:
        frame_number += 1

    listener.start()
    #print("started listener")
    

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        remote_socket.send(encode_control_message(frame_number, local_control_state))
        #print("sent packet")

        with lock:
            if len(rollback_list) > frame_number:
                rollback_list[frame_number]["local_input"] = local_control_state.make_list()
            elif len(rollback_list) == frame_number:
                rollback_list.append({
                        "local_input":local_control_state.make_list(),
                        "remote_input": copy.deepcopy(rollback_list[-1]["remote_input"])
                })
            else:
                # Error - somehow skipped a frame locally???
                #
                print("Error - desync?")

        with lock:
            game_logic.render_frame(game_logic.GameState(game_state_list=rollback_list[frame_number-1]["game_state_list"]), window)

        if player_number == 1:
            # Use the previous game states and the current inputs to calc new game state
            with lock:
                game_state = game_logic.update_state(
                        game_logic.GameState(game_state_list=rollback_list[frame_number-1]["game_state_list"]),
                        game_logic.ControlState(control_state_list=rollback_list[frame_number]["local_input"]),
                        game_logic.ControlState(control_state_list=rollback_list[frame_number]["remote_input"])
                                                )
            #game_state = game_logic.update_state(game_state, local_control_state, remote_control_state)
        elif player_number == 2:
            #game_state = game_logic.update_state(game_state, remote_control_state, local_control_state)
            with lock:
                game_state = game_logic.update_state(
                        game_logic.GameState(game_state_list=rollback_list[frame_number-1]["game_state_list"]),
                        game_logic.ControlState(control_state_list=rollback_list[frame_number]["remote_input"]),
                        game_logic.ControlState(control_state_list=rollback_list[frame_number]["local_input"])
                                                )
            

        with lock:
            rollback_list[frame_number]["game_state_list"] = game_state.make_list()
            #print(rollback_list[frame_number])


        with lock:
            frame_number += 1

        clock.tick(30) # Lock the game at 30fps, all timings are based on framerate, so this controls run speed
    
    # Quit Pygame
    pygame.quit()

    # Finished successfully
    return 0

