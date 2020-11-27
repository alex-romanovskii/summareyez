#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np

# pattern={
#     'text name without .txt':[
#         list of lists
#         ['question','Possible answer','Possible answer','Possible answer','Possible answer','Correct answer',]
#         .....
#     ]
# }

dict_questions={
    'lor':[
    ['ques1','q','w','r','t','q'],
    ['ques2','q','w','r','t','q'],
    ['ques3','q','w','r','t','q']
    ],
    'lorem':[
    ['ques1','q','w','r','t','q'],
    ['ques2','q','w','r','t','q'],
    ['ques3','q','w','r','t','q']
    ]
    
}

np.save("questions/questions.npy", dict_questions)

