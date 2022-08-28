import pandas as pd
import numpy as np

from game_mechanics import TeamGame, Turn

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
                temp2['Average Score'] = (temp2['Total Score']/temp2['Total Turns']).round(1)
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
        print("Average Score: ",round(self.total_score/self.total_turns,1))
