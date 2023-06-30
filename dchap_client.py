#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3 as sql
import socket
from stribog import stribog
from Crypto.Random import get_random_bytes


# In[2]:


class chap_client():
    def __init__(self):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hasher=stribog()
        self.server_password='qwerty1234'
    def connect(self,IP='127.0.0.1',port=9037):
        self.socket.connect((IP,port))
        command='-h'
        #Ввод клиентом команд
        while command!='q':
            command=input('Print -h for help\n')
            command_words=command.split(' ')
            if(command_words[0]=='-h'):
                print('It is server which can registrate and authenticate you.\nTo registrate use command: reg <username:password>\nTo authenticate use command: auth <username:password>\n\n\n')
                continue            
            if(len(command_words)!=2):
                print('print(Enter username and password in that way: <login:password>)')
                continue
            elif(command_words[0]=='reg'):
                if(':' not in command_words[1]):
                    print('Enter username and password in that way: <login:password>')
                    continue
                client_logopass=bytes(command, 'utf-8')
                client_challenge=get_random_bytes(16)                
                client_reg_req=client_logopass
                self.socket.sendall(client_reg_req)
                self.socket.sendall(client_challenge)
                recv_data=self.socket.recv(1024)
                print(recv_data)
            #Если команда auth
            elif(command_words[0]=='auth'):
                if(':' not in command_words[1]):
                    print('Enter username and password in that way: <login:password>')
                    continue
                #парсинг команды
                username, password=command_words[1].split(':')
                
                #создание команды для пересылки серверу. Пробел в конце добавляется для включения в запрос испытания
                command=command_words[0]+' '+username
                client_auth_req=bytes(command, 'utf-8')
                client_challenge=get_random_bytes(16)
                print('Random challenge produced: '+client_challenge.hex())
                self.socket.sendall(client_auth_req)
                self.socket.sendall(client_challenge)
                
                #получение ответа от сервера. Два ответа, хэш-значение испытания от клиента и следом испытание от сервера
                hashed_client_challenge=self.socket.recv(1024)
                server_challenge=self.socket.recv(1024)
                true_hashed_client_challenge=self.hasher.haash(client_challenge, bytes(self.server_password,'utf-8'))
                if(true_hashed_client_challenge!=hashed_client_challenge):
                    print('Failed to authenticate server')
                    self.socket.close()
                else:
                    print('Server successsfully authicated')
                    
                #аутентификация на хэш-испытании, полученном от сервера
                print('Got challenge from server: '+server_challenge.hex())
                hashed_server_challenge=self.hasher.haash(server_challenge, bytes(password, 'utf-8'))
                self.socket.sendall(hashed_server_challenge)
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


# In[ ]:


b'sdfsd:fdfs'+get_random_bytes(16)


# In[ ]:




