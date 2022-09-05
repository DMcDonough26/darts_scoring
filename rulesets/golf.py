import numpy as np
import pandas as pd

from game_mechanics import SingleGame, TeamGame, Turn

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

                temp2 = self.history[self.history['Game']==self.game_name].groupby(['Level']).agg({'Total Score':'sum','Total Turns':'sum'})
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
        print("Average Score: ",round(self.total_score/self.total_turns,1))
