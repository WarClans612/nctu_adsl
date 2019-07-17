#!/usr/bin/env python
# coding: utf-8

# In[7]:


from ArticutAPI.ArticutAPI import Articut
import json

try:
    accountFile = os.path.join(os.path.dirname(__file__), '../account.info')
    with open(accountFile) as f:
        accountInfoDICT = json.loads(f.read())
    articut = Articut(username=accountInfoDICT["email"], apikey=accountInfoDICT["apikey"])
except:
    articut = Articut()

from pprint import pprint

if __name__ == '__main__':
    input_string = "聊天機器人開發。"

    result = articut.parse(input_string, userDefinedDictFILE="./UserDefinedDictFile.json")
    pprint(result)

    #result = articut.versions()
    #pprint(result)


# In[ ]:




