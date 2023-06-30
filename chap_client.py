#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket
from stribog import stribog


# In[2]:


class chap_client():
    def __init__(self):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hasher=stribog()
#подключение к серверу
    def connect(self,IP='127.0.0.1',port=9094):
        self.socket.connect((IP,port))
        command='-h'
 #ввод команд клиентом     
        while command!='q':
            command=input('Print -h for help\n')
            command_words=command.split(' ')
            if(command_words[0]=='-h'):
                print('It is server which can registrate and authenticate you.\nTo registrate use command: reg <username:password>\nTo authenticate use command: auth <username:password>\n\n\n')
            #регистрация на сервере
            elif(command_words[0]=='reg'):
                if(':' not in command_words[1]):
                    print('Enter username and password in that way: <login:password>')
                data=bytes(command, 'utf-8')
                self.socket.sendall(data)
                recv_data=self.socket.recv(1024)
                print(recv_data)
            #аутентификация на сервере    
            elif(command_words[0]=='auth'):
                if(':' not in command_words[1]):
                    print('Enter username and password in that way: <login:password>')
                username, password=command_words[1].split(':')
                command=command_words[0]+' '+username
                data=bytes(command, 'utf-8')
                self.socket.sendall(data)
                Nonce=self.socket.recv(1024)
                print('Got challenge', Nonce.hex())
                hashed_Nonce=self.hasher.haash(Nonce, bytes(password, 'utf-8'))
                self.socket.sendall(hashed_Nonce)
                recv_data=self.socket.recv(1024)
                print(recv_data)
        client_socket.close()
                


# In[3]:


def main():
    c=chap_client()
    c.connect()


# In[ ]:


if (__name__=='__main__'):
    main()


# In[5]:


c=stribog()


# In[ ]:


c

