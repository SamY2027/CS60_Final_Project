# Requirements

What is required should go here


## Parent Driver file

 `./python3 driver.py <Port>` OR `./python3 driver.py <IP> <PORT>`

The driver file *shall*:

1. Start from the command line with the form above. If started via the first method, it opens a socket with the given port and listens for connections. If started with the second option, connects to the driver at the given port and IP. 
1. Once a connection has been initiated, the driver allows for the selection of serveral options before the initiation of a game. 
    * Whether to initiate a game using the delay based protocol or the rollback protocol
    * If the game is using the rollback protocol, how much input delay to have
    * Whether to start a game in the debugging/test mode, which should only display whether the inputs are being correctly captured and sent
1. Once a game has been initiated, the driver starts several threads
    * One to handle the user input, send it via the send method in `server.py` and update the game state accordingly
    * One to update the gamestate at a constant rate based on the local input and the remote input
    * One to listen on the socket for inputs from the remote player, and call methods from `rollback.py` or `delay.py` to handle them
1. From here, the driver shall run until it receives a game over message from the game state handler, printing out a summary of the game and exiting. 

## Delay Based Netcode Version
 'delay_netcode.py'

The delay based netcode *shall*
1. Wait until it has received control inputs over the network for the other play before advancing the frame
2. Not store any history of game state or controller inputs outside of the current frame

## Rollback Netcode Version

The rollback netcode version *shall*
1. Do rollback things

## Game Logic Handler

The game logic *shall*
1. Implement a basic, proof-of-concept two-player fighting game with movement, multi-frame attack animations, a health-point system and a victory-condition
2. Implement game logic which is deterministic based on only control inputs and does not utilize floating point math to avoid inconsistency between machines
3. Implement game and controller states that can be easily summarized in a list to save, compare and send over the network
4. Render the game using only the previously mentioned game state
5. Be able to simulate several frames of gameplay in the time allotted before the next frame must be displayed


```
    Files needed:
        parent driver file
        Delay based network beacon version
        Rollback based network beacon version
        game logic handler
        
```

```
    functionality - what should the system do?
    performance - goals for speed, size, energy efficiency, etc.
    compliance - with federal/state law or institutional policy
    compatibility - with standards or with existing systems
    security - against a specific threat model under certain trust assumptions
    cost - goals for cost, if system operation incurs costs
    timeline - when will various part of the system be completed? what are the deadlines?
    hardware/software - what hardware or software must be purchased or provisioned?
    personnel - who will work on this project?
```
