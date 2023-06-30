#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pygost.gost34112012256 import GOST34112012256


# In[2]:


class stribog():
    def __init__(self):
        self.hash_maker=GOST34112012256()
    #модуль обработки строковых данных
    def string_preproc(self,string_data):
        if(type(string_data)!=bytes):
            try:
                byts=bytes(string_data, 'utf-8')
            except:
                raise ValueError('Не удалось представить строку в виде набора байт')
            return(byts)
        else:
            return(string_data)
    #модуль шифрования ГОСТ 34.11_2012 СТРИБОГ. На вход получает строки для хэширования (хэш получается от конкатенации строк), на выходе строка байт
    def haash(self,*args):
        for word in args:
            word=self.string_preproc(word)
            self.hash_maker.update(word)
            digest=self.hash_maker.digest()
        return(digest)


# In[ ]:




