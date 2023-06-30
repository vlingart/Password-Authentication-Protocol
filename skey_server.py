#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3 as sql
import socket
from stribog import stribog
from Crypto.Random import random


# In[2]:


#количество возможных транзакций на одном ключе
max_trans=1000


# In[3]:



class skey_server():
    def __init__(self):
        self.hasher=stribog()
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 9099))
    def use_db(self,data_base_name):
        self.db = sql.connect('bases/'+data_base_name)
    def registrate_new_client(self,client_data):
        client_login,client_key=client_data.split(':')
        with self.db:
            cur = self.db.cursor()
            #проверка наличия пользователя и добавление нового
            #try:
            sql_command="CREATE TABLE IF NOT EXISTS `{login}` (`OTP` STRING, `TID` STRING)".format(login=client_login)
            cur.execute(sql_command)
            OTP=bytes(client_key, 'utf-8')
            for ind in range (max_trans):
                OTP=self.hasher.haash(OTP)
                sql_command="INSERT INTO `{login}` VALUES (?,?)".format(login=client_login)
                cur.execute(sql_command,(OTP.hex(), ind))
            #except:
                #return('Sorry, user with current login exists, try another login')
        return('You are successfully registrated!')
    #Аутентификация пользователей
    def authentication(self,client_data):
        #получение данных от клиента
        Username=client_data
        print(Username + ' trying to login')
        TID=bytes(str(random.randint(500,1000)),'utf-8')
        self.client_socket.sendall(TID)
        TID=int(TID.decode())
        with self.db:
            cur = self.db.cursor()
            try:
                print(TID)
                sql_command="SELECT OTP FROM `{user}` WHERE TID=?".format(user=Username)
                cur.execute(sql_command,(TID-1, ))
                user_password_in_base_check = cur.fetchall()[0][0]
                client_OTP=self.client_socket.recv(1024).hex()
                if(client_OTP==user_password_in_base_check):
                    msg='Welcome, '+Username
                else:
                    msg='Oops, something wrong. Please, try again.'
            except:
                msg='Oops, something wrong. Please, try again.'
        return(msg)
    def start(self):
        self.socket.listen(10)
        while True:
            self.client_socket, self.client_addres=self.socket.accept()
            print('Connected by',self.client_addres)
            while True:
                data=self.client_socket.recv(1024)
                data=data.decode()
                print(data)
                command, client_data=data.split(' ')
                if(command=='reg'):
                    answer=bytes(self.registrate_new_client(client_data),'utf-8')
                    self.client_socket.sendall(answer)
                if(command=='auth'):
                    answer=bytes(self.authentication(client_data),'utf-8')
                    self.client_socket.sendall(answer)
                if not data:
                    break;
            self.client_socket.close()


# In[4]:


def main():
    s=skey_server()
    s.use_db('test1.db')
    s.start()


# In[ ]:


if(__name__=='__main__'):
    main()


# In[ ]:




