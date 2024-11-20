import csv
import tkinter
from tkinter import messagebox
import random
import string
import nltk
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
                                "\n4. Then the games continues till 10/20 words as opted by you at the beginning of the game."
                                "\n5. You need to select the word length ( 3-letter word / 4-letter word / 5-letter word / Random letter word)"
                                "\n6. You need to spell the word right"
                                "\n7. For each correct answer, you will be given +5 points. "
                                "\n8. For each wrong answer, your score will be reduced by -1 points. ")
        self.rulesText.config(state='disabled')
        self.rulesText.grid(row=1, column=0)

        self.startButton = tkinter.Button(self.frame, text="Start", command=self.gameStart)
        self.startButton.grid(row=2, column=0)

        self.radioButtonLetter = {"4-Letter": 4, "5-Letter": 5, "random": 0}
        self.radioLevelValue = tkinter.StringVar()
        self.radioButtonWordLimit = {"10": 10, "20": 20, "30": 30}
        self.radioWordValue = tkinter.StringVar()

        self.displayedWords=set([])
        #self.userGivenWords=set([])

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


    def createWordFile(self):
        for word in self.engWords:
            if len(word)==3:
                with open('3-letterWords.txt','a') as fileObject:
                    fileObject.write(word.title()+"\n")
            elif len(word)==4:
                with open('4-letterWords.txt','a') as fileObject:
                    fileObject.write(word.title()+"\n")
            elif len(word)==5:
                with open('5-letterWords.txt','a') as fileObject:
                    fileObject.write(word.title()+"\n")
            with open('randomWords.txt','a') as fileObject:
                fileObject.write(word.title() + "\n")

    def createWordList(self):
        wordLength = self.radioLevelValue.get()
        if wordLength=='3':
            with open('3-letterWords.txt', 'r') as fileObject:
                for fileWord in fileObject:
                    self.threeLetter[fileWord[0].upper()].append(fileWord.strip("\n").title())
        elif wordLength == '4':
            with open('4-letterWords.txt', 'r') as fileObject:
                for fileWord in fileObject:
                    self.fourLetter[fileWord[0].upper()].append(fileWord.strip("\n").title())
        elif wordLength=='5':
            with open('5-letterWords.txt', 'r') as fileObject:
                for fileWord in fileObject:
                    self.fiveLetter[fileWord[0].upper()].append(fileWord.strip("\n").title())
        else:
            with open('randomWords.txt','r') as fileObject:
                for fileWord in fileObject:
                    self.randomLetter[fileWord[0].upper()].append(fileWord.strip("\n").title())

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
        #print("3 Letter: ",self.threeLetter)
        #print("4 Letter: ", self.fourLetter)
        #print("5 Letter: ", self.fiveLetter)
        #print("Random Letter: ", self.randomLetter)


    def categorizeData(self):
        nameAgeScore=[]
        with open('ScoreSheet.csv','r') as fileObject:
            reader=csv.reader(fileObject)
            for data in reader:
                name,age,score,wordCount=data
                nameAgeScore.append((name,int(age),int(score),int(wordCount)))
        print("List of score data: ",nameAgeScore)

        sorted_nameAgeScore= sorted(nameAgeScore, key=lambda x:(x[3],x[2]), reverse=True)
        print("List of score sorted: ", nameAgeScore)
        #return sorted_nameAgeScore[:5]
        return [sublist for sublist in sorted_nameAgeScore if sublist[3] == self.wordCountSelected][:5]

    def graphDisplay(self):

        with open('ScoreSheet.csv','a') as fileObject:
            fileObject.write(self.name+","+str(self.age)+","+str(self.score)+","+str(self.wordCountSelected)+"\n")
        print("Saved data to file.")

        for frames in self.frame.winfo_children():
            frames.destroy()

        scoreFrame=tkinter.LabelFrame(self.frame)
        scoreFrame.grid(row=0,column=0)
        homeButton=tkinter.Button(scoreFrame,text="Home",command=self.gameStart)
        homeButton.grid(row=0,column=0)
        nameLabel=tkinter.Label(scoreFrame,text="Name: ")
        nameLabel.grid(row=1,column=0)
        nameDisplay=tkinter.Label(scoreFrame,text=self.name)
        nameDisplay.grid(row=1,column=1)
        ageLabel=tkinter.Label(scoreFrame,text="Age: ")
        ageLabel.grid(row=2,column=0)
        ageDisplay=tkinter.Label(scoreFrame,text=self.age)
        ageDisplay.grid(row=2,column=1)
        scoreLabel=tkinter.Label(scoreFrame,text="Score: ")
        scoreLabel.grid(row=3,column=0)
        scoreDisplay=tkinter.Label(scoreFrame,text=self.score)
        scoreDisplay.grid(row=3,column=1)
        graphFrame=tkinter.LabelFrame(self.frame,text="Top 5 scorers: ")
        graphFrame.grid(row=1,column=0)
        header=['Rank','Name','Age','Score']
        column=0
        for data in header:
            headerLabel = tkinter.Label(graphFrame, text=data)
            headerLabel.grid(row=0, column=column)
            column += 1
        graphData=self.categorizeData()
        for row in range(len(graphData)):
            dataLabel = tkinter.Label(graphFrame, text=row+1)
            dataLabel.grid(row=row + 1, column=0)
            for column in range(len(graphData[row])):
                dataLabel=tkinter.Label(graphFrame,text=graphData[row][column])
                dataLabel.grid(row=row+1,column=column+1)

        """
        tableView=ttk.Treeview(graphFrame,columns=("Name","Age","Score"),show='headings')
        #tableView.heading("Place",text="Rank")
        tableView.heading("Name", text="Name")
        tableView.heading("Age", text="Age")
        tableView.heading("Score", text="Score")
        for data in graphData[:5]:
                tableView.insert("","end",values=data)
        tableView.pack()
        """
    def fetchAppWord(self,userWordPassed):
        if userWordPassed=="firstTime":
            userWordPassed= random.choice(string.ascii_uppercase)
        else:
            userWordPassed= userWordPassed
        #fourLetter=[]
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
                #word= random.choice(self.fourLetter[userWordPassed[-1].upper()])
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
        """This is where we need to use the new lib to validate the user given word."""
        """This is where we need to populate the app displayed word."""
        print("User typed word: ",userWordPassed)
        if userWordPassed.isalpha():
            if len(userWordPassed)==int(self.radioLevelValue.get()) or int(self.radioLevelValue.get())==0:
                print("word fetched by app:", appFetchedWord)
                if userWordPassed[0].upper()==appFetchedWord[-1].upper():
                    if userWordPassed.lower() in self.engWords:
                        print("Words used: ",self.displayedWords)
                        if userWordPassed.title() not in self.displayedWords:
                            if self.wordCount > 1:
                                self.score+=5
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
                            self.score-=1
                            scoreVar.set(self.score)
                            scoreObject.insert(0, scoreVar)
                    else:
                        tkinter.messagebox.showerror(title="Error!!!", message="The given word is not a proper english word.")
                        self.score-=1
                        scoreVar.set(self.score)
                        scoreObject.insert(0, scoreVar)

                else:
                    tkinter.messagebox.showerror(title="Error!!!", message="The word has to start with the letter/char "+appFetchedWord[-1].upper())
                    self.score -= 1
                    scoreVar.set(self.score)
                    scoreObject.insert(0, scoreVar)
            else:
                tkinter.messagebox.showerror(title="Error!!",message="Error!!! Please enter "+self.radioLevelValue.get()+" letter word.")
                self.score -= 1
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
                        #self.createWordFile()
                        #self.createWordList()
                        self.createWordListDirectly()
                        self.name=nameSent
                        self.age=int(ageSent)
                        self.wordCountSelected=int(wordCount)
                        self.wordLength=int(level)
                        for frames in self.frame.winfo_children():
                           frames.destroy()
                        self.wordCount=int(wordCount)
                        gameFrame=tkinter.LabelFrame(self.frame)
                        gameFrame.grid(row=0,column=0)
                        stopButton=tkinter.Button(gameFrame,text="Home",command=self.gameStart)
                        stopButton.grid(row=0,column=0)
                        if self.radioLevelValue.get()=='0':
                            length='Enter a word of any length'
                        else:
                            length='Enter '+self.radioLevelValue.get()+'-letter word'

                        wordLengthDisplay=tkinter.Label(gameFrame,text=length)
                        wordLengthDisplay.grid(row=0,column=2)
                        scoreLabel=tkinter.Label(gameFrame,text="Score: ")
                        scoreLabel.grid(row=0,column=3)
                        scoreResult = tkinter.IntVar()
                        scoreResult.set(0)
                        scoreEntry=tkinter.Entry(gameFrame,textvariable=scoreResult,state='disabled',width=5)
                        scoreEntry.grid(row=0,column=4)

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
                        wordCountLeft.set(int(wordCount))
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
        levelLabel=tkinter.Label(dataFrame,text="Pick your word length: ")
        levelLabel.grid(row=1,column=0)

        self.radioLevelValue.set("level")
        row=1
        for name,value in self.radioButtonLetter.items():
            row+=1
            tkinter.Radiobutton(dataFrame,text=name,variable=self.radioLevelValue,value=value).grid(row=row,column=1)
        wordLimitLabel=tkinter.Label(dataFrame, text="How many words you like to try? ")
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
