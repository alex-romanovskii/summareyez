# summareyez
This is my python code for my eye tracker thesis
The program takes coordinates on display and connect them with text sentences
In my project, I use data from the eye tracker, it is possible to use the coordinates of the mouse cursor and others

For demonstration, run main.py

## Describtion
**Home screen** 
for user authorization. Texts available from folder named "texts"
![Screenshot](description/first_screen.png)
"I want to see gaze point" - takes x,y coordinates, and then draws a point on the screen

**Text screen**
While the screen is active, the weight of each sentence increases depending on the coordinates
![Screenshot](description/text_screen.png)

**Question screen**
![Screenshot](description/question_screen.png)

**Output**
This is csv file in folder "results" with following features:
- index - sentence number
- sentenсe
- count_fixation - the number of coordinates received by each sentence
- fixation_order 	- order of changing sentences
- count_words 
- count_fixation_normalized - count_fixation relative to word count
- user_name
- text
- Age
- Gender
- Time - reading time all text
- Question... - 0 if wrong answer else 1
![Screenshot](description/output.PNG)
