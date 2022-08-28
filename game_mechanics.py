import random

class TeamGame():
    # defines games that can be played
    def __init__(self,name='1',players=['Player 1','Player 2'],scoreboard=[],teams=[],
    next=0,over=False,winner='',startscore=0,training=False):
        self.name = name
        self.players = players
        self.scoreboard = scoreboard
        self.teams = teams
        self.next = next
        self.over = False
        self.winner = winner
        self.startscore = startscore
        self.backup_scoreboard = []
        self.training = False

    def printscore(self):
        team1 = self.teams[0]
        team2 = self.teams[1]
        print(team1.displayname+":",team1.space,team1.score)
        print(team2.displayname+":",team2.space,team2.score,'\n')
        print(self.scoreboard,'\n')

    def scoreturn(self):
        pass

    def maketeams(self):
        print('\nWelcome, ',self.players,'\n')
        random.shuffle(self.players)

        team1list = []
        team2list = []

        for i in range(len(self.players)):
            if i%2 == 0:
                team1list.append(self.players[i])
            else:
                team2list.append(self.players[i])

        team1 = Team(players=team1list)
        team2 = Team(players=team2list)

        for i in range(len(team1.players)):
            if i == 0:
                team1.displayname = str(team1.players[i])
                team2.displayname = str(team2.players[i])
            else:
                team1.displayname = str(team1.displayname + ', ' + team1.players[i])
                team2.displayname = str(team2.displayname + ', ' + team2.players[i])

        team1.space = ' ' * (len(team2.displayname)-len(team1.displayname))
        team2.space = ' ' * (len(team1.displayname)-len(team2.displayname))

        self.teams = [team1,team2]

    def rungame(self):
        self.setup()
        self.printscore()
        while self.over != True:
            self.scoreturn()
        print('Congrats! -',self.winner)

class SingleGame():
    # defines games that can be played
    def __init__(self,name='1',playernames=[],scoreboard=[],next=0,over=False,winner='',players=[], training=False, training_level = '1'):
        self.name = name
        self.playernames = playernames
        self.scoreboard = scoreboard
        self.next = next
        self.over = False
        self.winner = winner
        self.players = players
        self.training = training
        self.training_level = training_level

    def printscore(self):
        print()
        for i in range(len(self.players)):
            print(self.players[i].name+":",self.players[i].space,self.players[i].score)
        print('\n',self.scoreboard,'\n')

    def scoreturn(self):
        pass

    def maketeams(self):
        print('\nWelcome, ',self.playernames,'\n')

        random.shuffle(self.playernames)

        ## loop through and figure out max name
        lengths = []
        for i in range(len(self.playernames)):
            self.players.append(Player(self.playernames[i]))
            lengths.append(len(self.players[i].name))

        for i in range(len(self.players)):
            self.players[i].space = ' ' * (max(lengths) - len(self.players[i].name))

    def rungame(self):
        self.setup()
        self.printscore()
        while self.over != True:
            self.scoreturn()
        print('Congrats! -',self.winner)

class Team():
    # define teams
    def __init__(self,players,score=0, space=0, displayname=''):
        self.players = players
        self.score = score
        self.space = space
        self.displayname = displayname
        self.backup_score = 0

class Turn():
    # define turns
    def __init__(self,team='Team 1',player = 'Player 1',message ='',darts=[],number_dict={},opponent=[],numbers=[]):
        self.team = team
        self.player = player
        self.message = message
        self.darts = darts
        self.number_dict= number_dict
        self.opponent = opponent
        self.numbers= numbers

class Player():
    # define teams
    def __init__(self,name='',score=0, space=0, lives=3):
        self.name = name
        self.score = score
        self.space = space
        self.lives = lives
        # Is this class actually being used anywhere?