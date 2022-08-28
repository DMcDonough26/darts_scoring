import random

import numpy as np
import pandas as pd

from game_mechanics import SingleGame, TeamGame, Turn

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
