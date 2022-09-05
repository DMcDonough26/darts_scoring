import numpy as np
import pandas as pd

from game_mechanics import TeamGame, Turn

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
        print("Average Score: ",round(self.total_score/self.total_turns,2))
