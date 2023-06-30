#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3 as sql
import socket
from stribog import stribog
from Crypto.Random import get_random_bytes


# In[2]:


#количество возможных транзакций на одном ключе
max_trans=1000


# In[3]:


class skey_client():
    def __init__(self):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hasher=stribog()
    def connect(self,IP='127.0.0.1',port=9099):
        self.socket.connect((IP,port))  
        command='-h'
        while command!='q':
            command=input('Print -h for help\n')
            command_words=command.split(' ')
            if(command_words[0]=='-h'):
                print('It is server which can registrate and authenticate you.\nTo registrate use command: reg <username:password>\nTo authenticate use command: auth <username:password>\n\n\n')
           
            #функция регистрации
            elif(command_words[0]=='reg'):
                if(':' not in command_words[1]):
                    print('Enter username and password in that way: <login:password>')
                data=bytes(command, 'utf-8')
                user,key=command_words[1].split(':')
                self.socket.sendall(data)
                recv_data=self.socket.recv(1024)
                print(recv_data)
                
                #создание базы OTP пользователя
                if(recv_data==b'You are successfully registrated!'):
                    user_bd=sql.connect('client_bases/'+user+'.bd')
                    with user_bd:
                        cur = user_bd.cursor()    
                        sql_command="CREATE TABLE IF NOT EXISTS `OTPS` (`OTP` STRING, `TID` STRING)"
                        cur.execute(sql_command)  
                        OTP=bytes(key, 'utf-8')
                        for ind in range(max_trans):
                            OTP=self.hasher.haash(OTP)
                            sql_command="INSERT INTO `OTPS` VALUES (?,?)"
                            cur.execute(sql_command,(OTP.hex(), ind))  
                            
            #функция авторизации
            elif(command_words[0]=='auth'):
                print('Enter username')
                username=command_words[1]
                command=command_words[0]+' '+username
                data=bytes(command, 'utf-8')
                self.socket.sendall(data)
                TID=self.socket.recv(1024)
                TID=int(TID.decode())
                print('TID: ', TID)
                user_bd=sql.connect('client_bases/'+username+'.bd')
                try:
                    user_bd=sql.connect('client_bases/'+username+'.bd')
                    with user_bd:
                        cur = user_bd.cursor()    
                        sql_command="SELECT OTP FROM OTPS WHERE TID=?"
                        cur.execute(sql_command,(TID-1,))
                        client_OTP=cur.fetchall()[0][0]
                        print(client_OTP)
                        print('your OTP is '+client_OTP)
                except:
                        pass
                client_OTP=input('Enter your OTP\n')
                self.socket.sendall(bytes.fromhex(client_OTP))
                answer=self.socket.recv(1024)
                print(answer)


# In[ ]:


def main():
    c=skey_client()
    c.connect()
if(__name__=='__main__'):
    main()


# In[ ]:


cur.

