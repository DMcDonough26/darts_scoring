import random

import pandas as pd

from game_mechanics import SingleGame, TeamGame, Turn


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
    