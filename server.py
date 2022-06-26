#Import the Libraries
import socket
import threading                                                

#Local Host
host = '127.0.0.1'                                                      

#Choosing unreserved port
port = 7976                                                             

#socket initialization
# socket.AF_INET means socket belong to IPV4 Family
# socket.SOCK_STREAM means connection configured using TCP Protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              

#binding host and port to socket
server.bind((host, port))                                               
server.listen()

clients = []
nicknames = []

#broadcast function declaration
def broadcast(message):                                                 
    for client in clients:
        client.send(message)

def handle(client):                                         
    while True:
        try:                                                            
            #recieving valid messages from client
            message = client.recv(1024)
            broadcast(message)
        except:                                                         
            #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

#accepting multiple clients

# During listening our server is waiting, therefore our code won't receive multiple SMS send from client 
# To tackle this we need to apply multithreading, therefore I did the same to receiving method 
# So as it can keep receiving independently without blocking the our app
def receive():                                                          
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))       
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
