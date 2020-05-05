import random 

listOfShit = ['Darrel Long', 'Mackey', 'CE12', 'Dining Hall', 'Flexi Dollars', \
    'Iveta', 'Owl\'s Nest', 'Raymond\'s Catering', 'CMPS-12B', 'Tracy Larrabee', \
    'Yerba', 'Science and Engineering Library', 'Strike', 'Patrick Tantalo', 'Asbestos', \
    'Porter', 'College Nine/Ten', 'Stevenson', 'Crown', 'Seshadhri', \
    'Dimitris', 'Slug', 'Deer', 'International', 'Meme', \
    'Gaming', '4/20', 'Marijuana', 'Psychidelics', 'Bus', \
    'Housing', 'Drunk Monkeys', 'Opers', 'Walk', 'Classroom Unit 2']

#honestly this is unnecessarily complicated but oh well LOL
def generateNames():
    firstlist = []
    rows, cols = (5, 5) 
    arr2D = [[0 for i in range(cols)] for j in range(rows)] 
    #above creates 2d array 5x5 with 0s  
    for i in range(25):
        r=random.randint(0, len(listOfShit) - 1)
        theWord=listOfShit[r]
        while(theWord in firstlist):
            r=random.randint(0, len(listOfShit) - 1)
            theWord=listOfShit[r]
            #if we get a repeat word keep regenerating until we get a new word
        firstlist.append(theWord)
    #its a list of 25 words, turning it into a 2D list with 5 list of 5 words
    for i in range(5):
        for n in range(5):
            arr2D[i][n] = firstlist[i*5 + n]
    return arr2D

generateNames()

