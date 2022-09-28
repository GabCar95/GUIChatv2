import socket, threading

#Define constants to be used
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024

#Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()


#Create two blank list to store connected client socket and their names
client_socket_list = []
client_name_list = []

def broadcast_message(message):
    '''Send a message to ALL clienmts connected to the server'''
    for client_socket in client_socket_list:
        client_socket.send(message)

def receive_message(client_socket):
    '''Receive an incoming message from a specific client and forward the message to be broadcasted'''
    while True:
        try:
            #Get the name of the given client
            index = client_socket_list.index(client_socket)
            name = client_name_list[index]

            #Receive meesage from client
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            message = f"{name}: {message}".encode(ENCODER)
            broadcast_message(message)

        except:
            #Find the index of the client socket in out list
            index = client_socket_list.index(client_socket)
            name = client_name_list[index]

            #Remove the client socket and name from the list
            client_socket_list.remove(client_socket)
            client_name_list.remove(name)

            #Close the client socket
            client_socket.close()

            #Broadcast that the client has left the chat
            broadcast_message(f"{name} has left the chat!".encode(ENCODER))
            break

def connect_client():
    '''Connect an incoming client to the server'''
    while True:
        #Accept any incoming client connection
        client_socket, client_address = server_socket.accept()
        print(f"Connect with {client_address}...")

        #Send a NAME flag to prompt the client for their name
        client_socket.send("NAME".encode(ENCODER))
        client_name = client_socket.recv(BYTESIZE).decode(ENCODER)

        #Add new client socket and client name to appropriate lists
        client_socket_list.append(client_socket)
        client_name_list.append(client_name)

        #Update the server, individual client, and ALL clients
        print(f"Name of the new client is {client_name}\n") #server
        client_socket.send(f"{client_name}, you have connected to the server!".encode(ENCODER)) #individual client
        broadcast_message(f"{client_name} has joined the chat!".encode(ENCODER))

        #Now that a new client has connected, start a new thread
        receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
        receive_thread.start()


#Start server
print("Server is listening for incoming connections...\n")
connect_client()
