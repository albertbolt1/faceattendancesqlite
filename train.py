
import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from keras_facenet import FaceNet
from teja import dictq
from teja import extract_face
import matplotlib.pyplot as plt
import sqlite3
import csv

window = tk.Tk()

window.title("attendance system")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'


window.configure(background='blue')


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

def trackimage():
    embedder = FaceNet()
    b=[]
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        img1=extract_face(frame)
        plt.imshow(frame)
        img1=np.expand_dims(img1,axis=0)
        if(img1.any()):
            emb=embedder.embeddings(img1)
            emb=np.transpose(emb)
            min_dist=100
            for key,value in dictq.items():
                dist=np.linalg.norm(emb-value)
                b.append(dist)
                if dist<min_dist:
                    min_dist=dist
                    identity=key
            print(identity)
            if min_dist < 1.0:
                cv2.putText(frame, "Face : " + identity,(100,100),cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0,255), 2)
                unknown_yes_or_no='no'
            else:
                cv2.putText(frame,'no match',(100,100),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
                unknown_yes_or_no='yes'
            cv2.imshow('face',frame)

            if cv2.waitKey(1) & 0xFF==27:
                break

    cap.release()
    cv2.destroyAllWindows()
    import pyttsx3
    engine = pyttsx3.init()
    if(unknown_yes_or_no=="yes"):
        engine.say("Good morning sorry we couldn't recognise you")
    else:
        str1="good morning "+identity+" your attendance has been recorded"
        engine.say(str1)
        conn = sqlite3.connect('face.db')
        sql = ''' INSERT INTO TEACHERS_ATTENDANCE(NAME,DATE_PRESENT,SESSION)
              VALUES(?,?,?) '''
        from datetime import date
        today1 = date.today()
        values=(identity,str(today1),"morning")
        cur = conn.cursor()
        cur.execute(sql,values)
        conn.commit()

    engine.runAndWait()



message = tk.Label(window, text="attendance system",bg="Green"  ,fg="white"  ,width=30  ,height=3,font=('times', 30, 'italic bold underline')) 

message.place(x=200, y=20)


def exit1():
    exit()

def getattendanceascsv():
    inputValue=textBox.get("1.0","end-1c")
    conn = sqlite3.connect('face.db')
    sql = ''' SELECT * FROM TEACHERS_ATTENDANCE WHERE date_present=? '''
    cur = conn.cursor()
    cur.execute(sql,(inputValue,))
    rows = cur.fetchall()
    name='attendance'+inputValue+'.csv'
    with open(name,'w') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(['id','name','date','session'])
        for row in rows:
            newFileWriter.writerow([row[0],row[1],row[2],row[3]])
            


textBox=tk.Text(window, height=3, width=10)
textBox.place(x=1000, y=500)
buttonCommit=tk.Button(window, height=3, width=30, text="clickheretogetcsv", 
                    command=lambda: getattendanceascsv())
buttonCommit.place(x=750,y=500)
trackImg = tk.Button(window, text="click here to mark attendance and wait till ur name shows up",wraplength=200,justify='left',command=trackimage  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=200, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=500, y=500)
 
window.mainloop()