# Implementation Spec
Written by Sam Young and Aleksander Nowicki

## Driver File

### Definiton of Function Protypes

```python

# Parse command line arguments, Call various functions to execute program funcitonality
main():
    pass


```

### Detailed Pseudo Code

```python

def main():
    
    if len(command_arguments) > 2:
        role = server
        
        command_arguments[1] = port
    else:
        role = client
        command_arguments[1] = IP_address
        command_arguments[2] = port

    if role == server:
        bool debug_mode = get_user_input()

        netcode_type = get_user_input() # Options are "Delay" and "Rollback"

        if netcode_type == Rollback:
            delay_frames = get_user_input() # Get number of frames to delay by from user

        socket = listen on port # Wait for client to connect

        if netcode_type == Delay:
            send_message(socket, "Connected Delay")


        else: # Mode is Rollback
            send_message(socket, "Connected Rollback")

        # at this point, we have all the information we need to start the game in the correct mode as either server or client

        start_thread(get_local_input)

        start_thread(listen)

        start_thread(run_game)

    else: # Client
        socket = connect to IP_address on port via TCP

        mode = get_message(socket) # Get either Delay or Rollback message from server to decide mode

        if mode == Delay:

        else: # Mode is Rollback

# Thread functions

def get_local_input():


def listen():


def run_game():

```

### Testing Plan

Using dummy versions of the various delay, rollback and game logic functions which either print to stdout or otherwise idicate they were called can allow us to independently test mode selection.

TCP messages can be observed in wireshark for correct formatting.

The driver's TCP connection functionality can be tested before any actual game functionality is added by simply commenting out everything after initial connection.

A testing mode is built into this program which skips game functionality entirely and simply makes sure that control communications are being sent correctly. This will function both to test driver and either of the delay or rollback netcode modes.

## Game logic

This set of functions implements a very simple 2-player fighting game using the pygame library. This game is designed specifically
to function well with a rollback system. Game states and control input states are easily stored in special classes. Simulation
uses no floating point math and is deterministic on control inputs as to maintain consistency between remote devices.

### Data Structures

```python
# Stores the state of the game on a particular frame
# Contains 6 integer variables, (p1_x, p1_hp, p1_atk_frame, p2_x, p2_hp, p2_atk_frame)
# which together sumarize the entire state of the game
class GameState:

# Store control input for ONE player on a particular frame
# Contains 3 booleans representing whether each of that player's buttons are pressed on a given frame
# (mv_l (move left), mv_r (move  right) and atk (attack))
class ControlState:
```

### Definition of Function Prototypes

```python

# Render the given state of the game using pygame library
def render_frame(game_state: GameState, window):
# Window is a pygame surface where the game will be rendered

# Return the game state on the next frame given the current state (which is not modified) and both players' control inputs
def update_state(current_game_state: GameState, p1_control_state: ControlState, p2_control_state) -> GameState:

# Methods for GameState

def __init__(self, p1_x=0, p1_hp=100, p1_atk_frame=0, p2_x=0, p2_hp=100, p2_atk_frame=0, game_state_list=None):

# Human readable string summary good for debugging, contains all variable values
def __str__(self):

# Store all variable values in a list for simple storage and recall, order is same as in init
def make_list(self) -> list:

# Create a GameState instance from a list output by the above function, this is called by init if you pass a game_state_list
def load_from_list(self, game_state_list):

# Methods for ControlState

def __init__(self, mv_l=False, mv_r=False, atk=False, control_state_list=None):

# Human readable string summary good for debugging, contains all variable values
def __str__(self):

# Store all variable valeus in a list for simple storage and recall, order is same as in init
def make_list(self) -> list:

# Create a ControlState from a list output by the above function, this is called by init if you pass a control_state_list
def load_from_list(self, control_state_list):

```

### Testing Plan

game_local.py, while not part of the final product, utilizes the Game Logic functions and classes to implement the simple game as local multiplayer, where both players' inputs come from the same keyboard. This allows testing of Game Logic in isolation from issues potentially arising from the network. That way, we can go into testing notcodes without having to worry about bugs fundemental to the game itself