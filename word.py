class Word:
    def __init__(self, word, index, position ):
        self.word = word
        self.index = index
        self.position = position

    def getRowPos(self):
        return int(self.position.split('.')[0])

    def getColPos(self):
        return int(self.position.split('.')[1])