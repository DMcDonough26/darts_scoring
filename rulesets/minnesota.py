import pandas as pd

from game_mechanics import TeamGame, Turn

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

                    if ((current_turn.team.score > current_turn.opponent.score) and (min(current_turn.team.numbers) == 3)):
                        self.over = True
                        self.winner = current_turn.team.displayname
                    break
            except:
                print('ERROR')
