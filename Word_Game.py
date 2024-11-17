import tkinter
from idlelib.autocomplete import FILES
from logging import disable
from tkinter import ttk
from tkinter import messagebox
import random
import string

#import nltk
#from nltk.corpus import words
appDisplayedWords=[]
userGivenWords=[]

def fetchAppWord(userWordPassed):
    if userWordPassed:
        userWordPassed=userWordPassed
    else:
        userWordPassed='Year'
    #fourLetter=[]
    word="Able"
    wordLength = radioLevelValue.get()
    wordCount = radioWordValue.get()
    #wordList=[]
    #for word in wordList:
    #    with open('4-letterWords.txt','a') as fileObject:
    #        fileObject.write(word+"\n")
    """
    1. Need to ensure that this function returns the word as per the user selected level.
    2. gets the wordlength given by user
    3. create a seperate text file for each given word length. 
        - each file will contain list of word of given length and max count in app. 
        - For each starting letter, create the list and append it to the file of respective count.
        - if there are no word in file that is used, then get a new word from internet.
        - better if we create list for a-z starting word in start, so that we just need to sort the list everytime. Time can save.
    4. create a global list for app word and user word. return the word not in both list.
    5. return the word based on the last letter of the user given word.
     """
    threeLetter = { letter :[] for letter in string.ascii_uppercase}
    fourLetter= { letter :[] for letter in string.ascii_uppercase}
    fiveLetter={ letter :[] for letter in string.ascii_uppercase}


    if wordLength=='4':
        with open('4-letterWords.txt','r') as fileObject:
            for fileWord in fileObject:
                fourLetter[fileWord[0].upper()].append(fileWord.strip("\n").title())
        print("List: ",fourLetter)
        if fourLetter: # checking if the list is empty of not.
            print("List not empty")
            return random.choice(fourLetter[userWordPassed[-1].upper()])
        else:
            print("List empty")
            return word
    elif wordLength=='3':
        pass
    elif wordLength=='5':
        pass
    else:
        pass

def wordSubmit(userWordPassed):
    """This is where we need to use the new lib to validate the user given word."""
    """This is where we need to pupulate the app displayed word."""
    print("User typed word: ",userWordPassed)
    word=fetchAppWord(userWordPassed)
    appDisplayedWords.append(word)

    print("word fetched by app:",word)
    pass

def gamePlay(nameSent,ageSent):
    print("Name: ",nameSent)
    print("Age: ",ageSent)
    print("Level: "+radioLevelValue.get()+":")
    print("Word Count: "+radioWordValue.get()+":")
    level = radioLevelValue.get()
    wordCount = radioWordValue.get()
    if nameSent != "" and nameSent != " " and ageSent!= "" and ageSent!= " " and level != "level" and wordCount!="wordCount":
        if nameSent.isalpha():
            try:
                ageConverted=int(ageSent)
                if ageConverted > 3 and ageConverted <= 110:
                    for frames in frame.winfo_children():
                        frames.destroy()
                    gameFrame=tkinter.LabelFrame(frame)
                    gameFrame.grid(row=0,column=0)
                    stopButton=tkinter.Button(gameFrame,text="Stop")
                    stopButton.grid(row=0,column=0)
                    scoreLabel=tkinter.Label(gameFrame,text="Score: ")
                    scoreLabel.grid(row=0,column=1)
                    scoreResult = tkinter.StringVar()
                    scoreResult.set("0")
                    scoreEntry=tkinter.Entry(gameFrame,textvariable=scoreResult,state='disabled')
                    scoreEntry.grid(row=0,column=2)
                    timerLabel=tkinter.Label(gameFrame,text="Time Left: ")
                    timerLabel.grid(row=0,column=3)
                    timer=tkinter.StringVar()
                    timer.set("00:00")
                    timerValue=tkinter.Entry(gameFrame,textvariable=timer,state='disabled')
                    timerValue.grid(row=0,column=4)
                    appWord = tkinter.StringVar()
                    appWordLabel=tkinter.Label(gameFrame,text="The word is: ")
                    appWordLabel.grid(row=1,column=1)

                    appWord.set("")
                    appWordEntry=tkinter.Entry(gameFrame,textvariable=appWord,state='disabled')
                    appWordEntry.grid(row=1,column=2)
                    userWordLabel=tkinter.Label(gameFrame,text="Enter your word: ")
                    userWordLabel.grid(row=2,column=1)
                    userWordEntry=tkinter.Entry(gameFrame)
                    userWordEntry.grid(row=2,column=2)
                    userSubmitButton=tkinter.Button(gameFrame,text="Submit",command= lambda : wordSubmit(userWordEntry.get()))
                    userSubmitButton.grid(row=2,column=3)
                    showWordCountLabel=tkinter.Label(gameFrame,text="Words Left: ")
                    showWordCountLabel.grid(row=3,column=2)
                    wordCountLeft=tkinter.StringVar()
                    wordCountLeft.set("10")
                    showWordCountValue=tkinter.Entry(gameFrame,textvariable=wordCountLeft,state='disabled')
                    showWordCountValue.grid(row=3,column=3)
                else:
                    tkinter.messagebox.showwarning(title="Error", message="Error !! Inappropriate Age.")
            except ValueError:
                tkinter.messagebox.showwarning(title="Error", message="Error !! Inappropriate Age.")
        else:
            tkinter.messagebox.showwarning(title="Error", message="Error !! Name can contain only alphabets.")
    else:
        tkinter.messagebox.showwarning(title="Error",message="Error !! All inputs are mandatory.")
def gameStart():
    for frames in frame.winfo_children():
        frames.destroy()
    dataFrame = tkinter.LabelFrame(frame)
    dataFrame.grid(row=0, column=0)
    nameLabel=tkinter.Label(dataFrame,text="Firstname: ")
    nameLabel.grid(row=0,column=0)
    nameData=tkinter.Entry(dataFrame)
    nameData.grid(row=0,column=1)
    ageLabel=tkinter.Label(dataFrame,text="Age: ")
    ageLabel.grid(row=0,column=2)
    ageData=tkinter.Entry(dataFrame)
    ageData.grid(row=0,column=3)
    levelLabel=tkinter.Label(dataFrame,text="Difficulty Level: ")
    levelLabel.grid(row=1,column=0)

    radioLevelValue.set("level")
    row=1
    for name,value in radioButtonLetter.items():
        row+=1
        tkinter.Radiobutton(dataFrame,text=name,variable=radioLevelValue,value=value).grid(row=row,column=1)
    wordLimitLabel=tkinter.Label(dataFrame, text="Word Limit: ")
    wordRow = row + 1
    wordLimitLabel.grid(row=wordRow,column=0)
    radioWordValue.set("wordCount")
    for name,value in radioButtonWordLimit.items():
        wordRow+=1
        tkinter.Radiobutton(dataFrame, text=name, variable=radioWordValue, value=value).grid(row=wordRow, column=1)
    playButton=tkinter.Button(frame,text="Play",command= lambda : gamePlay(nameData.get(),ageData.get()))
    playButton.grid(row=1,column=0)

window=tkinter.Tk()
window.title("Word Game")
frame=tkinter.Frame(window)
frame.pack()

label=tkinter.Label(frame,text="Word Game")
label.grid(row=0,column=0)

#gameFrame = tkinter.LabelFrame(frame)
#gameFrame.grid(row=0, column=0)

ruleFrame=tkinter.LabelFrame(frame,text="Rules:")
ruleFrame.grid(row=1,column=0)

rulesText=tkinter.Text(ruleFrame, height=12, width=85)
rulesText.insert('1.0',"1. This game will generate a random word"
                       "\n2. You need to generate a word using the last letter/character of the game given word"
                       "\n3. In return the game will generate a word using the last letter/character of the word given by you"
                       "\n4. then the games continues till 10/20 words are given by you. the word count challenge is selected at the beginning by you"
                       "\n5. You need to select the word length ( 3-letter word / 4-letter word / 5-letter word / Random letter word)"
                       "\n6. You need to spell the word right"
                       "\n7. You will be given 30 secs to submit a answer. If not the game will consider you don't have a word"
                       "\n8. For each correct answer, you will be given +5 points. For each wrong answer your score will be detected by 1 point")
rulesText.config(state='disabled')
rulesText.grid(row=1,column=0)

startButton=tkinter.Button(frame,text="Start",command=gameStart)
startButton.grid(row=2,column=0)

radioButtonLetter={"3-Letter":3,"4-Letter":4,"5-Letter":5,"random":0}
radioLevelValue = tkinter.StringVar()
radioButtonWordLimit = {"10": 10, "20": 20, "30": 30}
radioWordValue = tkinter.StringVar()

window.mainloop()
