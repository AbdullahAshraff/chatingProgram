import socket
import threading
'''
[msg] means what i send is a message
[usr] means what i send is a new username connected

[uco] USERNAME ADDRESS                                     means user connected
[udi] USERNAME ADDRESS                                     means user disconnected
[msg] [SENDER_USERNAME] [RECEIVER_ADDRESS] MESSAGE


[uco][]
'''
all_sockets = []

def handle_client(connsocket : socket.socket,address):
    global all_sockets
    all_sockets.append((connsocket,address))
    username = connsocket.recv(1024).decode()
    print(f"----- New Connection from [{address}], username: {username}")
    for i in all_sockets:
        i[0].sendall(f"[uco] {username} {address}".encode('utf-8'))


    while True:
        try:
            received_line = connsocket.recv(1024).decode()
        except ConnectionResetError:
            print(f"xxxxx Connection FORCIBLY ENDED by [{address}], username: {username}")
            connsocket.close()
            all_sockets.remove((connsocket,address))
            for i in all_sockets:
                i[0].sendall(f"[udi] {username} {address}".encode('utf-8'))
            return
        if received_line ==f"{username},DISCONNECT": 
            connsocket.close()
            print(f"----- Connection ENDED for [{address}], username: {username}")
            all_sockets.remove((connsocket,address))
            for i in all_sockets:
                i[0].sendall(f"[udi] {username} {address}".encode('utf-8'))
            return
        if received_line=='': continue
        rec_ls = received_line.split(sep='`',maxsplit=3)
        if rec_ls[2]=='[All]':
            for i in all_sockets:
                i[0].sendall(f"[msg] [{username}] {rec_ls[3]}".encode('utf-8'))
        else:
            for i in all_sockets:
                if str(i[1]) == str(rec_ls[2][1:-1]):
                    i[0].sendall(f"[msg] [{username}] {rec_ls[3]}".encode('utf-8'))




s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(f"the host ip is {(socket.gethostbyname(socket.gethostname()))}. Edit it in the file \"theServerIP\" to make the client connect to the server.")
with open("theServerIP") as file:
    s.bind((socket.gethostname(),int(file.readlines()[1])))
print("------ Server Started")
s.listen()
while True:
    connsocket, addr = s.accept()
    threading.Thread(target=handle_client,args=(connsocket,addr)).start()
    print(f"----- Active Connections are {threading.active_count()-1}")
