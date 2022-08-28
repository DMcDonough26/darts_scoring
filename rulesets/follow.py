from game_mechanics import SingleGame, TeamGame, Turn

class Follow(SingleGame):
    def __init__(self, name='1', playernames=[], scoreboard=[], next=0, over=False,winner='', startlegs=5, leadscore = 'Open',leader=[]):
        TeamGame.__init__(self,name,scoreboard,next,over,winner)
        self.playernames = playernames
        self.startlegs = startlegs
        self.leadscore = leadscore
        self.totallives = startlegs * len(playernames)
        self.leader = leader
        self.next = next

    def setup(self):
        self.maketeams()

        for i in range(len(self.players)):
            self.players[i].lives = self.startlegs

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
                        current_turn.darts = input(current_turn.message)

                        if current_turn.darts == 'exit':
                            self.over = True
                            break

                        if current_turn.darts == 'undo':
                            ## if yes, retrive the old stuff
                            self.next -= 1
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
                            current_turn.darts = current_turn.darts

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
