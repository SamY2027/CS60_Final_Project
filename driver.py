# Main driver program for our netocode project
# Takes command line args / user input for game options
# Calls other modules to run the game

import sys
import socket

COMMAND_USAGE_INSTRUCTIONS = "Usage: (Server) python3 driver.py <Port> OR (Client) python3 driver.py <IP> <Port>"

# Returns mode, ip, port
def parse_args(command_arguments):
    # 1 Argument, expects <Port>
    if len(command_arguments) == 2:
        try:
            port = int(command_arguments[1])

        # Occurs if input text is not an integer    
        except ValueError:
            print("<Port> must be a numerical value!")
            print(COMMAND_USAGE_INSTRUCTIONS)
            sys.exit(1)
        
        if port < 1 or port > 65535:
            print("<Port> must be a numerical value between 1 and 65535!")
            print(COMMAND_USAGE_INSTRUCTIONS)
            sys.exit(1)

        # Return values as server
        return "Server", None, port
    
    # 2 Arguments, expects <IP> <Port>
    elif len(command_arguments) == 3:
        ip_address = command_arguments[1]

        try:
            socket.inet_aton(ip_address) # Check if valid IP as per https://stackoverflow.com/questions/3462784/check-if-a-string-matches-an-ip-address-pattern-in-python
        except:
            print("<IP> must be a valid IP address!")
            print(COMMAND_USAGE_INSTRUCTIONS)
            sys.exit(1)

        try:
            port = int(command_arguments[2])

        # Occurs if input text is not an integer    
        except ValueError:
            print("<Port> must be a numerical value!")
            print(COMMAND_USAGE_INSTRUCTIONS)
            sys.exit(1)
        
        if port < 1 or port > 65535:
            print("<Port> must be a numerical value between 1 and 65535!")
            print(COMMAND_USAGE_INSTRUCTIONS)
            sys.exit(1)
        
        # Return values as client
        return "Client", ip_address, port
    else:
        print("Invalid number of command arguments!")
        print(COMMAND_USAGE_INSTRUCTIONS)
        sys.exit(1)

# Get the mode to run the game in for server
def get_mode():
    # Choose netcode type
        mode = None
        while mode == None:
            print("Enter the number corresponding to the mode you want to run in:\n(1) Test\n(2) Delay\n(3) Rollback")
            mode = input()
            try:
                mode = int(mode)
                if mode == 1:
                    mode = "Test"
                elif mode == 2:
                    mode = "Delay"
                elif mode == 3:
                    mode = "Rollback"
                else:
                    print("Please select a valid mode!")
                    mode = None
            except:
                print("Please enter a valid integer!")
                mode = None
        return mode



if __name__ == "__main__":
    role, ip_address, port = parse_args(sys.argv)
    print(role, ip_address, port)

    if role == "Server":
        mode = get_mode() # Possibilities are "Test", "Delay" and 'Rollback
        print(mode)

        # Open socket and wait for client to connect on given port
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP

        listen_socket.bind(('', port))

        listen_socket.listen(5)

        print("Waiting for client to connect on port " + str(port))
        client_socket, client_address = listen_socket.accept()

        print("Client connected", client_socket, client_address)

        listen_socket.close() # Program only handles one connection, so no longer need to listen

        client_socket.send(mode.encode()) # Send the current mode to the client

        # Run based on current mode
        if mode == "Test":
            pass
        elif mode == "Delay":
            pass
        elif mode == "Rollback":
            pass

        client_socket.close()

    elif role == "Client":
        # Connect to server at given IP and port
        print("Connecting to server at", ip_address, port)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((ip_address, port))
        print("Connected to server")

        # Get mode from server
        mode = server_socket.recv(1024).decode() # Valid options are Test, Delay and Rollback

        # Run based on received mode
        if mode == "Test":
            pass
        elif mode == "Delay":
            pass
        elif mode == "Rollback":
            pass
        else: # Invalid mode received
            print("Invalid Mode Received!")

        server_socket.close()
    else:
        print("Invalid Role!")
