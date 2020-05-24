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
            'Housing', 'Drunk Monkeys', 'Opers', 'Walk', 'Classroom Unit 2', \
            'MOSS', 'Cheating', 'Shrooms', 'Sage the Gemini', 'SJW']

        self.flippedCards_set = set()
        ###TODO change to dictionary
        self.team_red = []
        self.team_blue = []
        self.spymasters = [] #first spymaster is red's, second is blue's 
        self.red_agent_count = 8
        self.blue_agent_count = 9 
        self.assasin_count = 1
        self.innocent_bystanders_count = 7
        self.word_board = self._generateWordBoard() 
        self.state_board = self._generateStateBoard()
        self.users = [] #a list of all the usernames in the room 
        self.usersid = {}  #usersid is a dictionary where username maps to their corresponding sid 
        self.current_turn = 'blue' # this should either be blue or red. We start with B to make B always go first.
        self.senders = 0 # represents the number of people who sent cards. We might not need it since we'll implement a timer 


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
        hold = ['A']
        for r in range(self.red_agent_count):
            hold.append('R')
        for r in range(self.blue_agent_count):
            hold.append('B')
        for r in range(self.innocent_bystanders_count):
            hold.append('I')
        random.shuffle(hold)
        res = [[0] * (5) for i in range(5)]
        for i in range(5):
            for n in range(5):
                res[i][n] = hold[i*5 + n]
        return res

    def determineAction(self, cardQ, turn):
        """
        Returns a tuple, (state,word) if successful.
        On duplicate cards returns a tuple with empty strings
        """
        if turn == 'blue' and self.senders != (len(self.team_blue) - 1):
            print("Not time to emit back anything",file=sys.stderr)
            return 'error'
        elif turn == 'red' and self.senders != (len(self.team_red) - 1):
            print("Not time to emit back anything",file=sys.stderr)
            return 'error'
        """
        if (row,col) in self.flippedCards_set:
            print("already flipped before", file=sys.stderr)
            return('','')

        flipped_card = self.state_board[row][col]
        self.flippedCards_set.add((row,col))
         
        if flipped_card != 'A' or flipped_card != 'I':
            self._decrement(flipped_card)

        return (self.state_board[row][col], self.word_board[row][col])
        """
        return 'OK'

    def _decrement(self, card):
        if card == 'B':
            self.blue_agent_count -= 1
        elif card == 'R':
            self.red_agent_count -= 1
        

    