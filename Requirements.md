# Requirements

What is required should go here


## Parent Driver file

 `./python3 driver.py <Port>` OR `./python3 driver.py <IP> <PORT>`

The driver file *shall*
    1. Start from the command line with the form above. If started via the first methon, it opens a socket with the given port and listens for connections
    1.
    1.
    1.
    1.

## Delay Based Netcode Version

 'delay_netcode.py'

The delay based netcode *shall*
    1. Wait until it has received control inputs over the network for the other play before advancing the frame
    2. Not store any history of game state or controller inputs outside of the current frame

## Rollback Netcode Version

The rollback netcode version *shall*
    1.

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

    functionality - what should the system do?
    performance - goals for speed, size, energy efficiency, etc.
    compliance - with federal/state law or institutional policy
    compatibility - with standards or with existing systems
    security - against a specific threat model under certain trust assumptions
    cost - goals for cost, if system operation incurs costs
    timeline - when will various part of the system be completed? what are the deadlines?
    hardware/software - what hardware or software must be purchased or provisioned?
    personnel - who will work on this project?
