import random
import pandas as pd

class TeamGame():
    # defines games that can be played
    def __init__(self,name='1',players=['Player 1','Player 2'],gametype='1',scoreboard=[],teams=[],next=0,over=False,winner='',startscore=0):
        self.name = name
        self.players = players
        self.gametype = gametype
        self.scoreboard = scoreboard
        self.teams = teams
        self.next = next
        self.over = False
        self.winner = winner
        self.startscore = startscore
        self.backup_scoreboard = []

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

        if self.gametype == '1':
            team1 = Team(players=self.players[0])
            team2 = Team(players=self.players[1])
            team1.displayname = team1.players
            team2.displayname = team2.players
        else:
            team1 = Team(players=[self.players[0],self.players[2]])
            team2 = Team(players=[self.players[1],self.players[3]])
            team1.displayname = str(team1.players[0]) + ' and ' + str(team1.players[1])
            team2.displayname = str(team2.players[0]) + ' and ' + str(team2.players[1])

        team1.space = ' ' * (len(team2.displayname)-len(team1.displayname))
        team2.space = ' ' * (len(team1.displayname)-len(team2.displayname))

        self.teams = [team1,team2]

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

class Cricket(TeamGame):
    def __init__(self, name='1', players=['Player 1', 'Player 2'], gametype ='1', scoreboard=[], next=0, over=False,winner=''):
        TeamGame.__init__(self,name,players,gametype,scoreboard,next,over,winner)

    def setup(self):
        self.maketeams()

        self.teams[0].numbers = [0] * 7
        self.teams[1].numbers = [0] * 7

        self.teams[0].backup_numbers = [0] * 7
        self.teams[1].backup_numbers = [0] * 7

        self.scoreboard = pd.DataFrame({'Team 1':self.teams[0].numbers,'Team 2':self.teams[1].numbers},index=['20','19','18','17','16','15','Bull'])
        self.scoreboard.columns = [self.teams[0].displayname,self.teams[1].displayname]

        self.backup_scoreboard = pd.DataFrame({'Team 1':self.teams[0].numbers,'Team 2':self.teams[1].numbers},index=['20','19','18','17','16','15','Bull'])
        self.backup_scoreboard.columns = [self.teams[0].displayname,self.teams[1].displayname]

    def scoreturn(self):
        current_turn = Turn()

        if self.gametype == '1':
            current_turn.message = self.players[self.next%2] + " - you're up!\n"
        else:
            current_turn.message = self.players[self.next%4] + " - you're up!\n"

        while (True):

            try:
                current_turn.darts = input(current_turn.message)

                if current_turn.darts == 'exit':
                    self.over = True
                    break

                ## this is where you can check to see if the user said "undo"
                if current_turn.darts == 'undo':
                    ## if yes, retrive the old stuff

                    self.next -= 1
                    self.teams[0].score = int(self.teams[0].backup_score)
                    self.teams[1].score = int(self.teams[1].backup_score)

                    self.teams[0].numbers = list(self.teams[0].backup_numbers)
                    self.teams[1].numbers = list(self.teams[1].backup_numbers)

                    break

                else:
                    ## update object
                    self.teams[0].backup_score = int(self.teams[0].score)
                    self.teams[1].backup_score = int(self.teams[1].score)

                    self.teams[0].backup_numbers = list(self.teams[0].numbers)
                    self.teams[1].backup_numbers = list(self.teams[1].numbers)

                if current_turn.darts == 'miss':
                    self.next += 1
                    self.printscore()
                    break

                else:
                    current_turn.darts = current_turn.darts.split(',')

                    current_turn.number_dict = dict(zip(self.scoreboard.index,[0]*7))

                    score_dict = dict(zip(['t','d','s'],[3,2,1]))

                    letterval = ''
                    dartnum = ''
                    numberval = 0

                    for i in range(len(current_turn.darts)):
                        letterval = current_turn.darts[i][0]
                        numberval = score_dict[letterval]
                        dartnum = current_turn.darts[i][1:]
                        current_turn.number_dict[dartnum] += numberval

                    current_turn.numbers = list(current_turn.number_dict.values())

                    # add current to existing
                    if (self.next%2 == 0):
                        current_turn.team = self.teams[0]
                        current_turn.opponent = self.teams[1]
                    else:
                        current_turn.team = self.teams[1]
                        current_turn.opponent = self.teams[0]

                    # compare teams

                    scorelist = [20,19,18,17,16,15,25]

                    for i in range(7):
                        current_turn.team.numbers[i] = current_turn.team.numbers[i] + current_turn.numbers[i]
                        if current_turn.team.numbers[i] > 3 and current_turn.opponent.numbers[i] == 3:
                            current_turn.team.numbers[i] = 3
                            continue

                        if current_turn.team.numbers[i] > 3 and current_turn.opponent.numbers[i] < 3:
                            current_turn.team.score += (current_turn.team.numbers[i] - 3) * scorelist[i]
                            current_turn.team.numbers[i] = 3

                    # update teams
                    if (self.next%2 == 0):
                        self.teams[0] = current_turn.team
                        self.teams[1] = current_turn.opponent
                    else:
                        self.teams[1] = current_turn.team
                        self.teams[0] = current_turn.opponent

                    self.next += 1

                    self.scoreboard = pd.DataFrame({'Team 1':self.teams[0].numbers,'Team 2':self.teams[1].numbers},index=['20','19','18','17','16','15','Bull'])
                    self.scoreboard.columns = [self.teams[0].displayname,self.teams[1].displayname]

                    self.printscore()

                    if ((current_turn.team.score > current_turn.opponent.score) and (min(current_turn.team.numbers) == 3)):
                        self.over = True
                        self.winner = current_turn.team.displayname

                    break

            except:
                pass

class Spanish(TeamGame):
    def __init__(self, name='1', players=['Player 1', 'Player 2'], gametype ='1', scoreboard=[], next=0, over=False, winner=''):
        TeamGame.__init__(self,name,players,gametype,scoreboard,next,over,winner)

    def setup(self):
        self.maketeams()

        self.teams[0].numbers = [0] * 11
        self.teams[1].numbers = [0] * 11

        self.scoreboard = pd.DataFrame({'Team 1':self.teams[0].numbers,'Team 2':self.teams[1].numbers},index=['20','19','18','17','16','15','14','13','12','11','10'])
        self.scoreboard.columns = [self.teams[0].displayname,self.teams[1].displayname]

    def scoreturn(self):
        current_turn = Turn()

        if self.gametype == '1':
            current_turn.message = self.players[self.next%2] + " - you're up!\n"
        else:
            current_turn.message = self.players[self.next%4] + " - you're up!\n"

        while (True):
            try:
                current_turn.darts = input(current_turn.message)

                if current_turn.darts == 'exit':
                    self.over = True
                    break

                ## this is where you can check to see if the user said "undo"
                if current_turn.darts == 'undo':
                    ## if yes, retrive the old stuff

                    self.next -= 1
                    self.teams[0].score = int(self.teams[0].backup_score)
                    self.teams[1].score = int(self.teams[1].backup_score)

                    self.teams[0].numbers = list(self.teams[0].backup_numbers)
                    self.teams[1].numbers = list(self.teams[1].backup_numbers)

                    break

                else:
                    ## update object
                    self.teams[0].backup_score = int(self.teams[0].score)
                    self.teams[1].backup_score = int(self.teams[1].score)

                    self.teams[0].backup_numbers = list(self.teams[0].numbers)
                    self.teams[1].backup_numbers = list(self.teams[1].numbers)

                if current_turn.darts == 'miss':
                    self.next += 1
                    self.printscore()
                    break

                else:
                    current_turn.darts = current_turn.darts.split(',')

                    current_turn.number_dict = dict(zip(self.scoreboard.index,[0]*11))

                    score_dict = dict(zip(['t','d','s'],[3,2,1]))

                    letterval = ''
                    dartnum = ''
                    numberval = 0

                    for i in range(len(current_turn.darts)):
                        letterval = current_turn.darts[i][0]
                        numberval = score_dict[letterval]
                        dartnum = current_turn.darts[i][1:]
                        current_turn.number_dict[dartnum] += numberval

                    current_turn.numbers = list(current_turn.number_dict.values())

                    # add current to existing
                    if (self.next%2 == 0):
                        current_turn.team = self.teams[0]
                        current_turn.opponent = self.teams[1]
                    else:
                        current_turn.team = self.teams[1]
                        current_turn.opponent = self.teams[0]

                    # compare teams

                    scorelist = [20,19,18,17,16,15,14,13,12,11,10]

                    for i in range(11):
                        current_turn.team.numbers[i] = current_turn.team.numbers[i] + current_turn.numbers[i]
                        if current_turn.team.numbers[i] > 3 and current_turn.opponent.numbers[i] == 3:
                            current_turn.team.numbers[i] = 3
                            continue

                        if current_turn.team.numbers[i] > 3 and current_turn.opponent.numbers[i] < 3:
                            current_turn.team.score += (current_turn.team.numbers[i] - 3) * scorelist[i]
                            current_turn.team.numbers[i] = 3

                    # update teams
                    if (self.next%2 == 0):
                        self.teams[0] = current_turn.team
                        self.teams[1] = current_turn.opponent
                    else:
                        self.teams[1] = current_turn.team
                        self.teams[0] = current_turn.opponent

                    self.next += 1

                    self.scoreboard = pd.DataFrame({'Team 1':self.teams[0].numbers,'Team 2':self.teams[1].numbers},index=['20','19','18','17','16','15','14','13','12','11','10'])
                    self.scoreboard.columns = [self.teams[0].displayname,self.teams[1].displayname]

                    self.printscore()

                    if ((current_turn.team.score > current_turn.opponent.score) and (min(current_turn.team.numbers) == 3)):
                        self.over = True
                        self.winner = current_turn.team.displayname
                    break
            except:
                pass

class Minnesota(TeamGame):
    def __init__(self, name='1', players=['Player 1', 'Player 2'], gametype ='1', scoreboard=[], next=0, over=False, winner='', extrascore=0):
        TeamGame.__init__(self,name,players,gametype,scoreboard,next,over,winner,extrascore)
        self.extrascore = extrascore

    def setup(self):
        self.maketeams()

        self.teams[0].numbers = [0] * 10
        self.teams[1].numbers = [0] * 10

        self.scoreboard = pd.DataFrame({'Team 1':self.teams[0].numbers,'Team 2':self.teams[1].numbers},index=['20','19','18','17','16','15','Bull','T','D','Bed'])
        self.scoreboard.columns = [self.teams[0].displayname,self.teams[1].displayname]

    def scoreturn(self):
        current_turn = Turn()

        if self.gametype == '1':
            current_turn.message = self.players[self.next%2] + " - you're up!\n"
        else:
            current_turn.message = self.players[self.next%4] + " - you're up!\n"

        while (True):
            try:
                current_turn.darts = input(current_turn.message)

                if current_turn.darts == 'exit':
                    self.over = True
                    break

                ## this is where you can check to see if the user said "undo"
                if current_turn.darts == 'undo':
                    ## if yes, retrive the old stuff

                    self.next -= 1
                    self.teams[0].score = int(self.teams[0].backup_score)
                    self.teams[1].score = int(self.teams[1].backup_score)

                    self.teams[0].numbers = list(self.teams[0].backup_numbers)
                    self.teams[1].numbers = list(self.teams[1].backup_numbers)

                    break

                else:
                    ## update object
                    self.teams[0].backup_score = int(self.teams[0].score)
                    self.teams[1].backup_score = int(self.teams[1].score)

                    self.teams[0].backup_numbers = list(self.teams[0].numbers)
                    self.teams[1].backup_numbers = list(self.teams[1].numbers)

                current_turn.extrascore = int(input('Extra score?\n'))

                if current_turn.darts == 'miss':
                    self.next += 1
                    self.printscore()
                    break

                else:
                    current_turn.darts = current_turn.darts.split(',')

                    current_turn.number_dict = dict(zip(self.scoreboard.index,[0]*10))

                    score_dict = dict(zip(['t','d','s'],[3,2,1]))

                    letterval = ''
                    dartnum = ''
                    numberval = 0

                    for i in range(len(current_turn.darts)):
                        letterval = current_turn.darts[i][0]
                        numberval = score_dict[letterval]
                        dartnum = current_turn.darts[i][1:]
                        current_turn.number_dict[dartnum] += numberval

                    current_turn.numbers = list(current_turn.number_dict.values())

                    # add current to existing
                    if (self.next%2 == 0):
                        current_turn.team = self.teams[0]
                        current_turn.opponent = self.teams[1]
                    else:
                        current_turn.team = self.teams[1]
                        current_turn.opponent = self.teams[0]

                    # compare teams

                    scorelist = [20,19,18,17,16,15,25,0,0,0]

                    for i in range(10):
                        current_turn.team.numbers[i] = current_turn.team.numbers[i] + current_turn.numbers[i]
                        if current_turn.team.numbers[i] > 3 and current_turn.opponent.numbers[i] == 3:
                            current_turn.team.numbers[i] = 3
                            continue

                        if current_turn.team.numbers[i] > 3 and current_turn.opponent.numbers[i] < 3:
                            current_turn.team.score += (current_turn.team.numbers[i] - 3) * scorelist[i]
                            current_turn.team.numbers[i] = 3

                    current_turn.team.score += current_turn.extrascore

                    # update teams
                    if (self.next%2 == 0):
                        self.teams[0] = current_turn.team
                        self.teams[1] = current_turn.opponent
                    else:
                        self.teams[1] = current_turn.team
                        self.teams[0] = current_turn.opponent

                    self.next += 1

                    self.scoreboard = pd.DataFrame({'Team 1':self.teams[0].numbers,'Team 2':self.teams[1].numbers},index=['20','19','18','17','16','15','Bull','T','D','Bed'])
                    self.scoreboard.columns = [self.teams[0].displayname,self.teams[1].displayname]

                    self.printscore()

                    if ((current_turn.team.score > current_turn.opponent.score) and (min(current_turn.team.numbers) == 3)):
                        self.over = True
                        self.winner = current_turn.team.displayname
                    break
            except:
                pass

class X01(TeamGame):
    def __init__(self, name='1', players=['Player 1', 'Player 2'], gametype ='1', scoreboard=[], next=0, over=False,winner='',startscore=501):
        TeamGame.__init__(self,name,players,gametype,scoreboard,next,over,winner,startscore)
        self.startscore = startscore

    def setup(self):
        self.maketeams()

        self.teams[0].score = self.startscore
        self.teams[1].score = self.startscore

    def scoreturn(self):
        current_turn = Turn()

        if self.gametype == '1':
            current_turn.message = self.players[self.next%2] + "- you're up!\n"
        else:
            current_turn.message = self.players[self.next%4] + "- you're up!\n"

        while (True):
            try:
                current_turn.darts = input(current_turn.message)

                if current_turn.darts == 'exit':
                    self.over = True
                    break

                ## this is where you can check to see if the user said "undo"
                if current_turn.darts == 'undo':
                    ## if yes, retrive the old stuff

                    self.next -= 1
                    self.teams[0].score = int(self.teams[0].backup_score)
                    self.teams[1].score = int(self.teams[1].backup_score)
                    break

                else:
                    ## update object
                    current_turn.darts = int(current_turn.darts)
                    self.teams[0].backup_score = int(self.teams[0].score)
                    self.teams[1].backup_score = int(self.teams[1].score)

                # add current to existing
                if (self.next%2 == 0):
                    current_turn.team = self.teams[0]
                    current_turn.opponent = self.teams[1]
                else:
                    current_turn.team = self.teams[1]
                    current_turn.opponent = self.teams[0]

                current_turn.team.score -= current_turn.darts

                # update teams
                if (self.next%2 == 0):
                    self.teams[0] = current_turn.team
                    self.teams[1] = current_turn.opponent
                else:
                    self.teams[1] = current_turn.team
                    self.teams[0] = current_turn.opponent

                self.next += 1

                print()
                self.printscore()

                if (current_turn.team.score == 0):
                    self.over = True
                    self.winner = current_turn.team.displayname
                break
            except:
                pass

    def printscore(self):
        team1 = self.teams[0]
        team2 = self.teams[1]
        print(team1.displayname+":",team1.space,team1.score)
        print(team2.displayname+":",team2.space,team2.score,'\n')

class SingleGame():
    # defines games that can be played
    def __init__(self,name='1',playernames=[],scoreboard=[],next=0,over=False,winner='',players=[]):
        self.name = name
        self.playernames = playernames
        self.scoreboard = scoreboard
        self.next = next
        self.over = False
        self.winner = winner
        self.players = players

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

class Player():
    # define teams
    def __init__(self,name='',score=0, space=0, lives=3):
        self.name = name
        self.score = score
        self.space = space
        self.lives = lives

class Legs(SingleGame):
    def __init__(self, name='1', playernames=[], scoreboard=[], next=0, over=False,winner='', startlegs=5, leadscore = 26):
        TeamGame.__init__(self,name,scoreboard,next,over,winner)
        self.playernames = playernames
        self.startlegs = startlegs
        self.leadscore = leadscore
        self.totallives = startlegs * len(playernames)
        self.next = next
        self.backup_leadscore = []
        self.backup_totallives = []

    def setup(self):
        self.maketeams()

        for i in range(len(self.players)):
            self.players[i].lives = self.startlegs

    def scoreturn(self):
        current_turn = Turn()

        current_turn.player = self.players[self.next%len(self.players)]

        # check if the player is still in
        if current_turn.player.lives == 0:
            self.next += 1
            self.printscore()

        else:
            # check if you've won
            if current_turn.player.lives == self.totallives:
                self.over = True
                self.winner = current_turn.player.name

            else:
                current_turn.message = current_turn.player.name + " - you're up!\n" + str(self.leadscore) + " to you\n"

                while (True):
                    try:
                        current_turn.darts = input(current_turn.message)

                        if current_turn.darts == 'exit':
                            self.over = True
                            break

                        if current_turn.darts == 'undo':
                            ## if yes, retrive the old stuff
                            self.next -= 1
                            # need a backup lead score
                            self.leadscore = int(self.backup_leadscore)
                            # need a backup total lives
                            self.totallives = int(self.backup_totallives)
                            # need to backup each players legs
                            for i in range(len(self.players)):
                                self.players[i].lives = self.players[i].backup_lives
                            break

                        else:
                            ## update object
                            current_turn.darts = int(current_turn.darts)

                            self.backup_leadscore = int(self.leadscore)
                            self.backup_totallives = int(self.totallives)

                            for i in range(len(self.players)):
                                self.players[i].backup_lives = self.players[i].lives

                        if current_turn.darts > self.leadscore:
                            self.leadscore = current_turn.darts
                            self.next += 1
                            self.printscore()
                            break

                        else:
                            self.next += 1
                            self.leadscore = 26
                            current_turn.player.lives -= 1
                            self.totallives -= 1
                            self.printscore()
                            break
                    except:
                        pass

    def printscore(self):
        for i in range(len(self.players)):
            print(self.players[i].name+":",self.players[i].space,self.players[i].lives)
        print()

class Follow(SingleGame):
    def __init__(self, name='1', playernames=[], scoreboard=[], next=0, over=False,winner='', startlegs=5, leadscore = 'Open',leader=[]):
        TeamGame.__init__(self,name,scoreboard,next,over,winner)
        self.playernames = playernames
        self.startlegs = startlegs
        self.leadscore = leadscore
        self.totallives = startlegs * len(playernames)
        self.leader = leader
        self.next = next

    def setup(self):
        self.maketeams()

        for i in range(len(self.players)):
            self.players[i].lives = self.startlegs

    def scoreturn(self):
        current_turn = Turn()

        current_turn.player = self.players[self.next%len(self.players)]

        # check if the player is still in
        if current_turn.player.lives == 0:
            self.next += 1
            self.printscore()

        else:
            # check if you've won
            if current_turn.player.lives == self.totallives:
                self.over = True
                self.winner = current_turn.player.name

            elif self.leader == current_turn.player:
                self.next += 1

            else:
                current_turn.message = current_turn.player.name + " - you're up!\n" + str(self.leadscore) + " to you\n"

                while (True):
                    try:
                        current_turn.darts = input(current_turn.message)

                        if current_turn.darts == 'exit':
                            self.over = True
                            break

                        if current_turn.darts == 'undo':
                            ## if yes, retrive the old stuff
                            self.next -= 1
                            # need a backup lead score
                            self.leadscore = str(self.backup_leadscore)
                            # need a backup total lives
                            self.totallives = int(self.backup_totallives)
                            # need to backup each players legs
                            for i in range(len(self.players)):
                                self.players[i].lives = int(self.players[i].backup_lives)
                            break

                        else:
                            ## update object
                            current_turn.darts = current_turn.darts

                            self.backup_leadscore = str(self.leadscore)
                            self.backup_totallives = int(self.totallives)

                            for i in range(len(self.players)):
                                self.players[i].backup_lives = int(self.players[i].lives)

                        if current_turn.darts != 'miss':
                            self.leadscore = current_turn.darts
                            self.next += 1
                            self.leader = current_turn.player
                            self.printscore()
                            break

                        else:
                            self.next += 1
                            current_turn.player.lives -= 1
                            self.totallives -= 1
                            self.printscore()
                            break
                    except:
                        pass

    def printscore(self):
        for i in range(len(self.players)):
            print(self.players[i].name+":",self.players[i].space,self.players[i].lives)
        print()

class Golf(SingleGame):
    def __init__(self, name='1', playernames=[], scoreboard=[], next=0, over=False,winner='', holes=18, leadscore = 'Open',leader=[], hole=1):
        TeamGame.__init__(self,name,scoreboard,next,over,winner)
        self.playernames = playernames
        self.leadscore = leadscore
        self.totalturns = 1
        self.winner = winner
        self.hole = hole
        self.next = next
        self.overtime = False
        self.holes = holes

    def setup(self):
        self.maketeams()

    def scoreturn(self):
        current_turn = Turn()

        current_turn.player = self.players[self.next%len(self.players)]

        current_turn.message = current_turn.player.name + " - you're up!\n"

        while (True):
            try:
                current_turn.darts = input(current_turn.message)

                if current_turn.darts == 'exit':
                    self.over = True
                    break

                if current_turn.darts == 'undo':
                    # restore backups
                    self.next -= 1
                    self.leadscore = str(self.backup_leadscore)
                    self.totalturns = int(self.backup_totalturns)
                    self.hole = int(self.backup_hole)
                    self.overtime = bool(self.backup_overtime)

                    for i in range(len(self.players)):
                        self.players[i].score = int(self.players[i].backup_score)
                    break

                else:
                    ## update object
                    current_turn.darts = int(current_turn.darts)
                    # set backups
                    self.backup_leadscore = str(self.leadscore)
                    self.backup_totalturns = int(self.totalturns)
                    self.backup_hole = int(self.hole)
                    self.backup_overtime = bool(self.overtime)

                    for i in range(len(self.players)):
                        self.players[i].backup_score = int(self.players[i].score)

                self.totalturns += 1
                if (self.totalturns%len(self.playernames) == 1):
                    self.hole += 1

                current_turn.player.score += current_turn.darts
                self.printscore()

                self.players[self.next%len(self.players)] = current_turn.player
                self.next += 1
                break

            except:
                pass

        # check if it's the 19th hole or greater
        if self.hole >= (self.holes + 1):
            self.leadscore = self.hole * 6
            for i in range(len(self.players)):
                if self.players[i].score == self.leadscore:
                    self.overtime = True
                if self.players[i].score < self.leadscore:
                    self.overtime = False
                    self.leadscore = self.players[i].score
                    self.winner = self.players[i].name

            if self.overtime == False:
                self.over = True


    def printscore(self):

        print('\nHole: ',self.hole,'\n')
        for i in range(len(self.players)):
            print(self.players[i].name+":",self.players[i].space,self.players[i].score)
        print()

class Killer(SingleGame):
    def __init__(self, name='1', playernames=[], scoreboard=[], next=0, over=False,winner=''):
        TeamGame.__init__(self,name,scoreboard,next,over,winner)
        self.playernames = playernames
        self.startlegs = 0
        self.leadscore = 'Open'
        self.next = next
        self.numbers = []
        self.totallives = 0

    def setup(self):
        self.maketeams()


        keys = []
        values = []

        for i in range(len(self.players)):
            self.players[i].lives = self.startlegs
            while (True):
                number = random.randint(1,20)
                if number not in self.numbers:
                    self.players[i].number = number
                    self.numbers.append(number)
                    keys.append(self.players[i].name)
                    values.append(self.players[i].lives)
                    break
            self.players[i].killer = False

        self.backup_numbers = dict(zip(keys,values))

    def scoreturn(self):

        current_turn = Turn()

        current_turn.player = self.players[self.next%len(self.players)]

        if self.next < len(self.players):
            # turn 1 stuff
            current_turn.message = current_turn.player.name + " - you're up!\n"

            while (True):
                try:
                    current_turn.darts = input(current_turn.message)
                    if current_turn.darts == 'exit':
                        self.over = True
                        break

                    elif current_turn.darts == 'undo':
                        self.totallives = int(self.backup_totallives)
                        for i in range(len(self.players)):
                            self.players[i].lives = int(self.backup_numbers[self.players[i].name])
                        self.next -= 1
                        self.printscore()
                        break

                    else:
                        current_turn.darts = int(current_turn.darts)

                        if (current_turn.darts >= 0 & current_turn.darts <=3):

                            for i in range(len(self.players)):
                                self.backup_numbers[self.players[i].name] = int(self.players[i].lives)

                            self.backup_totallives = int(self.totallives)

                            current_turn.player.lives = int(current_turn.darts)
                            self.totallives += int(current_turn.darts)
                            self.players[self.next%len(self.players)] = current_turn.player
                            self.next += 1
                            self.printscore()
                            break
                except:
                    pass
        else:

            # after turn 1
            # check if the player is still in
            if current_turn.player.lives == 0:
                self.next += 1

            # check if you've won
            elif current_turn.player.lives == self.totallives:
                self.over = True
                self.winner = current_turn.player.name

            else:
                # receive input
                while (True):

                    current_turn.message = current_turn.player.name + " - you're up!\n"

                    current_turn.darts = input(current_turn.message)

                    if current_turn.darts == 'exit':
                        self.over = True
                        break

                    elif current_turn.darts == 'undo':
                        self.totallives = int(self.backup_totallives)
                        for i in range(len(self.players)):
                            self.players[i].lives = int(self.backup_numbers[self.players[i].name])
                        self.next -= 1
                        self.printscore()
                        break

                    elif current_turn.darts == 'miss':
                        self.next += 1
                        self.printscore()
                        break

                    else:
                        current_turn.darts = current_turn.darts.split(",")
                        print((len(current_turn.darts)-1)/2)
                        mine = current_turn.darts[0]
                        target = []
                        count = []

                        ##### find a way to loop through the rest of the list and create target/count lists and make a dictionary
                        for i in range(1,len(current_turn.darts)):
                            if i == 1:
                                target.append(current_turn.darts[i])
                            elif i%2 != 0:
                                target.append(current_turn.darts[i])
                            elif i%2 == 0:
                                count.append(current_turn.darts[i])

                        target_dict = dict(zip(target,count))

                        for i in range(len(self.players)):
                            self.backup_numbers[self.players[i].name] = int(self.players[i].lives)
                        self.backup_totallives = int(self.totallives)

                        # player's lives
                        current_turn.player.lives += int(mine)
                        self.totallives += int(mine)

                        # opponents' liveslist
                        for i in range(len(self.players)):
                            if self.players[i].name in target:
                                self.players[i].lives -= int(target_dict[self.players[i].name])
                                if self.players[i].lives < 0:
                                    self.players[i].lives = 0
                                self.totallives -= int(target_dict[self.players[i].name])

                        self.next += 1
                        self.printscore()
                        break


    def printscore(self):
        playerlist = []
        numberlist = []
        liveslist = []
        for i in range(len(self.players)):
            playerlist.append(self.players[i].name)
            numberlist.append(self.players[i].number)
            liveslist.append(self.players[i].lives)
            # print(self.players[i].name+":",self.players[i].space,self.players[i].lives,'\n')
        print(pd.DataFrame({'Number':numberlist,'Lives':liveslist},index=playerlist),'\n')

class CutthroatCricket(SingleGame):
    def __init__(self, name='1', playernames=[], scoreboard=[], next=0, over=False,winner=''):
        TeamGame.__init__(self,name,scoreboard,next,over,winner)
        self.playernames = playernames
        self.startlegs = 0
        self.leadscore = 'Open'
        self.next = next
        self.numbers = []
        self.totallives = 0

    def setup(self):
        self.maketeams()

        self.scoreboard_dict = {}

        for i in range(len(self.players)):
            self.players[i].numbers = [0] * 7
            self.players[i].backup_numbers = [0] * 7
            self.players[i].score = 0
            self.players[i].backup_score = 0
            self.scoreboard_dict[self.players[i].name] = list(self.players[i].numbers)

        self.scoreboard = pd.DataFrame(self.scoreboard_dict,index=['20','19','18','17','16','15','Bull'])
        self.backup_scoreboard = pd.DataFrame(self.scoreboard_dict,index=['20','19','18','17','16','15','Bull'])

    def scoreturn(self):

        while (True):
            try:
                current_turn = Turn()
                current_turn.player = self.players[self.next%len(self.players)]
                current_turn.message = current_turn.player.name + " - you're up!\n"

                current_turn.darts = input(current_turn.message)

                if current_turn.darts == 'exit':
                    self.over = True
                    break

                ## this is where you can check to see if the user said "undo"
                if current_turn.darts == 'undo':
                    ## if yes, retrive the old stuff

                    for i in range(len(self.players)):
                        self.players[i].score = int(self.players[i].backup_score)
                        self.players[i].numbers = list(self.players[i].backup_numbers)
                    self.next -= 1
                    self.printscore()
                    break

                else:
                    ## update object
                    for i in range(len(self.players)):
                        self.players[i].backup_score = int(self.players[i].score)
                        self.players[i].backup_numbers = list(self.players[i].numbers)

                if current_turn.darts == 'miss':
                    self.next += 1
                    self.printscore()
                    break

                else:
                    current_turn.darts = current_turn.darts.split(',')

                    current_turn.number_dict = dict(zip(self.scoreboard.index,[0]*7))

                    score_dict = dict(zip(['t','d','s'],[3,2,1]))

                    letterval = ''
                    dartnum = ''
                    numberval = 0

                    for i in range(len(current_turn.darts)):
                        letterval = current_turn.darts[i][0]
                        numberval = score_dict[letterval]
                        dartnum = current_turn.darts[i][1:]
                        current_turn.number_dict[dartnum] += numberval

                    current_turn.numbers = list(current_turn.number_dict.values())

                    # compare teams
                    scorelist = [20,19,18,17,16,15,25]

                    for i in range(7):
                        current_turn.player.numbers[i] = current_turn.player.numbers[i] + current_turn.numbers[i]

                        for j in range(len(self.players)):
                            if self.players[j].name != current_turn.player.name:
                                if ((current_turn.player.numbers[i] > 3) & (self.players[j].numbers[i] < 3)):
                                    self.players[j].score += (current_turn.player.numbers[i] - 3) * scorelist[i]

                        if current_turn.player.numbers[i] > 3:
                                current_turn.player.numbers[i] = 3

                    # update teams
                    self.players[self.next%len(self.players)] = current_turn.player

                    self.next += 1

                    for i in range(len(self.players)):
                        self.scoreboard_dict[self.players[i].name] = list(self.players[i].numbers)

                    self.scoreboard = pd.DataFrame(self.scoreboard_dict,index=['20','19','18','17','16','15','Bull'])

                    self.printscore()

                    opponents = (len(self.players) - 1)
                    for i in range(len(self.players)):
                        if current_turn.player.name != self.players[i].name:
                            if current_turn.player.score < self.players[i].score:
                                opponents -= 1

                    if ((opponents == 0) & (min(current_turn.player.numbers) == 3)):
                        self.over = True
                        self.winner = current_turn.player.name
                        break
            except:
                pass

class Cutthroat(SingleGame):
    def __init__(self, name='1', playernames=[], scoreboard=[], next=0, over=False,winner=''):
        TeamGame.__init__(self,name,scoreboard,next,over,winner)
        self.playernames = playernames
        self.startlegs = 3
        self.leadscore = 'Open'
        self.next = next
        self.numbers = []
        self.totallives = 0

    def setup(self):
        self.maketeams()

        # randomly assign numbers
        numbersperplayer = 20//len(self.players)
        temp_dict_name = dict(zip([20,1,18,4,13,6,10,15,2,17,3,19,7,16,8,11,14,9,12,5],['-']*20))
        temp_dict_value = dict(zip([20,1,18,4,13,6,10,15,2,17,3,19,7,16,8,11,14,9,12,5],['-']*20))

        for i in range(len(self.players)):
            self.players[i].numbers = []
            numbercount = 0
            while (True):
                number = random.randint(1,20)
                if number not in self.numbers:
                    self.players[i].numbers.append(number)
                    self.numbers.append(number)
                    temp_dict_name[number] = self.players[i].name
                    temp_dict_value[number] = self.startlegs
                    numbercount += 1
                    if numbercount == numbersperplayer:
                        break
            self.players[i].killer = False
            self.players[i].score_dict = dict(zip(self.players[i].numbers,[self.startlegs]*numbersperplayer))
            self.players[i].backup_score_dict = dict(zip(self.players[i].numbers,[self.startlegs]*numbersperplayer))
            self.dartboard = pd.DataFrame({"Player":list(temp_dict_name.values()),"Lives":list(temp_dict_value.values())},index=list(temp_dict_name.keys()))

    def scoreturn(self):

        current_turn = Turn()

        current_turn.player = self.players[self.next%len(self.players)]

        temp_frame = self.dartboard.copy()

        # check if the player is still in
        if (temp_frame[temp_frame['Player'] == current_turn.player.name]['Lives'].sum() == 0):
            self.next += 1
            self.printscore()

        # check if you've won
        elif (temp_frame[(temp_frame['Player'] != current_turn.player.name) & (temp_frame['Player'] != '-')]['Lives'].sum() == 0):
            self.over = True
            self.winner = current_turn.player.name

        # receive input
        else:
            while (True):
                try:

                    current_turn.message = current_turn.player.name + " - you're up!\n"

                    current_turn.darts = input(current_turn.message)

                    if current_turn.darts == 'exit':
                        self.over = True
                        break

                    elif current_turn.darts == 'undo':
                        pass

                    elif current_turn.darts == 'miss':
                        self.next += 1
                        self.printscore()
                        break

                    else:
                        current_turn.darts = current_turn.darts.split(',')
                        score_dict = dict(zip(['t','d','s'],[3,2,1]))

                        letterval = ''
                        dartnum = ''
                        numberval = 0

                        scratch = False
                        scratchval = 0

                        for i in range(len(current_turn.darts)):
                            letterval = current_turn.darts[i][0]
                            numberval = score_dict[letterval]
                            dartnum = int(current_turn.darts[i][1:])
                            # temp_frame.loc[dartnum]['Lives'] -= numberval
                            temp_frame.loc[dartnum,'Lives'] -= numberval
                            if (temp_frame.loc[dartnum]['Lives'] < 0):
                                temp_frame.loc[dartnum,'Lives'] = 0
                            if (temp_frame.loc[dartnum]['Player'] == current_turn.player.name):
                                scratch = True
                                scratchval = int(numberval)

                        if scratch == True:
                            bringback = input("Scratch - which darts?\n").split(',')

                            for dart in bringback:
                                dart = int(dart)
                                temp_frame.loc[dart,'Lives'] += scratchval
                                if temp_frame.loc[dart]['Lives'] > 3:
                                    temp_frame.loc[dart,'Lives'] = 3

                        self.dartboard = temp_frame.copy()

                        self.next += 1
                        self.printscore()
                        break

                except:
                    pass

    def printscore(self):
        print(self.dartboard,'\n')
        temp_df = self.dartboard
        players = temp_df['Player'].unique()
        for player in players:
            if player != '-':
                score = temp_df[temp_df['Player']==player]['Lives'].sum()
                print(player,'\t',score)
        print()

def main():
    #instantiate game
    start_game = TeamGame()

    # collect player names
    start_game.players = input('Hello, who is playing tonight?\n')
    start_game.players = start_game.players.split(', ')

    # Ask for singles vs doubles
    start_game.gametype = input('\nWhat type of game:\n1. 1x1\n2. 2x2\n3. Free for All\n')
    if (start_game.gametype == '1' or start_game.gametype == '2'):
        start_game.name = input('\nWhat game would you like to play:\n1. Cricket\n2. Spanish\n3. Minnesota\n4. X01\n')

        if start_game.name == '1':
            #instantiate game
            current_game = Cricket(name=start_game.name, players=start_game.players, gametype=start_game.gametype)
            current_game.rungame()

        # Launch spanish
        if start_game.name == '2':
            #instantiate game
            current_game = Spanish(name=start_game.name, players=start_game.players, gametype=start_game.gametype)
            current_game.rungame()

        # Launch minnesota
        if start_game.name == '3':
            #instantiate game
            current_game = Minnesota(name=start_game.name, players=start_game.players, gametype=start_game.gametype)
            current_game.rungame()

        # Launch X01
        if start_game.name == '4':
            start_game.startscore = int(input('What starting score do you want?\n'))
            #instantiate game
            current_game = X01(name=start_game.name, players=start_game.players, gametype=start_game.gametype, startscore=start_game.startscore)
            current_game.rungame()

    elif start_game.gametype == '3':
        start_game.name = input('\nWhat game would you like to play:\n1. Legs\n2. Follow the Leader\n3. Golf\n4. Killer\n5. Cutthroat Cricket\n6. Cutthroat\n')

        # Launch legs
        if start_game.name == '1':
            #instantiate game
            start_game.startscore = int(input('\nHow many legs to start?\n'))
            current_game = Legs(name=start_game.name, playernames=start_game.players, startlegs=start_game.startscore)
            current_game.rungame()

        # Follow the leader
        if start_game.name == '2':
            #instantiate game
            start_game.startscore = int(input('\nHow many legs to start?\n'))
            current_game = Follow(name=start_game.name, playernames=start_game.players, startlegs=start_game.startscore)
            current_game.rungame()

        # Golf
        if start_game.name == '3':
            #instantiate game
            start_game.startscore = int(input('\nHow many holes?\n'))
            current_game = Golf(name=start_game.name, playernames=start_game.players, holes=start_game.startscore)
            current_game.rungame()

        # Killer
        if start_game.name == '4':
            #instantiate game
            current_game = Killer(name=start_game.name, playernames=start_game.players)
            current_game.rungame()

        # CutthroatCricket
        if start_game.name == '5':
            #instantiate game
            current_game = CutthroatCricket(name=start_game.name, playernames=start_game.players)
            current_game.rungame()

        # Cutthroat
        if start_game.name == '6':
            #instantiate game
            current_game = Cutthroat(name=start_game.name, playernames=start_game.players)
            current_game.rungame()

# need to change cutthroat dataframe lives column to string datatype
# need to have exception handling for cutthroat

main()
