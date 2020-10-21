import tkinter as tk
from tkinter import messagebox
import crossword
gameInfo = {}

class resourceApp( tk.Tk ):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame( self )
        container.pack()
        self.canvas = tk.Canvas(container, width=500, height=500)
        scroll = tk.Scrollbar(container, orient = 'vertical', command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = scroll.set)
        scrollable_frame = tk.Frame(self.canvas)
        scrollable_frame.bind("<Configure>", lambda e:self.canvas.configure(scrollregion = self.canvas.bbox("all")))
        self.canvas.create_window((250,250), window = scrollable_frame, anchor = 'center')

        container.pack()
        self.canvas.pack()
        scroll.pack(side = "right", fill ="y")

        self.parent = scrollable_frame
        # look into collapsing frames

        self.show_frame("InputCrosswordDetailsPage")

    def show_frame(self, page_name):

        for F in [Crossword, InputCrosswordDetailsPage]:
            if F.__name__ == page_name:
                frame = F(parent=self.parent, controller = self)
                frame.grid(row = 0, column = 0, sticky = "nsew")
                frame.tkraise()


class StartPage( tk.Frame ):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class InputCrosswordDetailsPage( tk.Frame ):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.row = 0
        self.column = 0

        labeltitle = tk.Label(self, text = 'Crossword Generator')
        labeltitle.pack()
        labeldesc = tk.Label(self, text = 'Enter a minimum of 3 words and answers')
        labeldesc.pack()


        self.addClue = tk.Frame(self, name = "getInfo")
        self.addClue.pack()

        button1 = tk.Button(self, text='+', command=self.generateInput)
        button1.pack()
        button2 = tk.Button(self, text='-')
        button2.pack()

        submit = tk.Button(self, text = 'Submit', command = self.submit)
        submit.pack()
        self.generateInput()
        self.generateInput()
        self.generateInput()


    def generateInput(self):
        if self.row < 10:
            wordlbl = tk.Label(self.addClue, text = 'Word: ')
            cluelbl = tk.Label(self.addClue, text='Clue: ')
            word = tk.Entry(self.addClue, name = "word_"+str(self.row))
            clue = tk.Text(self.addClue,width = '20', height = '3', name = "clue_"+str(self.row))
            wordlbl.grid(row = self.row, column = self.column)
            word.grid( row = self.row, column = self.column+1)
            cluelbl.grid( row = self.row, column = self.column+2)
            clue.grid( row=self.row, column=self.column+3)
            self.incrementRow()
    def incrementRow(self):
        self.row += 1
    def submit(self):
        children = self.winfo_children()
        info = []
        for child in children:
            if isinstance( child, tk.Frame ):
                info = child
        try:
            for child in info.winfo_children():
                if isinstance( child, tk.Entry ):
                    index = str(child).split('_')[1]

                    for text in info.winfo_children():
                        if 'clue' in str(text) and index in str(text):

                            key = child.get().strip()
                            value = text.get("1.0", 'end').strip()

                            if len(key) < 0 or len(value) <0:
                                raise Exception('missing values')

                            gameInfo[key] = value
        #     trim each word
        except:
            messagebox.showinfo("Error", "Please ensure that you have filled every box ")
            return

        crossword.words = list(gameInfo.keys())
        crossword.createCrossword()
        crossword.transformGrid()
        app.show_frame("Crossword")


class Crossword(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        grid = crossword.grid

        boxSize = int(60/len(grid))

        finalRowIndex = len(grid)
        finalColIndex = len(grid[0])
        crosswordFrame = tk.Frame( self )
        crosswordFrame.pack()
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                txt = grid[row][col]
                forecolor = ''
                backcolor = ''
                if txt.isnumeric() == True:
                    forecolor = 'black'
                    backcolor = 'white'
                elif txt in '_*&$':
                    forecolor = 'black'
                    backcolor = forecolor
                else:
                    forecolor = 'white'
                    backcolor = forecolor
                l = tk.Label(crosswordFrame, text=txt, borderwidth=2, relief="groove", width=boxSize, height=int(boxSize/2.5), bg=backcolor,
                             fg=forecolor, anchor='w').grid(row=row,column=col)

        finalRowIndex += 1
        l = tk.Label(self, text = "Down:")
        l.pack()
        # l.grid(row = finalRowIndex, column = finalColIndex, padx=10, pady=10)
        finalRowIndex += 1
        finalColIndex += 1
        for down in crossword.down:
            word = down.word
            index = down.index
            clue = gameInfo[word]

            l = tk.Label(self, text = str(index) + ") " + clue)
            l.pack()
            # l.grid(row = finalRowIndex, column = 0)
            finalRowIndex += 1
            finalColIndex += 1

        l = tk.Label(self, text="Across:")
        l.pack()
        # l.grid(row=finalRowIndex, column=0)
        finalRowIndex += 1
        for across in crossword.across:
            word = across.word
            index = across.index
            clue = gameInfo[word]
            l = tk.Label(self, text= str(index) + ") " + clue)
            l.pack()
            # l.grid(row = finalRowIndex, column = 0)
            finalRowIndex += 1


app = resourceApp()
app.mainloop()
