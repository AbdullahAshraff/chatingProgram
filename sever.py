import socket
import threading
'''
[msg] means what i send is a message
[usr] means what i send is a new username connected
'''
all_sockets = []

def handle_client(connsocket : socket.socket,address):
    global all_sockets
    all_sockets.append(connsocket)
    username = connsocket.recv(1024).decode()
    print(f"----- New Connection from [{addr}], username: {username}")


    while True:
        try:
            msg = connsocket.recv(1024).decode()
        except ConnectionResetError:
            print(f"xxxxx Connection FORCIBLY ENDED by [{addr}], username: {username}")
            return
        if msg ==f"{username},DISCONNECT": 
            connsocket.close()
            print(f"----- Connection ENDED for [{addr}], username: {username}")
            all_sockets.remove(connsocket)
            return
        for i in all_sockets:
            i.sendall(f"[msg]{username}: {msg}".encode('utf-8'))




s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),1253))
print("------ Server Started")
s.listen()
while True:
    connsocket, addr = s.accept()
    threading.Thread(target=handle_client,args=(connsocket,addr)).start()
    print(f"----- Active Connections are {threading.active_count()-1}")
