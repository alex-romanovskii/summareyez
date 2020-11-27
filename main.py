#!/usr/bin/env python
# coding: utf-8

# In[3]:


from eyetrackergui import *

try:
    first_screen=First_screen()
    first_screen.mainloop()

    user_name=first_screen.user_name
    text_name=first_screen.user_text_name
    user_age=first_screen.user_age
    user_gender=first_screen.user_sex
    user_text=first_screen.user_text
    user_points=first_screen.points

    experiment_screen=Create_text(user_name,user_text,text_name,user_gender,
                                  user_age,points=user_points,eye_tracker=True,verbose=True,see_rectangle=True)  
    for i in range(150):
        x=random.random()
        y=random.random()
        try:
            experiment_screen.get_bbox(x,y)
            time.sleep(0.5)
        except TclError:
            break  
except AttributeError:
    pass
    
    


# In[ ]:




