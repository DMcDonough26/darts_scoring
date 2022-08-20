import random
import pandas as pd
import numpy as np
import datetime as dt

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
        if ((self.training_level != '0') & (self.winner != '')):
            # print summary
            self.output()

            # write to csv
            if len(self.history) == 0:
                pd.DataFrame(dict(zip(self.history.columns,
                    [self.training_player,dt.date.today(),self.game_name,self.training_level,
                    (self.training_player == self.winner)*1,(self.training_player != self.winner)*1,
                    self.total_score,self.total_turns,self.double_darts])),index=[len(self.history)]).to_csv('history.csv', index=False)
            else:
                pd.concat([self.history,pd.DataFrame(dict(zip(self.history.columns,
                    [self.training_player,dt.date.today(),self.game_name,self.training_level,
                    (self.training_player == self.winner)*1,(self.training_player != self.winner)*1,
                    self.total_score,self.total_turns,self.double_darts])),index=[len(self.history)])]).to_csv('history.csv', index=False)

    def output(self):
        pass

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
    def __init__(self, name='1', players=['Player 1', 'Player 2'], scoreboard=[], next=0, over=False,winner='', training_level='1'):
        TeamGame.__init__(self,name,players,scoreboard,next,over,winner)
        self.training_level = training_level
        self.training_player = str(players[0])
        self.game_name = 'Cricket'
        self.winner = winner

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

        if self.training_level != '0':
            self.history = pd.read_csv('history.csv')
            try:
                temp1 = self.history.groupby(['Game','Level']).agg({'Win':'sum','Loss':'sum'})
                temp1['%'] = (temp1['Win']/(temp1['Win']+temp1['Loss'])).round(2)
                print(temp1,'\n\n')

                temp2 = self.history[self.history['Game']==self.game_name].groupby(['Level']).\
                    agg({'Total Score':'sum','Total Turns':'sum'})
                temp2['Average Score'] = (temp2['Total Score']/temp2['Total Turns']).round(0)
                print(temp2,'\n\n')

            except:
                print("Good luck on your first game!\n")

        self.total_score = 0
        self.total_turns = 0
        self.double_darts = 0

    def scoreturn(self):
        current_turn = Turn()

        current_turn.player = self.players[self.next%len(self.players)]
        current_turn.message = current_turn.player + " - you're up!\n"

        while (True):

            try:
                # establish roles
                if (self.next%2 == 0):
                    current_turn.team = self.teams[0]
                    current_turn.opponent = self.teams[1]
                else:
                    current_turn.team = self.teams[1]
                    current_turn.opponent = self.teams[0]


                # confirm that it is the opponent
                if current_turn.player == 'Opponent':

                # loop through per darts
                    darts = []
                    scorelist = [20,19,18,17,16,15,25]
                    target = 0
                    value = 0
                    temp_dict = dict(zip(scorelist,[0]*7))
                    for j in range (3):
                        # if opponent is ahead
                        target = 0
                        if (current_turn.team.score > current_turn.opponent.score):
                            # and if there is something to close, then close
                            for i in range(7):
                                if (current_turn.team.numbers[i] + temp_dict[scorelist[i]]) < 3 and current_turn.opponent.numbers[i] == 3:
                                    target = scorelist[i]
                                    print(target)
                                    break

                            # if not, then open next available
                            if target == 0:
                                for i in range(7):
                                    if (current_turn.team.numbers[i] + temp_dict[scorelist[i]]) < 3:
                                        target = scorelist[i]
                                        break

                        # if opponent is behind
                        else:
                            # and if there is something to point, then point
                            for i in range(7):
                                if (current_turn.team.numbers[i] + temp_dict[scorelist[i]]) == 3 and current_turn.opponent.numbers[i] < 3:
                                    target = scorelist[i]
                                    break
                            # if not, then open next available
                            if target == 0:
                                for i in range(7):
                                    if current_turn.opponent.numbers[i] < 3:
                                        target = scorelist[i]
                                        break

                        # simulate number of darts
                        if target == 25:
                            target = "Bull"
                        else:
                            pass
                        mean_dict = {'1':0.5,'2':1,'3':1.5,'4':2}
                        sd_dict = {'1':0.25,'2':0.5,'3':0.5,'4':1}
                        value = min(max(round(np.random.normal(mean_dict[self.training_level],sd_dict[self.training_level])),0),3)
                        score_dict = dict(zip([3,2,1],['t','d','s']))
                        if value == 0:
                            pass
                        else:
                            darts.append(score_dict[value]+str(target))
                            if target == "Bull":
                                temp_dict[25] += value
                            else:
                                temp_dict[target] += value

                    current_turn.darts = list(darts)
                    print("Opponent scored: ",darts,'\n')

                # if not in training mode
                else:
                    current_turn.darts = input(current_turn.message)

                    if current_turn.darts == 'exit':
                        self.over = True
                        break

                    ## this is where you can check to see if the user said "undo"
                    if current_turn.darts == 'undo':
                        ## if yes, retrive the old stuff

                        self.next -= (1+self.players.count('Opponent'))
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

                    if self.training_level != '0':
                        self.total_turns += 1

                if current_turn.darts == 'miss':
                    self.next += 1
                    self.printscore()
                    break

                else:
                    if current_turn.player == 'Opponent':
                        pass
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

                        if ((self.training_level != '0') & (current_turn.player != 'Opponent')):
                            self.total_score += numberval

                    current_turn.numbers = list(current_turn.number_dict.values())

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

                    if ((current_turn.team.score >= current_turn.opponent.score) and (min(current_turn.team.numbers) == 3)):
                        self.over = True
                        self.winner = current_turn.team.displayname

                    break

            except:
                print('ERROR')

    def output(self):
        print("Average Score: ",int(self.total_score/self.total_turns))

class Spanish(TeamGame):
    def __init__(self, name='1', players=['Player 1', 'Player 2'], scoreboard=[], next=0, over=False, winner='',training_level='1'):
        TeamGame.__init__(self,name,players,scoreboard,next,over,winner)
        self.training_level = training_level
        self.training_player = str(players[0])
        self.game_name = 'Cricket'
        self.winner = winner

    def setup(self):
        self.maketeams()

        self.teams[0].numbers = [0] * 11
        self.teams[1].numbers = [0] * 11

        self.scoreboard = pd.DataFrame({'Team 1':self.teams[0].numbers,'Team 2':self.teams[1].numbers},index=['20','19','18','17','16','15','14','13','12','11','10'])
        self.scoreboard.columns = [self.teams[0].displayname,self.teams[1].displayname]

        if self.training_level != '0':
            self.history = pd.read_csv('history.csv')
            try:
                temp1 = self.history.groupby(['Game','Level']).agg({'Win':'sum','Loss':'sum'})
                temp1['%'] = (temp1['Win']/(temp1['Win']+temp1['Loss'])).round(2)
                print(temp1,'\n\n')

                temp2 = self.history[self.history['Game']==self.game_name].groupby(['Level']).\
                    agg({'Total Score':'sum','Total Turns':'sum'})
                temp2['Average Score'] = (temp2['Total Score']/temp2['Total Turns']).round(0)
                print(temp2,'\n\n')

            except:
                print("Good luck on your first game!\n")

        self.total_score = 0
        self.total_turns = 0
        self.double_darts = 0

    def scoreturn(self):
        current_turn = Turn()

        current_turn.player = self.players[self.next%len(self.players)]
        current_turn.message = current_turn.player + " - you're up!\n"

        while (True):
            try:
                # establish roles
                if (self.next%2 == 0):
                    current_turn.team = self.teams[0]
                    current_turn.opponent = self.teams[1]
                else:
                    current_turn.team = self.teams[1]
                    current_turn.opponent = self.teams[0]

                # confirm whether playing in training mode
                if current_turn.player == 'Opponent':

                # loop through per darts
                    darts = []
                    scorelist = [20,19,18,17,16,15,14,13,12,11,10]
                    target = 0
                    value = 0
                    temp_dict = dict(zip(scorelist,[0]*11))
                    for j in range (3):
                        # if opponent is ahead
                        target = 0
                        if (current_turn.team.score > current_turn.opponent.score):
                            # and if there is something to close, then close
                            for i in range(11):
                                if (current_turn.team.numbers[i] + temp_dict[scorelist[i]]) < 3 and current_turn.opponent.numbers[i] == 3:
                                    target = scorelist[i]
                                    print(target)
                                    break

                            # if not, then open next available
                            if target == 0:
                                for i in range(11):
                                    if (current_turn.team.numbers[i] + temp_dict[scorelist[i]]) < 3:
                                        target = scorelist[i]
                                        break

                        # if opponent is behind
                        else:
                            # and if there is something to point, then point
                            for i in range(11):
                                if (current_turn.team.numbers[i] + temp_dict[scorelist[i]]) == 3 and current_turn.opponent.numbers[i] < 3:
                                    target = scorelist[i]
                                    break
                            # if not, then open next available
                            if target == 0:
                                for i in range(11):
                                    if current_turn.opponent.numbers[i] < 3:
                                        target = scorelist[i]
                                        break

                        # simulate number of darts
                        mean_dict = {'1':0.5,'2':1,'3':1.5,'4':2}
                        sd_dict = {'1':0.25,'2':0.5,'3':0.5,'4':1}
                        value = min(max(round(np.random.normal(mean_dict[self.training_level],sd_dict[self.training_level])),0),3)
                        score_dict = dict(zip([3,2,1],['t','d','s']))
                        if value == 0:
                            pass
                        else:
                            darts.append(score_dict[value]+str(target))
                            temp_dict[target] += value

                    current_turn.darts = list(darts)
                    print("Opponent scored: ",darts,'\n')

                # if not in training mode
                else:
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

                    if self.training_level != '0':
                        self.total_turns += 1

                if current_turn.darts == 'miss':
                    self.next += 1
                    self.printscore()
                    break

                else:
                    if current_turn.player == 'Opponent':
                        pass
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

                        if ((self.training_level != '0') & (current_turn.player != 'Opponent')):
                            self.total_score += numberval

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

                    if ((current_turn.team.score >= current_turn.opponent.score) and (min(current_turn.team.numbers) == 3)):
                        self.over = True
                        self.winner = current_turn.team.displayname
                    break
            except:
                print('ERROR')

    def output(self):
        print("Average Score: ",int(self.total_score/self.total_turns))

class Minnesota(TeamGame):
    def __init__(self, name='1', players=['Player 1', 'Player 2'], scoreboard=[], next=0, over=False, winner='', extrascore=0):
        TeamGame.__init__(self,name,players,scoreboard,next,over,winner,extrascore)
        self.extrascore = extrascore

    def setup(self):
        self.maketeams()

        self.teams[0].numbers = [0] * 10
        self.teams[1].numbers = [0] * 10

        self.scoreboard = pd.DataFrame({'Team 1':self.teams[0].numbers,'Team 2':self.teams[1].numbers},index=['20','19','18','17','16','15','Bull','T','D','Bed'])
        self.scoreboard.columns = [self.teams[0].displayname,self.teams[1].displayname]

    def scoreturn(self):
        current_turn = Turn()

        current_turn.player = self.players[self.next%len(self.players)]
        current_turn.message = current_turn.player + " - you're up!\n"

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

                    if ((current_turn.team.score >= current_turn.opponent.score) and (min(current_turn.team.numbers) == 3)):
                        self.over = True
                        self.winner = current_turn.team.displayname
                    break
            except:
                print('ERROR')

class X01(TeamGame):
    def __init__(self, name='1', players=['Player 1', 'Player 2'], scoreboard=[], next=0, over=False,winner='',startscore=501,
        training_level='0'):
        TeamGame.__init__(self,name,players,scoreboard,next,over,winner,startscore)
        self.startscore = startscore
        self.training_level = training_level
        self.training_player = str(players[0])
        self.game_name = int(startscore)
        self.winner = winner

    def setup(self):

        self.maketeams()

        self.teams[0].score = self.startscore
        self.teams[1].score = self.startscore

        if self.training_level != '0':
            self.history = pd.read_csv('history.csv')
            try:
                temp1 = self.history.groupby(['Game','Level']).agg({'Win':'sum','Loss':'sum'})
                temp1['%'] = (temp1['Win']/(temp1['Win']+temp1['Loss'])).round(2)
                print(temp1,'\n\n')

                temp2 = self.history[self.history['Game']==self.game_name].groupby(['Level']).\
                    agg({'Total Score':'sum','Total Turns':'sum','Darts at Double':'sum','Win':'sum'})
                temp2['Average Score'] = (temp2['Total Score']/temp2['Total Turns']).round(0)
                temp2['Double Rate'] = (temp2['Win']/temp2['Darts at Double']).round(2)
                print(temp2,'\n\n')

            except:
                print("Good luck on your first game!\n")

            self.total_score = 0
            self.total_turns = 0
            self.double_darts = 0

    def scoreturn(self):
        current_turn = Turn()

        current_turn.player = self.players[self.next%len(self.players)]
        current_turn.message = current_turn.player + " - you're up!\n"

        while (True):
            try:
                # establish roles
                if (self.next%2 == 0):
                    current_turn.team = self.teams[0]
                    current_turn.opponent = self.teams[1]
                else:
                    current_turn.team = self.teams[1]
                    current_turn.opponent = self.teams[0]

                # if opponent is up sample from distribution
                if current_turn.player == 'Opponent':
                    score = int(current_turn.team.score)
                    darts = 0
                    singledart = 0
                    for i in range(3):
                        if score > 40:
                            mean_dict = {'1':35,'2':40,'3':45,'4':50}
                            sd_dict = {'1':5,'2':10,'3':10,'4':15}
                            singledart = round(np.random.normal(mean_dict[self.training_level],sd_dict[self.training_level])/3)
                            score = max(score-singledart, 2)
                            darts += int(singledart)
                            continue
                        elif ((score <= 40)&(score%2!=0)):
                            score -= 1
                            darts += 1
                            continue
                        elif ((score <= 40)&(score%2==0)):
                            double_dict = {'1':0.05,'2':0.1,'3':.17,'4':.25}
                            if (np.random.binomial(1,double_dict[self.training_level]) == 1):
                                darts = int(score)
                                break

                    current_turn.darts = int(darts)
                    print('Opponent scored',current_turn.darts)
                    # pass

                # otherwise proceed
                else:
                    current_turn.darts = input(current_turn.message)
                # current_turn.darts = input(current_turn.message)

                    if current_turn.darts == 'exit':
                        self.over = True
                        break

                    ## this is where you can check to see if the user said "undo"
                    if current_turn.darts == 'undo':
                        ## if yes, retrive the old stuff

                        self.next -= (1+self.players.count('Opponent'))
                        self.teams[0].score = int(self.teams[0].backup_score)
                        self.teams[1].score = int(self.teams[1].backup_score)
                        break

                    else:
                        ## update object
                        current_turn.darts = int(current_turn.darts)
                        self.teams[0].backup_score = int(self.teams[0].score)
                        self.teams[1].backup_score = int(self.teams[1].score)

                    if self.training_level != '0':
                        self.total_score += int(current_turn.darts)
                        self.total_turns += 1
                        if self.total_score <= 170:
                            self.double_darts += int(input('How many darts at double?\n'))

                # add current to existing
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
                print('ERROR')

    def printscore(self):
        team1 = self.teams[0]
        team2 = self.teams[1]
        print(team1.displayname+":",team1.space,team1.score)
        print(team2.displayname+":",team2.space,team2.score,'\n')

    def output(self):
        print("Average Score: ",int(self.total_score/self.total_turns))
        print("Double Rate: ",round((self.training_player == self.winner)*1/self.double_darts,2)*100,'%')

class ATW(TeamGame):
    def __init__(self, name='1', players=['Player 1', 'Player 2'], scoreboard=[], next=0, over=False,winner='',startscore='20',training_level='0'):
        TeamGame.__init__(self,name,players,scoreboard,next,over,winner,startscore)
        self.startscore = startscore
        self.training_level = training_level
        self.training_player = str(players[0])
        self.game_name = 'Around The World'
        self.winner = winner

    def setup(self):
        self.maketeams()

        self.teams[0].score = self.startscore
        self.teams[1].score = self.startscore

        if self.training_level != '0':
            self.history = pd.read_csv('history.csv')
            try:
                temp1 = self.history.groupby(['Game','Level']).agg({'Win':'sum','Loss':'sum'})
                temp1['%'] = (temp1['Win']/(temp1['Win']+temp1['Loss'])).round(2)
                print(temp1,'\n\n')

                temp2 = self.history[self.history['Game']==self.game_name].groupby(['Level']).\
                    agg({'Total Score':'sum','Total Turns':'sum','Darts at Double':'sum','Win':'sum'})
                temp2['Average Score'] = (temp2['Total Score']/temp2['Total Turns']).round(0)
                print(temp2,'\n\n')

            except:
                print("Good luck on your first game!\n")

            self.total_score = 0
            self.total_turns = 0
            self.double_darts = 0

    def scoreturn(self):
        current_turn = Turn()

        current_turn.player = self.players[self.next%len(self.players)]
        current_turn.message = current_turn.player + " - you're up!\n"

        while (True):
            try:
                # establish roles
                if (self.next%2 == 0):
                    current_turn.team = self.teams[0]
                    current_turn.opponent = self.teams[1]
                else:
                    current_turn.team = self.teams[1]
                    current_turn.opponent = self.teams[0]

                # if opponent is up sample from distribution
                if current_turn.player == 'Opponent':
                    # simulate turn value from distribution
                    mean_dict = {'1':0.5,'2':1,'3':1.5,'4':2}
                    sd_dict = {'1':0.25,'2':0.5,'3':0.5,'4':1}
                    value = max(round(np.random.normal(mean_dict[self.training_level],sd_dict[self.training_level])),0)
                    bull_dict1 = {'B':0,'BB':-1,'BBB':-2}
                    bull_dict2 = {0:'B',-1:'BB',-2:'BBB'}
                    if current_turn.team.score in bull_dict1.keys():
                        current_turn.team.score = bull_dict1[current_turn.team.score]
                        current_turn.darts = bull_dict2[max(current_turn.team.score - value, -2)]

                    else:
                        current_turn.darts = max(int(current_turn.team.score) - value,-2)
                        if current_turn.darts <= 0:
                                current_turn.darts = bull_dict2[current_turn.darts]

                # otherwise proceed
                else:
                    current_turn.darts = input(current_turn.message)

                    if current_turn.darts == 'exit':
                        self.over = True
                        break

                    ## this is where you can check to see if the user said "undo"
                    if current_turn.darts == 'undo':
                        ## if yes, retrive the old stuff

                        self.next -= (1+self.players.count('Opponent'))
                        self.teams[0].score = str(self.teams[0].backup_score)
                        self.teams[1].score = str(self.teams[1].backup_score)
                        break

                    else:
                        ## update object
                        self.teams[0].backup_score = str(self.teams[0].score)
                        self.teams[1].backup_score = str(self.teams[1].score)

                    if self.training_level != '0':
                        # calculate turn delta
                        bull_dict1 = {'B':0,'BB':-1,'BBB':-2}
                        if current_turn.team.score in bull_dict1.keys():
                            tempval1 = bull_dict1[current_turn.team.score]
                        else:
                            tempval1 = int(current_turn.team.score)
                        if current_turn.darts in bull_dict1.keys():
                            tempval2 = bull_dict1[current_turn.darts]
                        else:
                            tempval2 = int(current_turn.darts)
                        self.total_score += (tempval1 - tempval2)
                        self.total_turns += 1

                # add current to existing
                current_turn.team.score = str(current_turn.darts)

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

                if (current_turn.team.score == 'BBB'):
                    self.over = True
                    self.winner = current_turn.team.displayname
                break
            except:
                print('ERROR')

    def printscore(self):
        team1 = self.teams[0]
        team2 = self.teams[1]
        print(team1.displayname+":",team1.space,team1.score)
        print(team2.displayname+":",team2.space,team2.score,'\n')

    def output(self):
        print("Average Score: ",int(self.total_score/self.total_turns))

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
        if ((self.training_level != '0') & (self.winner != '')):
            # print summary
            self.output()

            # write to csv
            if len(self.history) == 0:
                pd.DataFrame(dict(zip(self.history.columns,
                    [self.training_player,dt.date.today(),self.game_name,self.training_level,
                    (self.training_player == self.winner)*1,(self.training_player != self.winner)*1,
                    self.total_score,self.total_turns,self.double_darts])),index=[len(self.history)]).to_csv('history.csv', index=False)
            else:
                pd.concat([self.history,pd.DataFrame(dict(zip(self.history.columns,
                    [self.training_player,dt.date.today(),self.game_name,self.training_level,
                    (self.training_player == self.winner)*1,(self.training_player != self.winner)*1,
                    self.total_score,self.total_turns,self.double_darts])),index=[len(self.history)])]).to_csv('history.csv', index=False)

    def output(self):
        pass

class Player():
    # define teams
    def __init__(self,name='',score=0, space=0, lives=3):
        self.name = name
        self.score = score
        self.space = space
        self.lives = lives

class Legs(SingleGame):
    def __init__(self, name='1', playernames=[], scoreboard=[], next=0, over=False,winner='', startlegs=5, leadscore = 26, training_level = '0'):
        TeamGame.__init__(self,name,scoreboard,next,over,winner)
        self.playernames = playernames
        self.startlegs = startlegs
        self.leadscore = leadscore
        self.totallives = startlegs * len(playernames)
        self.next = next
        self.backup_leadscore = []
        self.backup_totallives = []
        self.training_level = training_level
        self.training_player = str(playernames[0])
        self.game_name = 'Legs'

    def setup(self):

        self.maketeams()

        for i in range(len(self.players)):
            self.players[i].lives = self.startlegs

        if self.training_level != '0':
            self.history = pd.read_csv('history.csv')
            try:
                temp1 = self.history.groupby(['Game','Level']).agg({'Win':'sum','Loss':'sum'})
                temp1['%'] = (temp1['Win']/(temp1['Win']+temp1['Loss'])).round(2)
                print(temp1,'\n\n')

                temp2 = self.history[self.history['Game']==self.game_name].groupby(['Level']).agg({'Total Score':'sum','Total Turns':'sum'})
                temp2['Average Score'] = (temp2['Total Score']/temp2['Total Turns']).round(0)
                print(temp2,'\n\n')

            except:
                print("Good luck on your first game!\n")

            self.total_score = 0
            self.total_turns = 0
            self.double_darts = 0


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
                        # if opponent is up sample from distribution
                        if current_turn.player.name == 'Opponent':
                            mean_dict = {'1':35,'2':40,'3':45,'4':50}
                            sd_dict = {'1':5,'2':10,'3':10,'4':15}
                            current_turn.darts = round(np.random.normal(mean_dict[self.training_level],sd_dict[self.training_level]))
                            print('Opponent scored',current_turn.darts,'\n')

                        # otherwise proceed
                        else:
                            current_turn.darts = input(current_turn.message)

                            if current_turn.darts == 'exit':
                                self.over = True
                                break

                            if current_turn.darts == 'undo':
                                ## if yes, retrive the old stuff
                                self.next -= (1+self.playernames.count('Opponent'))
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

                            if self.training_level != '0':
                                self.total_score += int(current_turn.darts)
                                self.total_turns += 1


                        if current_turn.darts > self.leadscore:
                            self.leadscore = int(current_turn.darts)
                            self.next += 1
                            self.printscore()
                            break

                        else:
                            self.next += 1
                            self.leadscore = 26
                            # these could be a memory assignment error working correctly
                            current_turn.player.lives -= 1
                            self.totallives -= 1
                            self.printscore()
                            break
                    except:
                        print('ERROR')

    def printscore(self):
        for i in range(len(self.players)):
            print(self.players[i].name+":",self.players[i].space,self.players[i].lives)
        print()

    def output(self):
        print("Average Score: ",int(self.total_score/self.total_turns))

class Follow(SingleGame):
    def __init__(self, name='1', playernames=[], scoreboard=[], next=0, over=False,winner='', startlegs=5, leadscore = 'Open',leader=[], training_level='0'):
        TeamGame.__init__(self,name,scoreboard,next,over,winner)
        self.playernames = playernames
        self.startlegs = startlegs
        self.leadscore = leadscore
        self.totallives = startlegs * len(playernames)
        self.leader = leader
        self.next = next
        self.training_level = training_level
        self.training_player = str(playernames[0])
        self.game_name = 'Follow The Leader'

    def setup(self):
        self.maketeams()

        for i in range(len(self.players)):
            self.players[i].lives = self.startlegs

        if self.training_level != '0':
            self.history = pd.read_csv('history.csv')
            try:
                temp1 = self.history.groupby(['Game','Level']).agg({'Win':'sum','Loss':'sum'})
                temp1['%'] = (temp1['Win']/(temp1['Win']+temp1['Loss'])).round(2)
                print(temp1,'\n\n')

            except:
                print("Good luck on your first game!\n")

            self.total_score = 0
            self.total_turns = 0
            self.double_darts = 0

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
                        # if opponent is up sample from distribution
                        if current_turn.player.name == 'Opponent':
                            # defense probabilty dictionary - three dart probability of hitting t, d, s
                            d_triple_dict = {'1':(1-(1-0.04)**3),'2':(1-(1-0.08)**3),'3':(1-(1-.15)**3),'4':(1-(1-.20)**3)}
                            d_double_dict = {'1':(1-(1-0.04)**3),'2':(1-(1-0.08)**3),'3':(1-(1-.15)**3),'4':(1-(1-.20)**3)}
                            d_single_dict = {'1':(1-(1-0.04)**3),'2':(1-(1-0.08)**3),'3':(1-(1-.15)**3),'4':(1-(1-.20)**3)}

                            o_triple_dict = {'1':0.04,'2':0.08,'3':.15,'4':.20}
                            o_double_dict = {'1':0.04,'2':0.08,'3':.15,'4':.20}
                            o_single_dict = {'1':0.25,'2':0.40,'3':.55,'4':.70}

                            print(self.leadscore)

                            if self.leadscore != 'Open':
                                current_turn.darts = 'miss'
                                if self.leadscore[0] == 't':
                                    if (np.random.binomial(1,d_triple_dict[self.training_level]) == 1):
                                        current_turn.darts = 'hit'
                                elif self.leadscore[0] == 'd':
                                    if (np.random.binomial(1,d_double_dict[self.training_level]) == 1):
                                        current_turn.darts = 'hit'
                                elif self.leadscore[0] == 's':
                                    if (np.random.binomial(1,d_single_dict[self.training_level]) == 1):
                                        current_turn.darts = 'hit'

                            if ((current_turn.darts == 'hit') | (self.leadscore == 'Open')):
                                if (np.random.binomial(1,d_triple_dict[self.training_level]) == 1):
                                        # triple with random number
                                        current_turn.darts = 't'+str(random.randint(1,20))
                                elif (np.random.binomial(1,d_double_dict[self.training_level]) == 1):
                                    # double with random number
                                    current_turn.darts = 'd'+str(random.randint(1,20))
                                else:
                                    # single with random number
                                    current_turn.darts = 's'+str(random.randint(1,20))

                        else:
                            current_turn.darts = input(current_turn.message)

                            if current_turn.darts == 'exit':
                                self.over = True
                                break

                            if current_turn.darts == 'undo':
                                ## if yes, retrive the old stuff
                                self.next -= (1+self.playernames.count('Opponent'))
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
                        print('ERROR')

    def printscore(self):
        for i in range(len(self.players)):
            print(self.players[i].name+":",self.players[i].space,self.players[i].lives)
        print()

class Golf(SingleGame):
    def __init__(self, name='1', playernames=[], scoreboard=[], next=0, over=False,winner='', holes=18, leadscore = 'Open',leader=[], hole=1, training_level='0'):
        TeamGame.__init__(self,name,scoreboard,next,over,winner)
        self.playernames = playernames
        self.leadscore = leadscore
        self.totalturns = 1
        self.winner = winner
        self.hole = hole
        self.next = next
        self.overtime = False
        self.holes = holes
        self.training_level = training_level
        self.training_player = str(playernames[0])
        self.game_name = 'Golf'

    def setup(self):
        self.maketeams()

        if self.training_level != '0':
            self.history = pd.read_csv('history.csv')
            try:
                temp1 = self.history.groupby(['Game','Level']).agg({'Win':'sum','Loss':'sum'})
                temp1['%'] = (temp1['Win']/(temp1['Win']+temp1['Loss'])).round(2)
                print(temp1,'\n\n')

                temp2 = self.history[self.history['Game']=='Legs'].groupby(['Level']).agg({'Total Score':'sum','Total Turns':'sum'})
                temp2['Average Score'] = (temp2['Total Score']/temp2['Total Turns']).round(0)
                print(temp2,'\n\n')

            except:
                print("Good luck on your first game!\n")

            self.total_score = 0
            self.total_turns = 0
            self.double_darts = 0

    def scoreturn(self):
        current_turn = Turn()

        current_turn.player = self.players[self.next%len(self.players)]

        current_turn.message = current_turn.player.name + " - you're up!\n"

        while (True):
            try:
                # if opponent is up sample from distribution
                if current_turn.player.name == 'Opponent':
                    mean_dict = {'1':4,'2':3.5,'3':3,'4':2.5}
                    sd_dict = {'1':1,'2':1,'3':1,'4':1}
                    current_turn.darts = max(min(round(np.random.normal(mean_dict[self.training_level],sd_dict[self.training_level])),5),1)
                    print('Opponent scored',current_turn.darts,'\n')

                # otherwise proceed
                else:
                    current_turn.darts = input(current_turn.message)

                    if current_turn.darts == 'exit':
                        self.over = True
                        break

                    if current_turn.darts == 'undo':
                        # restore backups
                        self.next -= (1+self.playernames.count('Opponent'))
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

                        if self.training_level != '0':
                            self.total_score += int(current_turn.darts)
                            self.total_turns += 1

                self.totalturns += 1
                if (self.totalturns%len(self.playernames) == 1):
                    self.hole += 1

                current_turn.player.score += current_turn.darts
                self.printscore()

                self.players[self.next%len(self.players)] = current_turn.player
                self.next += 1
                break

            except:
                print('ERROR')

        # check if it's overtime
        if ((self.hole >= (self.holes + 1))&(self.totalturns%len(self.playernames) == 1)):
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

    def output(self):
        print("Average Score: ",int(self.total_score/self.total_turns))

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
                    print('ERROR')
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
                print('ERROR')

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
            self.backup_dartboard = pd.DataFrame({"Player":list(temp_dict_name.values()),"Lives":list(temp_dict_value.values())},index=list(temp_dict_name.keys()))

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

                    if current_turn.darts == 'undo':
                        self.next -= 1
                        self.dartboard = pd.DataFrame(self.backup_dartboard)
                        break

                    else:
                        self.backup_scoreboard = pd.DataFrame(self.backup_dartboard)

                    if current_turn.darts == 'miss':
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
                                scratchval += int(numberval)

                        if scratch == True:
                            bringback = input("Scratch - which darts?\n").split(',')

                            for dart in bringback:
                                letterval = dart[0]
                                numberval = score_dict[letterval]
                                dartnum = int(dart[1:])
                                temp_frame.loc[dartnum,'Lives'] += numberval
                                if temp_frame.loc[dartnum]['Lives'] > 3:
                                    temp_frame.loc[dartnum,'Lives'] = 3

                        self.dartboard = temp_frame.copy()

                        self.next += 1
                        self.printscore()
                        break

                except:
                    print('ERROR')

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

    if len(start_game.players) == 1:
        start_game.training = True
        start_game.players.append('Opponent')
        start_game.training_level = input('\nWhat level would you like to play:\n1. Beginner\n2. Intermediate\n3. Advanced\n4. Expert\n')
        start_game.name = input('\nWhat game would you like to play:\n1. Legs\n2. Follow The Leader\n3. Golf\n4. X01\n5. Cricket\n6. Spanish\n7. Around The World\n')

        # Launch legs
        if start_game.name == '1':
            #instantiate game
            start_game.startscore = int(input('\nHow many legs to start?\n'))
            current_game = Legs(name=start_game.name, playernames=start_game.players, startlegs=start_game.startscore, training_level=start_game.training_level)
            current_game.rungame()

        # Follow the leader
        if start_game.name == '2':
            #instantiate game
            start_game.startscore = int(input('\nHow many legs to start?\n'))
            current_game = Follow(name=start_game.name, playernames=start_game.players, startlegs=start_game.startscore, training_level=start_game.training_level)
            current_game.rungame()

        # Golf
        if start_game.name == '3':
            #instantiate game
            start_game.startscore = int(input('\nHow many holes?\n'))
            current_game = Golf(name=start_game.name, playernames=start_game.players, holes=start_game.startscore, training_level=start_game.training_level)
            current_game.rungame()

        # Launch X01
        if start_game.name == '4':
            start_game.startscore = int(input('What starting score do you want?\n'))
            #instantiate game
            current_game = X01(name=start_game.name, players=start_game.players, startscore=start_game.startscore,
                training_level=start_game.training_level)
            current_game.rungame()

        if start_game.name == '5':
            #instantiate game
            current_game = Cricket(name=start_game.name, players=start_game.players, training_level=start_game.training_level)
            current_game.rungame()

        # Launch spanish
        if start_game.name == '6':
            #instantiate game
            current_game = Spanish(name=start_game.name, players=start_game.players, training_level=start_game.training_level)
            current_game.rungame()

        # Launch ATW
        if start_game.name == '7':
            #instantiate game
            current_game = ATW(name=start_game.name, players=start_game.players, training_level=start_game.training_level)
            current_game.rungame()

    elif len(start_game.players)%2==1:
        #odd games
        start_game.name = input('\nWhat game would you like to play:\n\n1. Legs\n2. Follow the Leader\n3. Golf\n4. Killer\n5. Cutthroat Cricket\n6. Cutthroat\n')

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

    else:
        # all games
        start_game.name = input('''\nWhat game would you like to play:\n\nIndividual Games:\n1.  Legs\n2.  Follow the Leader\n3.  Golf\n4.  Killer\n5.  Cutthroat Cricket\n6.  Cutthroat\n\nTeam Games:\n7.  Cricket\n8.  Spanish\n9.  Minnesota\n10. X01\n11. Around The World\n''')

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

        if start_game.name == '7':
            #instantiate game
            current_game = Cricket(name=start_game.name, players=start_game.players)
            current_game.rungame()

        # Launch spanish
        if start_game.name == '8':
            #instantiate game
            current_game = Spanish(name=start_game.name, players=start_game.players)
            current_game.rungame()

        # Launch minnesota
        if start_game.name == '9':
            #instantiate game
            current_game = Minnesota(name=start_game.name, players=start_game.players)
            current_game.rungame()

        # Launch X01
        if start_game.name == '10':
            start_game.startscore = int(input('What starting score do you want?\n'))
            #instantiate game
            current_game = X01(name=start_game.name, players=start_game.players, startscore=start_game.startscore)
            current_game.rungame()

        # Launch ATW
        if start_game.name == '11':
            #instantiate game
            current_game = ATW(name=start_game.name, players=start_game.players)
            current_game.rungame()

# better understand need for default parameters in constructor methods for subclasses
# there may be some unintentional memory assignments that are not causing problems

main()
