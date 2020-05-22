import random 
import sys



class RoomMaster():
    def __init__(self):
        """
        Class to manage the state of a game board.
        """
        ### We made word board and stateboard two different functions
        ### This way we can alter either if desired.
        ### TODO: Move this out to config file.
        self.word_list = ['Darrel Long', 'Mackey', 'CE12', 'Dining Hall', 'Flexi Dollars', \
            'Iveta', 'Owl\'s Nest', 'Raymond\'s Catering', 'CMPS-12B', 'Tracy Larrabee', \
            'Yerba', 'Science and Engineering Library', 'Strike', 'Patrick Tantalo', 'Asbestos', \
            'Porter', 'College Nine/Ten', 'Stevenson', 'Crown', 'Seshadhri', \
            'Dimitris', 'Slug', 'Deer', 'International', 'Hello Kitty', \
            'Gaming', '4/20', 'Marijuana', 'Psychidelics', 'Bus', \
            'Housing', 'Drunk Monkeys', 'Opers', 'Walk', 'Classroom Unit 2']

        self.flippedCards_set = set()
        self.team_red = []
        self.team_blue = []
        self.spymasters = [] #first spymaster is red's, second is blue's 
        self.red_agent_count = 8
        self.blue_agent_count = 8
        self.double_agent_count = 1 
        self.assasin_count = 1
        self.innocent_bystanders_count = 7
        self.word_board = self._generateWordBoard() 
        self.state_board = self._generateStateBoard()
        self.users = [] #a list of all the usernames in the room 
        self.usersid = {}  #usersid is a dictionary where username maps to their corresponding sid 


    def changeWordBoard(self):
        """
        Sets current GM word_board to a new board
        """
        self.word_board = self._generateWordBoard()
    def changeWordBoard(self):
        """
        Sets current GM state_board to a new board
        """
        self.state_board= self._generateStateBoard()

    def _generateWordBoard(self):
        """
        Places words onto word_board. Alters word_board.
        """
        random.shuffle(self.word_list)
        rows, cols = (5, 5) 
        arr2D = [[0 for i in range(cols)] for j in range(rows)] 
        #its a list of 25 words, turning it into a 2D list with 5 list of 5 words
        for i in range(5):
            for n in range(5):
                arr2D[i][n] = self.word_list[i*5 + n]
        return arr2D
    def _generateStateBoard(self):
        """
        Places agents and bystanders across a board
        R: Red, B: BLUE, D:double, A: Assasin, I: bystander
        """
        hold = ['A','D']
        for r in range(8):
            hold.append('R')
        for r in range(8):
            hold.append('B')
        for r in range(7):
            hold.append('I')
        random.shuffle(hold)
        res = [[0] * (5) for i in range(5)]
        for i in range(5):
            for n in range(5):
                res[i][n] = hold[i*5 + n]
        return res

    def flipCard(self, row,col):
        """
        Returns a tuple, (state,word) if successful.
        On duplicate cards returns a tuple with empty strings
        """
        if (row,col) in self.flippedCards_set:
            print("already flipped before", file=sys.stderr)
            return('','')
            
        return (self.state_board[row][col], self.word_board[row][col])