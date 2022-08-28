import random

import pandas as pd

from game_mechanics import SingleGame, TeamGame, Turn

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
