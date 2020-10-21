import fnmatch
import word as crosswordAnswer
words = [ 'atlantic', 'pacific', 'ocean', 'global', 'asia', 'europe' ]
grid = []
gridIndexs = []

# sort
def sortArray( array ):
    sorted = []
    length = 0
    for i in range( len ( array ) ):
        length = len( sorted )
        if i == 0:
            sorted.append( array[i] )
        elif len( array[i] ) >= len( sorted[ 0 ] ):
            sorted.insert( 0, array[i])

        else:
            for j in range( length ):
                if j == length-1:
                    sorted.append(  array[i] )
                elif len( array[i] ) >= len( sorted[j] ):
                    sorted.insert( j, array[i] )
                    break
    return sorted


# grid = createGrid( sorted, [] )
# map to gui
def addWordToGrid( word, grid, gridIndexs ):
    length = len(word)
    if len(grid) == 0:
        grid.append( ['&'] + (['$'] * length) +['&'] )
        grid.append( ['_'] + list(word) + ['_'] )
        grid.append( ['&'] + (['$'] * length) +['&'] )
        for i in range( 0, length ):
            gridIndexs.append("1."+str(i+1))
        return True
    else:
        for i in gridIndexs:
            for j in range(length):
                if isMatch( grid, i, word[j] ):
                    if canVert(grid, i, j, length-j-1, word ):
                        addChar(grid, i, j, length - j-1, word, 'V')
                        return True
                    elif canHori( grid, i, j, length - j -1, word):
                        addChar(grid, i, j, length - j-1, word, 'H')
                        return True
        return False
def incrementGridIndexs( num, dir ):
    for i in range(len(gridIndexs)):
        index = gridIndexs[i].split('.')
        if dir == 'V':
            gridIndexs[i] = str(int(index[0])+num)+ '.'+index[1]
        else:
            gridIndexs[i] = index[0] +'.'+ str(int(index[1]) + num)

def canHori( grid, location, lb, lt, word ):
    loc = getLocations(location)
    okaylb = False
    okaylt = False
    checkChar = ''
    try:
        if loc[1] - lb > 0:
            checkChar = grid[loc[0]][loc[1] - lb -1]
            if checkChar not in ['&', '_', '$', '*']:
                return False
        for i in range(1,lb+1):
            checkChar = grid[loc[0]][loc[1] - i]
            if not(checkChar == "&" or checkChar == "*" or word[i-1] == checkChar):
                return False
        okaylb = True
    except:
        okaylb = True
    try:
        if loc[1] + lt < len(grid):
            checkChar = grid[loc[0]][loc[1] + lt + 1]
            if checkChar not in ['&', '_', '$', '*']:
                return False
        for i in range(1,lt+1):
            checkChar = grid[loc[0]][loc[1] + i]
            if not(checkChar == "&" or checkChar == "*" or word[lb + i - 1] == checkChar):
                return False
        okaylt = True
    except:
        okaylt = True
    return okaylb and okaylt

def fixEnds( location, lb, lt, dir ):
    num = 0
    if dir == 'V':
        grid[location[0] - lb - 1][location[1]] = '_'
        grid[location[0] + lt + 1][location[1]] = '_'
    else:
        grid[location[0]][location[1] - lb - 1] = '_'
        grid[location[0]][location[1] + lt + 1] = '_'


def addChar( grid, location, lb, lt, word, dir ):
    originalLoc = getLocations(location)
    checkSurround(grid, originalLoc, dir)
    while gridIndexs.count(location) < 2:
        gridIndexs.append(location)
    for i in range(1,lb+1):
        character = word[lb-i]
        add = -i
        changeChar( grid, location, add, character, dir )
    for i in range(1, lt+1):
        character = word[lb+i]
        old = grid[originalLoc[0]][originalLoc[1]]
        if lb > 0 and old != word[lb]:
            if dir == 'V':
                originalLoc[0] = lb + 1
            else:
                originalLoc[1] = lb + 1
        changeChar(grid, str(originalLoc[0]) + '.' + str(originalLoc[1]), i, character, dir )

    fixEnds(originalLoc, lb, lt, dir)

def symbolDecision( character, direc ):
    if character not in '$_*&':
        return character
    if direc == 'H':
        if character == '&' or character == '$':
            return '$'
        else:
            return '_'
    else:
        if character == '*' or character == '&':
            return '*'
        else:
            return '_'

def addToGrid(directionCheck, num, grid):
    if directionCheck:
        if num == 1:
            addCol(grid, 'right')
        else:
            addCol(grid, 'left')
    else:
        if num == 1:
            addRow(grid, 'bottom')
        else:
            addRow(grid, 'top')

def checkSurround(grid,loc, dir):
    directionCheck = False
    num = 0
    for i in [-1,1]:
        try:
            directionCheck = False
            if loc[0] == 0 and i == -1:
                raise Exception("Negative Number")
            grid[ loc[0] + i][loc[1]] = symbolDecision( grid[ loc[0]+i][loc[1]], dir )
        except:
            addToGrid( directionCheck, i, grid )
            if loc[0] == 0 and i == -1:
                grid[loc[0]][loc[1]] = '_'
                loc[0] += 1
            else:
                grid[loc[0] + i][loc[1]] = '_'
        try:
            directionCheck = True
            if loc[1] == 0 and i == -1:
                raise Exception("Negative Number")
            grid[loc[0]][loc[1] + i] = symbolDecision(grid[loc[0]][loc[1]+i], dir)
        except:
            addToGrid(directionCheck, i, grid)
            if loc[1] == 0 and i == -1:
                grid[loc[0]][loc[1]] = '_'
                loc[1] += 1
            else:
                grid[loc[0]][loc[1] + i] = '_'

def changeChar( grid, location, add, char, dir ):
    loc = getLocations(location)
    if dir == 'H':
        loc[1] += add
        if loc[1] < 0:
            loc[1] = 0
    else:
        loc[0] += add
        if loc[0] < 0:
            loc[0] = 0
    grid[ loc[0] ][ loc[1] ] = char
    gridIndexs.append( str(loc[0]) + '.' + str(loc[1]) )
    checkSurround( grid, loc, dir )

def addRow( grid, side ):
    if side == 'top':
        grid.insert(0, ['&'] * len(grid[0]))
        incrementGridIndexs(1,'V')
    else:
        grid.append( ['&'] * len(grid[0]))

def addCol( grid, side ):
    if side == 'left':
        for i in range(len(grid)):
            grid[i] = ['&'] + grid[i]
        incrementGridIndexs(1, 'H')
    else:
        for i in range(len(grid)):
            grid[i] = grid[i] + ['&']


def getLocations( location ):
    row = int(location.split('.')[0])
    column = int(location.split('.')[1])
    return [row, column]

def canVert( grid, location, lb, lt, word ):
    loc = getLocations(location)
    okaylb = False
    okaylt = False
    checkChar = ''
    try:
        # check if there is a character before the supposed first character
        # if character before first is not (& or _) you cannot do it here
        if loc[0] - lb > 0:
            checkChar = grid[loc[0] - lb -1][loc[1]]
            if checkChar not in ['&', '_', '$', '*']:
                return False
        for i in range(1,lb+1):
            checkChar = grid[loc[0] - i][loc[1]]
            if not(checkChar == '$' or checkChar == '&' or word[i - 1] == checkChar):
                return False
        okaylb = True
    except:
        okaylb = True
    try:
        if loc[0] + lt < len(grid):
            checkChar = grid[loc[0] + lt + 1 ][loc[1]]
            if checkChar not in ['&', '_', '$', '*']:
                return False
        for i in range(1,lt+1):
            checkChar = grid[loc[0]+i][loc[1]]
            if not(checkChar == '$' or checkChar == '&' or word[lb + i - 1] == checkChar):
                return False
        okaylt = True
    except:
        okaylt = True
    return okaylb and okaylt


def isMatch( grid, location, character ):
    loc = getLocations(location)
    try:
        if grid[loc[0]][loc[1]] == character:
            return True
        else:
            return False
    except:
        num = 9


def getLetter(loc):
    loc = getLocations(loc)
    return grid[loc[0]][loc[1]]


def posLetter( location1, location2, dir ):
    loc1 = getLocations(location1)
    loc2 = getLocations(location2)
    if loc1[not dir] != loc2[not dir]:
        return -1
    if loc1[dir]+1 == loc2[dir]:
        return 1
    elif loc1[dir]-1 == loc2[dir]:
        return 0
    else:
        return -1

def groupWords( dir ):
    group = []
    index = 1
    crossover = []
    for i in set(gridIndexs):
        if gridIndexs.count(i) ==2 and i not in crossover:
            crossover.append(i)
    words = []
    for i in set(crossover):
        plane = []
        num = -1
        pos = i
        while pos != '':
            plane.insert(0, pos )
            pos = isOneBeside(i, dir, num)
            num -= 1
        pos = '_'
        num = 1
        while pos != '':
            if pos == '_':
                pos = isOneBeside( i, dir, num )
                num+= 1
                plane.append(pos)
                pos = isOneBeside(i, dir, num)
                num += 1
            else:
                plane.append( pos )
                pos = isOneBeside(i, dir, num)
                num+= 1
        word = getWord(plane)
        if word not in words:
            words.append(word)
            group.append(crosswordAnswer.Word(word, index, plane[0]))
            index += 1
    return group

def isOneBeside( index, dir, num ):
    loc = getLocations(index)
    newLoc = ''
    if dir == 0:
        newLoc = str(loc[0] + num) + '.' + str(loc[1])
    else:
        newLoc = str(loc[0]) + '.' + str(loc[1] + num)
    if newLoc in gridIndexs:
        return newLoc
    return ''

def getWord( indexs ):
    word= ''
    for i in indexs:
        loc = getLocations(i)
        word+= grid[loc[0]][loc[1]]
    return word

def orderIndexs( indexs, dir ):
    ordered = []
    for i in indexs:
        if len(ordered) == 0:
            ordered.append(i)
        elif getLocations(i)[dir] < getLocations(ordered[0])[dir]:
            ordered.insert(0, i)
        elif getLocations(i)[dir] > getLocations(ordered[len(ordered)-1])[dir]:
            ordered.append(i)
        else:
            for j in ordered:
                if getLocations(i)[dir] > getLocations(j)[dir]:
                    ordered.insert( ordered.index(j), i )
    return ordered

def isSequential( list, dir ):
    words = []
    word = []
    for i in list:
        if len(word) == 0:
            word.append(i)
        else:
            loc1 = getLocations(word[len(word) - 1] )
            loc2 = getLocations(i)
            if loc1[dir] + 1 == loc2[dir]:
                word.append( i )
            else:
                words.append(word)
                word.clear()
    return words

across = []
down = []

def transformGrid():
    global across
    across = groupWords( 1 )
    global down
    down = groupWords( 0 )

    for i in across:
        grid[ i.getRowPos() ][ i.getColPos() ] = str(i.index)
    for k in down:
        crossIndex = grid[ k.getRowPos() ][ k.getColPos() ]
        if crossIndex.isnumeric() and crossIndex != k.index:
            actionRequired = ''
            for i in down:
                if i.index == crossIndex:
                    actionRequired = i
            if actionRequired != '':
                greatest = findGreatestIndex( down )
                down[down.index(actionRequired)] = greatest
            down[down.index( k )].index = str(crossIndex)
        else:
            grid[k.getRowPos()][k.getColPos()] = str(k.index)


def findGreatestIndex( group ):
    greatest = 0
    for i in group:
        if int(i.index) > greatest:
            greatest = int(i.index)
    return greatest


def createCrossword():
    sorted = sortArray(words)
    dump = []
    for i in sorted:
        if not addWordToGrid(i , grid, gridIndexs):
            dump.append(i)
    length = len(dump)
    length += 1
    while len(dump) != length:
        length = len(dump)
        for i in dump:
            if addWordToGrid(i, grid, gridIndexs):
                dump.remove(i)