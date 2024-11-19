import tkinter
from idlelib.autocomplete import FILES
from logging import disable
from tkinter import ttk
from tkinter import messagebox
import random
import string
#import time
#from matplotlib.pyplot import title
import nltk
from matplotlib.pyplot import title
#nltk.download('words')
from nltk.corpus import words



class WordGame:
    def __init__(self,window):
        self.frame = tkinter.Frame(window)
        self.frame.pack()

        self.label = tkinter.Label(self.frame, text="Word Game")
        self.label.grid(row=0, column=0)

        self.ruleFrame = tkinter.LabelFrame(self.frame, text="Rules:")
        self.ruleFrame.grid(row=1, column=0)

        self.rulesText = tkinter.Text(self.ruleFrame, height=12, width=85)
        self.rulesText.insert('1.0', "1. This game will generate a random word"
                                "\n2. You need to generate a word using the last letter/character of the game given word"
                                "\n3. In return the game will generate a word using the last letter/character of the word given by you"
                                "\n4. then the games continues till 10/20 words are given by you. the word count challenge is selected at the beginning by you"
                                "\n5. You need to select the word length ( 3-letter word / 4-letter word / 5-letter word / Random letter word)"
                                "\n6. You need to spell the word right"
                                "\n7. You will be given 30 secs to submit a answer. If not the game will consider you don't have a word"
                                "\n8. For each correct answer, you will be given +5 points. For each wrong answer your score will be detected by 1 point")
        self.rulesText.config(state='disabled')
        self.rulesText.grid(row=1, column=0)

        self.startButton = tkinter.Button(self.frame, text="Start", command=self.gameStart)
        self.startButton.grid(row=2, column=0)

        self.radioButtonLetter = {"3-Letter": 3, "4-Letter": 4, "5-Letter": 5, "random": 0}
        self.radioLevelValue = tkinter.StringVar()
        self.radioButtonWordLimit = {"10": 10, "20": 20, "30": 30}
        self.radioWordValue = tkinter.StringVar()

        self.displayedWords=set([])
        self.userGivenWords=set([])

        self.threeLetter = {letter: [] for letter in string.ascii_uppercase}
        self.fourLetter = {letter: [] for letter in string.ascii_uppercase}
        self.fiveLetter = {letter: [] for letter in string.ascii_uppercase}

        self.score=0
        self.wordCount=0
    def createWordList(self):
        print("Inside createWordList function")
        wordLength = self.radioLevelValue.get()
        if wordLength=='3':
            pass
        elif wordLength == '4':
            with open('4-letterWords.txt', 'r') as fileObject:
                for fileWord in fileObject:
                    self.fourLetter[fileWord[0].upper()].append(fileWord.strip("\n").title())
            print("List: ", self.fourLetter)
        elif wordLength=='5':
            pass
        elif wordLength=='0':
            pass
    def graphDisplay(self):
        for frames in self.frame.winfo_children():
            frames.destroy()

    def fetchAppWord(self,userWordPassed):
        if userWordPassed=="firstTime":
            userWordPassed= random.choice(string.ascii_uppercase)
        else:
            userWordPassed= userWordPassed
        #fourLetter=[]
        word=""
        wordLength = self.radioLevelValue.get()
        wordCount = self.radioWordValue.get()
        #wordList=[]
        #for word in wordList:
        #    with open('4-letterWords.txt','a') as fileObject:
        #    fileObject.write(word+"\n")
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
        if wordLength=='3':
            pass
        elif wordLength=='4':
            if self.fourLetter[userWordPassed[-1].upper()]:  # checking if the list is empty of not.
                print("List not empty")
                print("List:",self.fourLetter)
                temp=[]
                for value in self.fourLetter[userWordPassed[-1].upper()]:
                    if value not in self.displayedWords:
                        temp.append(value)
                #word= random.choice(self.fourLetter[userWordPassed[-1].upper()])
                word=random.choice(temp)
            else:
                print("List empty")
        elif wordLength=='5':
            pass
        else:
            pass
        self.displayedWords.add(word.title())
        return word

    def wordSubmit(self,userWordPassed,appFetchedWord,appWordBoxVariable,appWordBoxObject,userWordBoxEntryObject,scoreVar,scoreObject,wordCountIntVar,countObject):
        """This is where we need to use the new lib to validate the user given word."""
        """This is where we need to pupulate the app displayed word."""
        print("User typed word: ",userWordPassed)
        if userWordPassed.isalpha():
            if len(userWordPassed)==int(self.radioLevelValue.get()):
                print("word fetched by app:", appFetchedWord)
                if userWordPassed[0].upper()==appFetchedWord[-1].upper():
                    engWords = set(words.words())
                    if userWordPassed.lower() in engWords:
                        print("Words used: ",self.displayedWords)
                        if userWordPassed.title() not in self.displayedWords:
                            if self.wordCount > 1:
                                self.score+=5
                                self.wordCount-=1
                                print("WordCount: ",self.wordCount)
                                userWordBoxEntryObject.config(state='disabled')
                                print("inside main part")
                                self.displayedWords.add(userWordPassed.title())
                                newAppWord=self.fetchAppWord(userWordPassed)
                                print("New Word: ",newAppWord)
                                tkinter.messagebox.showinfo(title="Lovely!!", message="Good Job!! The New word is: "+newAppWord)
                                appWordBoxVariable.set(newAppWord)
                                appWordBoxObject.insert(0,appWordBoxVariable)
                                userWordBoxEntryObject.config(state='normal')
                                userWordBoxEntryObject.delete(0,"end")
                                scoreVar.set(self.score)
                                scoreObject.insert(0,scoreVar)
                                wordCountIntVar.set(self.wordCount)
                                countObject.insert(0,wordCountIntVar)
                            else:
                                tkinter.messagebox.showinfo(title="Completed!!",message="You have successfully completed the game!!!")
                                self.graphDisplay()
                        else:
                            tkinter.messagebox.showerror(title="Error!!!",message="Words cannot be repeated.")
                    else:
                        tkinter.messagebox.showerror(title="Error!!!", message="The given word is not a proper english word.")
                else:
                    tkinter.messagebox.showerror(title="Error!!!", message="The word has to start with the letter/char "+appFetchedWord[-1].upper())
            else:
                tkinter.messagebox.showerror(title="Error!!",message="Error!!! Please enter "+self.radioLevelValue.get()+" letter word.")
        else:
            tkinter.messagebox.showerror(title="Error!!",message="Error!!! Invalid input. You can enter only alphabets.")


    def gamePlay(self,nameSent,ageSent):
        print("Name: ",nameSent)
        print("Age: ",ageSent)
        print("Level: "+self.radioLevelValue.get()+":")
        print("Word Count: "+self.radioWordValue.get()+":")
        level = self.radioLevelValue.get()
        wordCount = self.radioWordValue.get()
        if nameSent != "" and nameSent != " " and ageSent!= "" and ageSent!= " " and level != "level" and wordCount!="wordCount":
            if nameSent.isalpha():
                try:
                    ageConverted=int(ageSent)
                    if ageConverted > 3 and ageConverted <= 110:
                        self.createWordList()
                        for frames in self.frame.winfo_children():
                           frames.destroy()
                        self.wordCount=int(wordCount)
                        gameFrame=tkinter.LabelFrame(self.frame)
                        gameFrame.grid(row=0,column=0)
                        stopButton=tkinter.Button(gameFrame,text="Home",command=self.gameStart)
                        stopButton.grid(row=0,column=0)

                        scoreLabel=tkinter.Label(gameFrame,text="Score: ")
                        scoreLabel.grid(row=0,column=1)
                        scoreResult = tkinter.IntVar()
                        scoreResult.set(0)
                        scoreEntry=tkinter.Entry(gameFrame,textvariable=scoreResult,state='disabled')
                        scoreEntry.grid(row=0,column=2)

                        appWordLabel=tkinter.Label(gameFrame,text="The word is: ")
                        appWordLabel.grid(row=1,column=1)
                        appWord = tkinter.StringVar()
                        wordShown = self.fetchAppWord("firstTime")
                        appWord.set(wordShown)
                        appWordEntry=tkinter.Entry(gameFrame,textvariable=appWord,state='disabled')
                        appWordEntry.grid(row=1,column=2)
                        userWordLabel=tkinter.Label(gameFrame,text="Enter your word: ")
                        userWordLabel.grid(row=2,column=1)
                        userWordEntry=tkinter.Entry(gameFrame)
                        userWordEntry.grid(row=2,column=2)
                        userSubmitButton=tkinter.Button(gameFrame,text="Submit",command= lambda : self.wordSubmit(userWordEntry.get(),appWordEntry.get(),appWord,appWordEntry,userWordEntry,scoreResult,scoreEntry,wordCountLeft,showWordCountValue))
                        userSubmitButton.grid(row=2,column=3)
                        showWordCountLabel=tkinter.Label(gameFrame,text="Words Left: ")
                        showWordCountLabel.grid(row=3,column=1)
                        wordCountLeft=tkinter.IntVar()
                        wordCountLeft.set(wordCount)
                        showWordCountValue=tkinter.Entry(gameFrame,textvariable=wordCountLeft,state='disabled')
                        showWordCountValue.grid(row=3,column=2)


                    else:
                        tkinter.messagebox.showwarning(title="Error", message="Error !! Inappropriate Age.")
                except ValueError:
                    tkinter.messagebox.showwarning(title="Error", message="Error !! Inappropriate Age.")
            else:
                tkinter.messagebox.showwarning(title="Error", message="Error !! Name can contain only alphabets.")
        else:
            tkinter.messagebox.showwarning(title="Error",message="Error !! All inputs are mandatory.")
    def gameStart(self):
        for frames in self.frame.winfo_children():
            frames.destroy()
        dataFrame = tkinter.LabelFrame(self.frame)
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

        self.radioLevelValue.set("level")
        row=1
        for name,value in self.radioButtonLetter.items():
            row+=1
            tkinter.Radiobutton(dataFrame,text=name,variable=self.radioLevelValue,value=value).grid(row=row,column=1)
        wordLimitLabel=tkinter.Label(dataFrame, text="Word Limit: ")
        wordRow = row + 1
        wordLimitLabel.grid(row=wordRow,column=0)
        self.radioWordValue.set("wordCount")
        for name,value in self.radioButtonWordLimit.items():
            wordRow+=1
            tkinter.Radiobutton(dataFrame, text=name, variable=self.radioWordValue, value=value).grid(row=wordRow, column=1)
        playButton=tkinter.Button(self.frame,text="Play",command= lambda : self.gamePlay(nameData.get(),ageData.get()))
        playButton.grid(row=1,column=0)


window=tkinter.Tk()
window.title("Word Game")
game=WordGame(window)
window.mainloop()
