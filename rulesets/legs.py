import numpy as np
import pandas as pd
from scipy.stats import binom_test

from game_mechanics import SingleGame, TeamGame, Turn

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
                temp1['p_val'] = temp1.apply(lambda y: binom_test(x=y['Win'],n=(y['Win']+y['Loss']),p=0.5,alternative='greater').round(2),axis=1)
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
