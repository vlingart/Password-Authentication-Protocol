#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3 as sql
import socket
from stribog import stribog
from Crypto.Random import get_random_bytes


# In[2]:


class chap_server():
    def __init__(self):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 9094))
        self.hasher=stribog()
    #подключение базы данных
    def use_db(self,data_base_name):
        self.db = sql.connect('bases/'+data_base_name)
        with self.db:
            cur = self.db.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS `LOGPASS` (`Login` STRING, `Password` STRING)")    
    #Регистрация пользователей
    def registrate_new_client(self,client_data):
        client_login,client_pass=client_data.split(':')
        with self.db:
            cur = self.db.cursor()
            #проверка существования пользователя
            cur.execute("SELECT * FROM `LOGPASS` WHERE Login=?",(client_login,))
            user_registration_check=cur.fetchall()
            if(user_registration_check!=[]):
                return('Sorry, user with current login exists, try another login')
            #добавление нового пользователя
            cur.execute("INSERT INTO `LOGPASS` VALUES (?,?)",(client_login,client_pass))
        return('You are successfully registrated!')
    #Регистрация пользователей
    def authentication(self,client_data):
        Username=client_data
        print(Username + ' trying to login')
        #генерация и отправка случайного испытания
        Nonce=get_random_bytes(16)
        print('Generated random challenge: ', Nonce.hex())
        self.client_socket.sendall(Nonce)
        #получение хэш-значения от испытания на пароле пользователя
        client_hashed_Nonce=self.client_socket.recv(1024)
        print(Username+' sent hash: ' + client_hashed_Nonce.hex() )
        with self.db:
            cur = self.db.cursor()
            #проверка существования пользователя
            cur.execute("SELECT Password FROM `LOGPASS` WHERE Login=?",(Username, ))
            user_password_in_base_check=cur.fetchall()[0][0]
            if(user_password_in_base_check==[]):
                msg='Oops, something wrong. Please, try again.'
                return(msg)
            else:
                hashed_Nonce=self.hasher.haash(Nonce,bytes(user_password_in_base_check, 'utf-8'))
        if(hashed_Nonce==client_hashed_Nonce):
            msg='Welcome, '+Username
        else:
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
        


# In[3]:


def main():
    s=chap_server()
    s.use_db('test.db')
    s.start()


# In[ ]:


if (__name__=='__main__'):
    main()

