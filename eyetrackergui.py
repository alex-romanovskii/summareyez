from tkinter import *
from tkinter import messagebox 
import os
from tkinter.ttk import Combobox 
from PIL import Image, ImageTk
import random
import time
import pandas as pd
import numpy as np

class First_screen(Tk):
    def __init__(self):
        super().__init__() 
        self.config(cursor='circle red') 
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight() 
        self.background_photo=ImageTk.PhotoImage(Image.open("background.jpg"))
        self.background = Label(self, image=self.background_photo)
        self.background.place(x=0, y=0)
        self.logo = ImageTk.PhotoImage(Image.open("logo.png"))
        self.draw_logo = Label(self, image=self.logo)
        self.draw_logo.place(relx=0.7, rely=0.1)
        self.font=("helvetica Bold", 20)
        self.texts=[text.split('.txt')[0] for text in os.listdir('texts')]
        self.title("SummerEyes")
        self.attributes('-fullscreen', True) 

        self.lbl_name = Label(self, text="Entry your name",font=self.font)
        self.lbl_name.place(relx=0.1, rely=0.1)        
        self.txt_name = Entry(self, width=8,font=self.font)
        self.txt_name.place(relx=0.3, rely=0.1)
        self.lbl_age = Label(self, text="Entry your age",font=self.font)
        self.lbl_age.place(relx=0.1, rely=0.2)
        self.spin_age = Spinbox(self, from_=18, to=30, width=3,font=self.font)  
        self.spin_age.place(relx=0.3, rely=0.2)
        self.lbl_sex = Label(self, text="Choose your sex",font=self.font)
        self.lbl_sex.place(relx=0.1, rely=0.3)
        self.combo_sex = Combobox(self,font=self.font,width=8)  
        self.combo_sex['values'] = ('Male','Female')
        self.combo_sex.place(relx=0.3, rely=0.3)
        self.lbl_choose_text = Label(self, text="Choose text",font=self.font)
        self.lbl_choose_text.place(relx=0.1, rely=0.4)
        self.combo = Combobox(self,font=self.font,width=8)  
        self.combo['values'] = self.texts
        self.combo.place(relx=0.3, rely=0.4)  
        self.chk_state = BooleanVar()  
        self.chk_state.set(False) 
        self.chk = Checkbutton(self, text='I want to see gaze point', var=self.chk_state,font=self.font)  
        self.chk.place(relx=0.1, rely=0.5)         
        self.btn = Button(self, text="START", command=self.clicked,font=self.font)  
        self.btn.place(relx=0.1, rely=0.7)
        self.btn_exit = Button(self, text="EXIT", command=self.destroy,font=self.font)  
        self.btn_exit.place(relx=0.2, rely=0.7)
    
    
    def clicked(self):
        user_name = self.txt_name.get()
        user_age=self.spin_age.get()
        user_sex=self.combo_sex.get()
        user_text=self.combo.get()
        points=self.chk_state.get()
        if len(user_name)==0 or len(user_sex)==0 or len(user_text)==0:
            messagebox.showinfo('Error', 'Try again')
        else:    
            self.user_name = user_name
            self.user_age=user_age
            self.user_sex=user_sex
            self.user_text_name=user_text
            self.user_text=(open('texts/{}.txt'.format(self.user_text_name),'r')).read()
            self.points=points
            self.destroy()
        
class Create_text(Tk):
    def __init__(self,user_name,text,text_name,user_gender,user_age,eye_tracker=False,see_rectangle=True,points=True,verbose=True):
        super().__init__() 
        self.start_time=time.time()
        self.config(cursor='circle red')
        self.user_name=user_name
        self.text_name=text_name
        self.user_gender=user_gender
        self.user_age=user_age
        self.text=text
        self.see_rectangle=see_rectangle
        self.points=points
        self.verbose=verbose
        self.title("SummerEyes")
        self.width = self.winfo_screenwidth() #get display width
        self.height = self.winfo_screenheight() #get display height
        self.attributes('-fullscreen', True) 
        self.font=("helvetica", 20)
        self.canvas_background="white" #backgroun color
        self.canvas = Canvas(self,bg=self.canvas_background,width=self.width, height=self.height)
        self.canvas.pack() #necessarily
        self.eye_tracker=eye_tracker # if x,y coordinates from 0 to 1 set eye_tracker=True to convert them to px
        self.start_position_x=40 #start text position (x)
        self.start_position_y=40 #start text position (y)
        self.fixation_number=0
        self.previous_fixation=None
        self.bbox_info=None
        self.print_text()

    def print_text(self):
        self.button_save = Button(self, text = "Save and Exit", command = self.quit, font=self.font,anchor=W)
        self.button_save.place(relx=0.03, rely=0.9)
        self.button_questions = Button(self, text = "Questions", command = self.questions, font=self.font,anchor=W)
        self.button_questions.place(relx=0.8, rely=0.9)
        
        
        bbox_info={}
        for index,sentenсe in enumerate(self.text.split(".")):
            if len(sentenсe)==0:
                continue
            sentenсe=sentenсe.lstrip()
            positions=[]
            for number,word in enumerate(sentenсe.split(" ")):
                if len(word)==0:
                    continue
                if number==len(sentenсe.split(" "))-1:
                    suffix='. '
                else:
                    suffix=' '
                sent_id = self.canvas.create_text(self.start_position_x, self.start_position_y, 
                    text=word+suffix,font=self.font,
                    justify=LEFT, fill="black",anchor=NW)
                bbox = self.canvas.bbox(sent_id) 
                if self.see_rectangle==True:
                    self.canvas.create_rectangle(bbox, outline="black") #draw word rectangles
                width=self.start_position_x + bbox[2] - bbox[0] + 5 
                x_left=self.start_position_x
                x_right=self.start_position_x+ bbox[2] - bbox[0]
                y_up=self.start_position_y
                y_down=self.start_position_y+ bbox[3] - bbox[1] 
                if width+120<self.width:
                    self.start_position_x += bbox[2] - bbox[0] 
                else:    
                    self.start_position_x=40
                    self.start_position_y+=40 
                positions.append([x_left,x_right,y_up,y_down])
            bbox_info[index]=[(sentenсe),(positions),(0),[]]  
            self.bbox_info=bbox_info
            self.update()
    
    def draw_point(self,x,y):
        try:
            self.canvas.delete(self.point) 
        except:
            pass
        self.point=self.canvas.create_oval(x-10, y-10, x, y, outline="#2541f4",width=5)
        self.update()
    
    def quit(self):
        self.finish_time=time.time()
        self.read_time=round(self.finish_time-self.start_time)
        self.get_output(save=True)
        messagebox.showinfo('File was saved', 'File was saved/n You read {} sec'.format(self.read_time))
        self.destroy()
        
    def questions(self):
        self.finish_time=time.time()
        self.read_time=round(self.finish_time-self.start_time)
        self.get_output(save=False)
        messagebox.showinfo('Questions', 'Start questions')
        self.destroy()
        self=QuestionScreen(self.text_name,self.output,self.user_name)
        self.mainloop()

        
    def get_bbox(self,x,y):
        if self.eye_tracker==True:
            x = (x*self.width)
            y = (y*self.height) 
        if self.points==True:
            self.draw_point(x,y)
        for key,value in self.bbox_info.items():
            positions=value[1]
            for position in positions:
                x_left=position[0]
                x_right=position[1]
                y_up=position[2]
                y_down=position[3]
                if x_left<=x<=x_right and y_up<=y<=y_down:
                    index=key
                    sentenсe=value[0]
                    positions=value[1]
                    fixations=value[2]+1
                    if self.previous_fixation!=index:
                        self.fixation_number+=1
                    self.previous_fixation=index
                    order=value[3]
                    order.append(self.fixation_number)
                    self.bbox_info[index]=[(sentenсe),(positions),(fixations),order]
                    if self.verbose==True:
                        print('Number sentence:{}, Sentence:{}, Order sentence:{}'.format(index,sentenсe,self.fixation_number))
                    self.update()    
                    break
                        

    def get_output(self,save): # create dataframe from bbox_info
        self.output=pd.DataFrame([(a,b[0],b[2],b[3]) for a,b in self.bbox_info.items()],columns=['index','sentenсe','count_fixation','fixation_order'])
        self.output['count_words']=self.output['sentenсe'].apply(lambda x:len(x.split(' ')))
        self.output['count_fixation_normalized']=self.output['count_fixation']/self.output['count_words']
        self.output['user_name']=self.user_name
        self.output['text']=self.text_name
        self.output['fixation_order']=self.output['fixation_order'].apply(lambda x:list(set(x))) 
        self.output['Age']=self.user_age
        self.output['Gender']=self.user_gender
        self.output['Time']=self.read_time
        if save==True:
            self.output.to_csv('results/fixations_{}_{}.csv'.format(self.user_name,self.text_name),index=False)    
            display(self.output)

class QuestionScreen(Tk):
    def __init__(self,text_name,user_df,user_name):
        super().__init__() 
        self.configure(background='white')
        self.logo = ImageTk.PhotoImage(Image.open("logo.png"))
        self.draw_logo = Label(self, image=self.logo)
        self.draw_logo.place(relx=0.7, rely=0.1)
        
        self.attributes('-fullscreen', True)
        self.text_name=text_name
        questions=np.load("questions/questions.npy",allow_pickle=True).item()
        self.questions=(i for i in questions[self.text_name])
        self.first_question=True
        self.correct_answers=[]
        self.user_df=user_df
        self.user_name=user_name
        self.start()
        
    
    def start(self):
        if self.first_question==False:
            self.user_answer=self.r_var.get()
            if self.user_answer==self.right_question:
                self.correct_answers.append(1)
            else:
                self.correct_answers.append(0)        
        self.first_question=False
        try:
            all_question=next(self.questions)
        except:
            for number_question,accuracy in enumerate(self.correct_answers,1):
                self.user_df['Question {}'.format(number_question)]=accuracy
            self.user_df.to_csv('results/fixations_{}_{}.csv'.format(self.user_name,self.text_name),index=False)    
            display(self.user_df) 
            messagebox.showinfo('Finished', 'You finished')
            self.destroy()
        
        self.question=all_question[0]
        self.answ_1=all_question[1]
        self.answ_2=all_question[2]
        self.answ_3=all_question[3]
        self.answ_4=all_question[4]
        self.right_question=all_question[5]
        
        self.lbl_name = Label(self, text="{}".format(self.question),font=("helvetica Bold", 20),bg='white')
        self.lbl_name.place(relx=0.1, rely=0.25) 
        
        self.r_var = StringVar()
        self.r_var.set(0)
        
        self.rad1 = Radiobutton(self, text=self.answ_1, value=self.answ_1,variable=self.r_var,font=("helvetica Bold", 20),bg='white')  
        self.rad2 = Radiobutton(self, text=self.answ_2, value=self.answ_2,variable=self.r_var,font=("helvetica Bold", 20),bg='white')  
        self.rad3 = Radiobutton(self, text=self.answ_3, value=self.answ_3,variable=self.r_var,font=("helvetica Bold", 20),bg='white')
        self.rad4 = Radiobutton(self, text=self.answ_4, value=self.answ_4,variable=self.r_var,font=("helvetica Bold", 20),bg='white')
        self.rad1.place(relx=0.1, rely=0.4)
        self.rad2.place(relx=0.1, rely=0.5) 
        self.rad3.place(relx=0.1, rely=0.6)
        self.rad4.place(relx=0.1, rely=0.7)

        self.btn_exit = Button(self, text="SUBMIT", command=self.start,font=("helvetica Bold", 20))  
        self.btn_exit.place(relx=0.1, rely=0.8)
        
        self.btn_exit = Button(self, text="EXIT", command=self.destroy,font=("helvetica Bold", 20))  
        self.btn_exit.place(relx=0.8, rely=0.8)