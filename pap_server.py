#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3 as sql
import socket


# In[2]:


class pap_server():
    def __init__(self):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 9095))
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
        client_login,client_pass=client_data.split(':')
        with self.db:
            cur = self.db.cursor()
            #проверка существования пользователя
            cur.execute("SELECT * FROM `LOGPASS` WHERE Login=? AND Password=?",(client_login, client_pass))
            user_data_in_base_check=cur.fetchall()
            if(user_data_in_base_check==[]):
                msg='Oops, something wrong. Please, try again.'
            else:
                msg='Welcome, '+client_login
        return(msg)
    def start(self):
        self.socket.listen(10)
        while True:
            client_socket, client_addres=self.socket.accept()
            print('Connected by',client_addres)
            while True:
                data=client_socket.recv(1024)
                data=data.decode()
                print(data)
                command, client_data=data.split(' ')
                if(command=='reg'):
                    answer=bytes(self.registrate_new_client(client_data),'utf-8')
                    client_socket.sendall(answer)
                if(command=='auth'):
                    answer=bytes(self.authentication(client_data),'utf-8')
                    client_socket.sendall(answer)
                if not data:
                    break;
            client_socket.close()
        


# In[3]:


def main():
    s=pap_server()
    s.use_db('test.db')
    s.start()


# In[ ]:


if (__name__=='__main__'):
    main()


# In[ ]:




