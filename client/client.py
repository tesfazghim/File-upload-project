'''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
-Meron Tesfazghi 3066795
-client.py
-the program uses socket programming to send a file to the server 
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'''
import socket 
import sys 
import os
import datetime  
import json 

def client():
    
    #server name and port number
    serverName=input("Enter the server name or IP adress: ")
    serverPort = 13000
    
    #create a socket for communication
    try:
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as e:
        print("Error in client socket creation: ",e)
        sys.exit(1)
        
    try:
        #start a connection
        clientSocket.connect((serverName, serverPort))
        
        #receive first message which is the welcome + menu
        msg=clientSocket.recv(2048).decode('ascii')
        user=input (msg)                           
        clientSocket.send(user.encode('ascii'))    
        
        if user == 'user1':
            menu = clientSocket.recv(2048).decode('ascii')
            choice = input (menu)
            clientSocket.send(choice.encode('ascii'))
            #loop to keep asking for choice until 3 is hit
            while (choice in ['1', '2']):                
                
                if choice == '1':
                    print(clientSocket.recv(2048).decode('ascii'))
                    
                    data = clientSocket.recv(2048).decode('ascii')              
                    print_dict(data)
                    
                #if user choosed to upload a file
                elif choice == '2':
                    req = clientSocket.recv(2048).decode('ascii')
                    filename = input(req)
                    #if file is in directory then go ahead and upload
                    if os.path.isfile(filename):
                        filesize = os.path.getsize(filename) #size of file
                        
                        summary = filename + "\n" + str(filesize)
                        clientSocket.send(summary.encode('ascii')) #file info
                        
                        confirmation=clientSocket.recv(2048).decode('ascii')
                        print(confirmation)
                        
                        #open the file and send the file piece by piece using the loop
                        with open(filename, "rb") as file:
                            filepart = file.read(int(filesize/2))
                            clientSocket.send(filepart)
                            current = len(filepart) #used to break 
                            
                            while filepart != "":
                                filepart = file.read(int(filesize/2))
                                clientSocket.send(filepart)
                                current += len(filepart)
                                
                                #print completion message and break loop
                                if current == filesize:
                                    status = clientSocket.recv(2048).decode('ascii')
                                    print(status)
                                    file.close()
                                    break
                #get new choice
                menu = clientSocket.recv(2048).decode('ascii')
                choice = input(menu)
                clientSocket.send(choice.encode('ascii'))           
                                
            #terminate connection
            if choice == '3':
                print(clientSocket.recv(2048).decode('ascii'))
                clientSocket.close()
        
        #if user enters incorrect username 
        else:
            disconnect = clientSocket.recv(2048).decode('ascii')
            print(disconnect)
            clientSocket.close()
              
        
    except socket.error as e:
        print('An error occurred: ',e)
        
#helper function to print the dictionary      
def print_dict(data):

    metadata = data.replace("'","\"")
    metadata = json.loads(metadata)
    for name in metadata:
        print(f"{name:<15} {metadata[name]['size']:<23} {metadata[name]['time']}")
                
        
################################################################################
if __name__ == "__main__":
    client()
