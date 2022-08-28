import pandas as pd

from game_mechanics import SingleGame, TeamGame, Turn


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
