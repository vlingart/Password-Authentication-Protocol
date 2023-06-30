#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket


# In[2]:


class pap_client():
    def __init__(self):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self,IP='127.0.0.1',port=9095):
        self.socket.connect((IP,port))
        command='-h'
        while command!='q':
            command=input('Print -h for help\n')
            command_words=command.split(' ')
            if(command_words[0]=='-h'):
                print('It is server which can registrate and authenticate you.\nTo registrate use command: reg <username:password>\nTo authenticate use command: auth <username:password>\n\n\n')
            elif(command_words[0]=='reg'):
                if(':' not in command_words[1]):
                    print('Enter username and password in that way: <login:password>')
                data=bytes(command, 'utf-8')
                self.socket.sendall(data)
                recv_data=self.socket.recv(1024)
                print(recv_data)
            elif(command_words[0]=='auth'):
                if(':' not in command_words[1]):
                    print('Enter username and password in that way: <login:password>')
                data=bytes(command, 'utf-8')
                self.socket.sendall(data)
                recv_data=self.socket.recv(1024)
                print(recv_data)
        client_socket.close()
                


# In[3]:


def main():
    c=pap_client()
    c.connect()


# In[ ]:


if(__name__=='__main__'):
    main()


# In[1]:





# In[2]:


a=stribog()
a.haash('aa')


# In[ ]:




