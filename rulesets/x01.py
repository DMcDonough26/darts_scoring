import numpy as np
import pandas as pd
from scipy.stats import binom_test

from game_mechanics import TeamGame, Turn

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
                temp1['p_val'] = temp1.apply(lambda y: binom_test(x=y['Win'],n=(y['Win']+y['Loss']),p=0.5,alternative='greater').round(2),axis=1)
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
                        if current_turn.team.score <= 170:
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
