#Cleint side GUI Chat Room
import tkinter, socket, threading
from tkinter import DISABLED, VERTICAL, END
from tkinter.font import NORMAL

#Window
root = tkinter.Tk()
root.title("Chat Client")
root.iconbitmap("message_icon.ico")
root.geometry("600x600")
root.resizable(0,0)


#fonts and colors
my_font = ('SimSun', 14)
light_grey = "#CDCDCD"
royal_blue = "#1d1bf9"
root.config(bg=light_grey)


#Socket constants
ENCODER = "utf-8"
BYTESIZE = 1024
global client_socket 

#Functions
def connect():
    '''Connect to a server at a given ip/port address'''
    global client_socket 

    #Clears chat when connecting
    my_listbox.delete(0, END)

    name = name_entry.get()
    ip = ip_entry.get()
    port = port_entry.get()

    #Only try to make a connection if all fields are filled
    if name and ip and port:
        my_listbox.insert(0, f"{name} is waiting to connect to {ip} at {port}...")

        #Create client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, int(port)))

        #verify connection is valid
        verify_connection(name)
    else:
        my_listbox.insert(0, "insufficient information to make connection...")



def verify_connection(name):
    '''Verify that the server connection is valid and pass required info'''
    global client_socket

    flag = client_socket.recv(BYTESIZE).decode(ENCODER)

    if flag == 'NAME':
        client_socket.send(name.encode(ENCODER))
        message = client_socket.recv(BYTESIZE).decode(ENCODER)

        if message:
            my_listbox.insert(0, message)

            #change button states
            connect_button.config(state=DISABLED)
            disconnect_button.config(state=NORMAL)
            send_button.config(state=NORMAL)

            name_entry.config(state=DISABLED)
            ip_entry.config(state=DISABLED)
            port_entry.config(state=DISABLED)


            #Create thread to continously receive messages from server
            receive_thread = threading.Thread(target=receive_message)
            receive_thread.start()
        
        else:
            #No verification message received
            my_listbox.insert(0, "Connection not verified. Goodbye...")
            client_socket.close()
    else:
        #No name flag sent, connection refused
        my_listbox.insert(0, "Connection refused. Goodbye...")
        client_socket.close()

def disconnect():
    '''Disconnect from server'''
    global client_socket

    client_socket.close()

    #change button states
    connect_button.config(state=NORMAL)
    disconnect_button.config(state=DISABLED)
    send_button.config(state=DISABLED)
    name_entry.config(state=NORMAL)
    ip_entry.config(state=NORMAL)
    port_entry.config(state=NORMAL)

def send_message():
    '''Send message to the server to be broadcasted'''
    global client_socket

    message = input_entry.get()
    client_socket.send(message.encode(ENCODER))
    input_entry.delete(0, END)

def receive_message():
    '''Receive an incoming message form the server'''
    global client_socket

    while True:
        try: 
            #receive incoming message from server
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            my_listbox.insert(0, message)
        except:
            my_listbox.insert(0, "Closing the connection. Goodbye...")
            disconnect()
            break

#GUI layout
info_frame = tkinter.Frame(root, bg=light_grey)
output_frame = tkinter.Frame(root, bg=light_grey)
input_frame = tkinter.Frame(root, bg=light_grey)
info_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()

#Info Frame layout
name_label = tkinter.Label(info_frame, text="Client Name: ", font=my_font, fg=royal_blue, bg=light_grey)
name_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
ip_label = tkinter.Label(info_frame, text="Host IP: ",  font=my_font, fg=royal_blue, bg=light_grey)
ip_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
port_label = tkinter.Label(info_frame, text="Port Num: ", font=my_font, fg=royal_blue, bg=light_grey)
port_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font, width=10)
connect_button = tkinter.Button(info_frame, text="Connect", font=my_font, bg=royal_blue, fg="#f3f3fe", borderwidth=5, width=10, command=connect)
disconnect_button = tkinter.Button(info_frame, text="Disconnect", font=my_font, bg=royal_blue, fg="#f3f3fe", borderwidth=5, width=10, state=DISABLED, command=disconnect)

name_label.grid(row=0, column=0, padx=2, pady=10)
name_entry.grid(row=0, column=1, padx=2, pady=10)
port_label.grid(row=0, column=2, padx=2, pady=10)
port_entry.grid(row=0, column=3, padx=2, pady=10)
ip_label.grid(row=1, column=0, padx=2, pady=5)
ip_entry.grid(row=1, column=1, padx=2, pady=5)
connect_button.grid(row=1, column=2, padx=4, pady=5)
disconnect_button.grid(row=1, column=3, padx=4, pady=5)

#Output frame layout
my_scollbar = tkinter.Scrollbar(output_frame, orient=VERTICAL)
my_listbox = tkinter.Listbox(output_frame, height=20, width=55, borderwidth=3, bg=light_grey, fg=royal_blue, font=my_font, yscrollcommand=my_scollbar.set)
my_scollbar.config(command=my_listbox.yview)

my_listbox.grid(row=0, column=0)
my_scollbar.grid(row=0, column=1, sticky="NS")

#Input frame layout
input_entry = tkinter.Entry(input_frame, width=45, borderwidth=3, font=my_font)
send_button = tkinter.Button(input_frame, text="Send", borderwidth=5, width=10, font=my_font, bg=royal_blue, fg="#f3f3fe", state=DISABLED, command=send_message)
input_entry.grid(row=0, column=0, padx=5, pady=5)
send_button.grid(row=0, column=1, padx=5, pady=5)


root.mainloop()
