import csv
import tkinter
from tkinter import messagebox
from tkinter import ttk
import random
import string
import nltk
#nltk.download('words')
from nltk.corpus import words



class WordGame:
    def __init__(self,window):

        self.frame = tkinter.Frame(window)
        self.frame.pack()

        self.label = tkinter.Label(self.frame, text="Word Game",font = ('Calibri', 18, 'bold'))
        self.label.grid(row=0, column=0)

        self.ruleFrame = tkinter.LabelFrame(self.frame,text="Rules:",font=('Calibri', 12, 'bold'))
        self.ruleFrame.grid(row=1, column=0)

        self.rulesText = tkinter.Text(self.ruleFrame,width=80,height=9, font=('Calibri', 12))
        self.rulesText.insert('1.0', "1. This game will generate a random word"
                                "\n2. You need to generate a word using the last letter/character of the game given word"
                                "\n3. In return the game will generate a word using the last letter/character of the word given by you"
                                "\n4. Then the games continues till 10/20 words as opted by you at the beginning of the game."
                                "\n5. You need to select the word length ( 3-letter / 4-letter / 5-letter / Random letter)"
                                "\n6. You need to spell the word right"
                                "\n7. For each correct answer, you will be given +5 points. "
                                "\n8. For each wrong answer, your score will be reduced by -2 points. ")
        self.rulesText.config(state='disabled')
        self.rulesText.grid(row=1, column=0)
        self.startButton = tkinter.Button(self.frame, text="Start",font=('Calibri', 12, 'bold'), command=self.gameStart)
        self.startButton.grid(row=2, column=0)
        self.radioButtonLetter = {"4-Letter": 4, "5-Letter": 5, "random": 0}
        self.radioLevelValue = tkinter.StringVar()
        self.radioButtonWordLimit = {"10": 10, "20": 20, "30": 30}
        self.radioWordValue = tkinter.StringVar()
        self.displayedWords=set([])
        self.threeLetter = {letter: [] for letter in string.ascii_uppercase}
        self.fourLetter = {letter: [] for letter in string.ascii_uppercase}
        self.fiveLetter = {letter: [] for letter in string.ascii_uppercase}
        self.randomLetter = {letter: [] for letter in string.ascii_uppercase}
        self.engWords = set(words.words())
        self.score=0
        self.wordCount=0
        self.name=""
        self.age=0
        self.wordCountSelected=0
        self.wordLength=0


    def createWordListDirectly(self):
        print("Inside createWordList directly function")
        for word in self.engWords:
            if len(word)==3:
                self.threeLetter[word[0].upper()].append(word.title())
            elif len(word)==4:
                self.fourLetter[word[0].upper()].append(word.title())
            elif len(word)==5:
                self.fiveLetter[word[0].upper()].append(word.title())
            self.randomLetter[word[0].upper()].append(word.title())


    def categorizeData(self):
        nameAgeScore=[]
        with open('ScoreSheet.csv','r') as fileObject:
            reader=csv.reader(fileObject)
            for data in reader:
                name,age,score,wordCount=data
                nameAgeScore.append((name,int(age),int(score),int(wordCount)))
        print("List of score data: ",nameAgeScore)
        sorted_nameAgeScore= sorted(nameAgeScore, key=lambda x:(x[3],x[2]), reverse=True)
        print("List of score sorted: ", sorted_nameAgeScore)
        refined_sorted_list=[]
        rank=0
        for sublist in sorted_nameAgeScore:
            if sublist[3] == self.wordCountSelected:
                rank+=1
                refined_sorted_list.append((rank,sublist[0],sublist[2]))
        print("Refined List: ",refined_sorted_list)
        return refined_sorted_list[:5]

    def graphDisplay(self):
        with open('ScoreSheet.csv','a') as fileObject:
            fileObject.write(self.name+","+str(self.age)+","+str(self.score)+","+str(self.wordCountSelected)+"\n")
        print("Saved data to file.")
        for frames in self.frame.winfo_children():
            frames.destroy()

        homeFrame=tkinter.Frame(self.frame)
        homeFrame.grid(row=0,column=0)
        homeButton = tkinter.Button(homeFrame, text="Home", command=self.gameStart,font=('Calibri', 12, 'bold'))
        homeButton.grid(row=0, column=0)

        scoreFrame=tkinter.Frame(self.frame)
        scoreFrame.grid(row=1,column=0)
        nameLabel=tkinter.Label(scoreFrame,text="Name: ",font=('Calibri', 12, 'bold'))
        nameLabel.grid(row=0,column=0)
        nameDisplay=tkinter.Label(scoreFrame,text=self.name,font=('Calibri', 12, 'bold'))
        nameDisplay.grid(row=0,column=1)
        ageLabel=tkinter.Label(scoreFrame,text="Age: ",font=('Calibri', 12, 'bold'))
        ageLabel.grid(row=1,column=0)
        ageDisplay=tkinter.Label(scoreFrame,text=self.age,font=('Calibri', 12, 'bold'))
        ageDisplay.grid(row=1,column=1)
        scoreLabel=tkinter.Label(scoreFrame,text="Your Final Score: ",font=('Calibri', 12, 'bold'))
        scoreLabel.grid(row=2,column=0)
        scoreDisplay=tkinter.Label(scoreFrame,text=self.score,font=('Calibri', 12, 'bold'))
        scoreDisplay.grid(row=2,column=1)

        graphData = self.categorizeData()
        """
        ViewFrame=tkinter.LabelFrame(self.frame,text="Top 5 scorers: ")
        ViewFrame.grid(row=2,column=0)
        header=['Rank','Name','Score']
        column=0
        for data in header:
            headerLabel = tkinter.Label(ViewFrame, text=data)
            headerLabel.grid(row=0, column=column)
            column += 1
        for row in range(len(graphData)):
            for column in range(len(graphData[row])):
                dataLabel=tkinter.Label(ViewFrame,text=graphData[row][column])
                dataLabel.grid(row=row+1,column=column)
        """
        tableFrame = tkinter.LabelFrame(self.frame, text="Top 5 scorers: ",font=('Calibri', 12, 'bold'))
        tableFrame.grid(row=2, column=0)

        tableView=ttk.Treeview(tableFrame,columns=("Rank","Name","Score"),show='headings')
        tableView.heading("Rank",text="Rank")
        tableView.heading("Name", text="Name")
        #tableView.heading("Age", text="Age")
        tableView.heading("Score", text="Score")
        for data in graphData:
                tableView.insert("","end",values=data)
        tableView.grid(row=0,column=0)

    def fetchAppWord(self,userWordPassed):
        if userWordPassed=="firstTime":
            userWordPassed= random.choice(string.ascii_uppercase)
        else:
            userWordPassed= userWordPassed
        word=""
        wordLength = self.radioLevelValue.get()
        if wordLength=='3':
            if self.threeLetter[userWordPassed[-1].upper()]:  # checking if the list is empty of not.
                print("List not empty")
                temp=[]
                for value in self.threeLetter[userWordPassed[-1].upper()]:
                    if value not in self.displayedWords:
                        temp.append(value)
                word=random.choice(temp)
            else:
                print("List empty")
        elif wordLength=='4':
            if self.fourLetter[userWordPassed[-1].upper()]:  # checking if the list is empty of not.
                print("List not empty")
                temp=[]
                for value in self.fourLetter[userWordPassed[-1].upper()]:
                    if value not in self.displayedWords:
                        temp.append(value)
                word=random.choice(temp)
            else:
                print("List empty")
        elif wordLength=='5':
            if self.fiveLetter[userWordPassed[-1].upper()]:  # checking if the list is empty of not.
                print("List not empty")
                temp=[]
                for value in self.fiveLetter[userWordPassed[-1].upper()]:
                    if value not in self.displayedWords:
                        temp.append(value)
                word=random.choice(temp)
            else:
                print("List empty")
        else:
            if self.randomLetter[userWordPassed[-1].upper()]:  # checking if the list is empty of not.
                print("List not empty")
                temp=[]
                for value in self.randomLetter[userWordPassed[-1].upper()]:
                    if value not in self.displayedWords:
                        temp.append(value)
                word=random.choice(temp)
            else:
                print("List empty")
        self.displayedWords.add(word.title())
        return word

    def wordSubmit(self,userWordPassed,appFetchedWord,appWordBoxVariable,appWordBoxObject,userWordBoxEntryObject,scoreVar,scoreObject,wordCountIntVar,countObject):
        print("User typed word: ",userWordPassed)
        if userWordPassed.isalpha():
            if len(userWordPassed)==int(self.radioLevelValue.get()) or int(self.radioLevelValue.get())==0:
                print("word fetched by app:", appFetchedWord)
                if userWordPassed[0].upper()==appFetchedWord[-1].upper():
                    if userWordPassed.lower() in self.engWords:
                        print("Words used: ",self.displayedWords)
                        if userWordPassed.title() not in self.displayedWords:
                            self.score += 5
                            if self.wordCount > 1:
                                
                                self.wordCount-=1
                                #print("WordCount: ",self.wordCount)
                                userWordBoxEntryObject.config(state='disabled')
                                #print("inside main part")
                                self.displayedWords.add(userWordPassed.title())
                                newAppWord=self.fetchAppWord(userWordPassed)
                                #print("New Word: ",newAppWord)
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
                            self.score-=2
                            scoreVar.set(self.score)
                            scoreObject.insert(0, scoreVar)
                    else:
                        tkinter.messagebox.showerror(title="Error!!!", message="The given word is not a proper english word.")
                        self.score-=2
                        scoreVar.set(self.score)
                        scoreObject.insert(0, scoreVar)
                else:
                    tkinter.messagebox.showerror(title="Error!!!", message="The word has to start with the letter/char "+appFetchedWord[-1].upper())
                    self.score -= 2
                    scoreVar.set(self.score)
                    scoreObject.insert(0, scoreVar)
            else:
                tkinter.messagebox.showerror(title="Error!!",message="Error!!! Please enter "+self.radioLevelValue.get()+" letter word.")
                self.score -= 2
                scoreVar.set(self.score)
                scoreObject.insert(0, scoreVar)
        else:
            tkinter.messagebox.showerror(title="Error!!",message="Error!!! Invalid input. You can enter only alphabets.")


    def gamePlay(self,nameSent,ageSent):
        print("Name: ",nameSent)
        print("Age: ",ageSent)
        print("Level: "+self.radioLevelValue.get()+":")
        print("Word Count: "+self.radioWordValue.get()+":")
        level = self.radioLevelValue.get()
        wordCount = self.radioWordValue.get()
        self.displayedWords.clear()
        self.score=0
        if nameSent != "" and nameSent != " " and ageSent!= "" and ageSent!= " " and level != "level" and wordCount!="wordCount":
            if nameSent.isalpha():
                try:
                    if 3 < int(ageSent) <= 110:
                        self.createWordListDirectly()
                        self.name=nameSent.title()
                        self.age=int(ageSent)
                        self.wordCountSelected=int(wordCount)
                        self.wordLength=int(level)
                        for frames in self.frame.winfo_children():
                           frames.destroy()
                        self.wordCount=int(wordCount)
                        homeFrame=tkinter.Frame(self.frame)
                        homeFrame.grid(row=0,column=0)
                        stopButton = tkinter.Button(homeFrame, text="Home",font=('Calibri', 12, 'bold'), command=self.gameStart)
                        stopButton.grid(row=0, column=0)
                        if self.radioLevelValue.get() == '0':
                            length = 'Enter a word of any length'
                        else:
                            length = 'Enter ' + self.radioLevelValue.get() + '-letter word'
                        wordLengthDisplay = tkinter.Label(homeFrame, text=length, font=('Calibri', 12, 'bold'))
                        wordLengthDisplay.grid(row=1, column=0)

                        gameFrame=tkinter.Frame(self.frame)
                        gameFrame.grid(row=1,column=0)

                        scoreLabel=tkinter.Label(gameFrame,text="Score: ",font=('Calibri', 12, 'bold'))
                        scoreLabel.grid(row=1,column=0)
                        scoreResult = tkinter.IntVar()
                        scoreResult.set(0)
                        scoreEntry=tkinter.Entry(gameFrame,textvariable=scoreResult,font=('Calibri', 12, 'bold'),state='disabled',width=5)
                        scoreEntry.grid(row=1,column=1)

                        appWordLabel=tkinter.Label(gameFrame,text="The word is: ",font=('Calibri', 12, 'bold'))
                        appWordLabel.grid(row=2,column=0)
                        appWord = tkinter.StringVar()
                        wordShown = self.fetchAppWord("firstTime")
                        appWord.set(wordShown)
                        appWordEntry=tkinter.Entry(gameFrame,textvariable=appWord,font=('Calibri', 12, 'bold'),state='disabled')
                        appWordEntry.grid(row=2,column=1)
                        userWordLabel=tkinter.Label(gameFrame,text="Enter your word: ",font=('Calibri', 12, 'bold'))
                        userWordLabel.grid(row=3,column=0)
                        userWordEntry=tkinter.Entry(gameFrame)
                        userWordEntry.grid(row=3,column=1)
                        showWordCountLabel=tkinter.Label(gameFrame,text="Words Left: ",font=('Calibri', 12, 'bold'))
                        showWordCountLabel.grid(row=4,column=0)
                        wordCountLeft=tkinter.IntVar()
                        wordCountLeft.set(int(wordCount))
                        showWordCountValue=tkinter.Entry(gameFrame,textvariable=wordCountLeft,font=('Calibri', 12, 'bold'),state='disabled',width=5)
                        showWordCountValue.grid(row=4,column=1)
                        submitFrame=tkinter.Frame(self.frame)
                        submitFrame.grid(row=2,column=0)
                        userSubmitButton = tkinter.Button(submitFrame, text="Submit", font=('Calibri', 12, 'bold'),
                                                          command=lambda: self.wordSubmit(userWordEntry.get(),
                                                                                          appWordEntry.get(), appWord,
                                                                                          appWordEntry, userWordEntry,
                                                                                          scoreResult, scoreEntry,
                                                                                          wordCountLeft,
                                                                                          showWordCountValue))
                        userSubmitButton.grid(row=0, column=0)

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
        nameAgeFrame = tkinter.Frame(self.frame)
        nameAgeFrame.grid(row=0, column=0)
        nameLabel=tkinter.Label(nameAgeFrame,text="Username: ",font=('Calibri', 12, 'bold'))
        nameLabel.grid(row=0,column=0)
        nameData=tkinter.Entry(nameAgeFrame)
        nameData.grid(row=0,column=1)
        ageLabel=tkinter.Label(nameAgeFrame,text="Age: ",font=('Calibri', 12, 'bold'))
        ageLabel.grid(row=0,column=2)
        ageData=tkinter.Entry(nameAgeFrame,width=10)
        ageData.grid(row=0,column=3)
        wordLengthFrame = tkinter.Frame(self.frame)
        wordLengthFrame.grid(row=1, column=0)
        levelLabel=tkinter.Label(wordLengthFrame,text="Pick your word length: ",font=('Calibri', 12, 'bold'))
        levelLabel.grid(row=0,column=0)

        self.radioLevelValue.set("level")
        row=1
        for name,value in self.radioButtonLetter.items():
            rb_object=tkinter.Radiobutton(wordLengthFrame,text=name,variable=self.radioLevelValue,value=value)
            rb_object.grid(row=row,column=0)
            row += 1
        wordCountFrame = tkinter.Frame(self.frame)
        wordCountFrame.grid(row=2, column=0)
        wordLimitLabel=tkinter.Label(wordCountFrame, text="How many words you like to try? ",font=('Calibri', 12, 'bold'))
        wordRow = 0
        wordLimitLabel.grid(row=wordRow,column=0)
        self.radioWordValue.set("wordCount")
        for name,value in self.radioButtonWordLimit.items():
            wordRow+=1
            tkinter.Radiobutton(wordCountFrame, text=name, variable=self.radioWordValue, value=value).grid(row=wordRow, column=0)
        playButton=tkinter.Button(self.frame,text="Play",font=('Calibri', 12, 'bold'),command= lambda : self.gamePlay(nameData.get(),ageData.get()))
        playButton.grid(row=3,column=0)


window=tkinter.Tk()

window_width = 650
window_height = 270
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
position_right = int(screen_width/2 - window_width/2)
position_down = int(screen_height/2 - window_height/2)
window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

window.title("Word Game")
game=WordGame(window)
window.mainloop()
