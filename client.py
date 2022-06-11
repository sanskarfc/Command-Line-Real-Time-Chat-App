
import socket
import threading
nickname = input("Choose your nickname: ")

#socket initialization
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      

#connecting client to server
client.connect(('127.0.0.1', 7976))                             

def receive():
    while True:                                                 
        try:
            #making valid connection
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:                                                 
            #case on wrong ip/port details
            print("An error occured!")
            client.close()
            break

def write():
    while True:                                                 
        #message layout
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

#receiving multiple messages
receive_thread = threading.Thread(target=receive)               
receive_thread.start()

#sending messages 
write_thread = threading.Thread(target=write)                   
write_thread.start()