'''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
-Meron Tesfazghi 3066795
-server.py
-the program uses socket programming to receive a file from the client 
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'''
import socket 
import sys 
import os
from datetime import datetime  
import json

def server():
    serverPort = 13000 #server port #
    
    #Welcome message + menu
    welcome="Welcome to our system.\nEnter your username: "
    menu='''\nPlease select the operation:
            1) View uploaded files' information
            2) Upload a file
            3) Terminate the connection
            Choice: '''
    
    #create a server socket
    try:
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as e:
        print("Error in the server socket creation: ",e)
        sys.exit(1)
        
    try:
        serverSocket.bind(('',serverPort)) #bind the server socket
    except socket.error as e:
        print("Error in the server socket binding: ",e)
        sys.exit(1)
        
    serverSocket.listen(1)  #let the server socket listen to a client
    
    while 1:
        try:
            #accept connection
            connectionSocket,addr = serverSocket.accept()
            
            connectionSocket.send(welcome.encode('ascii'))
            user = connectionSocket.recv(2048).decode('ascii')
            
            if user == 'user1':
                connectionSocket.send(menu.encode('ascii'))
                choice = connectionSocket.recv(2048).decode('ascii')
                
                
                #use loop to repeatedly ask  for choice
                while (choice in ['1', '2']):
                    if choice == '1':
                                               
                        metadata={}
                        #load dictionary from json and send as string to client
                        if os.path.isfile("Database.json"):
                            #send header of print statement
                            header = "Name\t\tSize (Bytes)\t\tUpload Date and time"
                            connectionSocket.send(header.encode('ascii'))                             
                            with open("Database.json", 'r') as data_file:
                                metadata = json.load(data_file)
                            
                            connectionSocket.send(str(metadata).encode('ascii'))
                            
                    #if user choosed to upload a file
                    elif choice == '2':
                        metadata={}
                        req="Please provide the file name: "
                        connectionSocket.send(req.encode('ascii'))
                        
                        try:
                            #filename + file size
                            summary = connectionSocket.recv(2048).decode("ascii")
                            summary_lst = summary.split("\n")
                            name = summary.split("\n")[0]
                            size = int(summary.split("\n")[1])
                            
                            #send confirmation to server to start uploading
                            confirmation = "OK "+ summary_lst[1]
                            connectionSocket.send(confirmation.encode('ascii'))
                            
                            #open the new file and receive the file piece by piece using the loop
                            newfile = open(name, "wb")
                            filepart = connectionSocket.recv(int(size/2))
                            newfile.write(filepart)
                            
                            current = len(filepart) #to used to break the loop
                            while current < size:
                                filepart = connectionSocket.recv(int(size/2))
                                newfile.write(filepart)
                                current += len(filepart)
                                
                                #send  completion message and break loop
                                if current == size:
                                    status = "Upload process completed"
                                    connectionSocket.send(status.encode('ascii'))
                                    newfile.close()
                                    break
                            
                            #if json exists, load and update or 
                            if os.path.isfile("Database.json"):
                                with open("Database.json", 'r') as data_file:
                                        metadata = json.load(data_file)
                            metadata[name]={}
                            metadata[name]["size"] = str(size)
                            metadata[name]["time"] = str(datetime.now())
                            
                            with open ("Database.json", 'w') as data_file:
                                json.dump(metadata, data_file, indent = 2) 
                            
                        except socket.error as e:
                            print('An error occurred: ',e)
                            
                    
                    connectionSocket.send(menu.encode('ascii'))
                    choice = connectionSocket.recv(2048).decode('ascii')
                 
                #send message to client and close connection
                if (choice == '3'):
                    terminate="Connection terminated"
                    connectionSocket.send(terminate.encode('ascii'))
                    connectionSocket.close()
            #if user enters incorrect username
            else:
                disconnect="Incorrect username. Connection Terminated."
                connectionSocket.send(disconnect.encode('ascii'))
                connectionSocket.close()
        except socket.error as e:
            print('An error occurred: ',e)
    
            
################################################################################

if __name__ == "__main__":
    server()
