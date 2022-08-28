from game_mechanics import TeamGame
from rulesets.atw import ATW
from rulesets.cricket import Cricket
from rulesets.cutthroat import Cutthroat
from rulesets.cutthroat_cricket import CutthroatCricket
from rulesets.follow import Follow
from rulesets.golf import Golf
from rulesets.killer import Killer
from rulesets.legs import Legs
from rulesets.minnesota import Minnesota
from rulesets.spanish import Spanish
from rulesets.x01 import X01


def main():
    #instantiate game
    start_game = TeamGame()

    # collect player names
    start_game.players = input('Hello, who is playing tonight?\n')
    start_game.players = start_game.players.split(', ')

    if len(start_game.players) == 1:
        start_game.training = True
        start_game.players.append('Opponent')
        start_game.training_level = input('\nWhat level would you like to play:\n1. Beginner\n2. Intermediate\n3. Advanced\n4. Expert\n')
        start_game.name = input('\nWhat game would you like to play:\n1. Legs\n2. Follow The Leader\n3. Golf\n4. X01\n5. Cricket\n6. Spanish\n7. Around The World\n')

        # Launch legs
        if start_game.name == '1':
            #instantiate game
            start_game.startscore = int(input('\nHow many legs to start?\n'))
            current_game = Legs(name=start_game.name, playernames=start_game.players, startlegs=start_game.startscore, training_level=start_game.training_level)
            current_game.rungame()

        # Follow the leader
        if start_game.name == '2':
            #instantiate game
            start_game.startscore = int(input('\nHow many legs to start?\n'))
            current_game = Follow(name=start_game.name, playernames=start_game.players, startlegs=start_game.startscore, training_level=start_game.training_level)
            current_game.rungame()

        # Golf
        if start_game.name == '3':
            #instantiate game
            start_game.startscore = int(input('\nHow many holes?\n'))
            current_game = Golf(name=start_game.name, playernames=start_game.players, holes=start_game.startscore, training_level=start_game.training_level)
            current_game.rungame()

        # Launch X01
        if start_game.name == '4':
            start_game.startscore = int(input('What starting score do you want?\n'))
            #instantiate game
            current_game = X01(name=start_game.name, players=start_game.players, startscore=start_game.startscore,
                training_level=start_game.training_level)
            current_game.rungame()

        if start_game.name == '5':
            #instantiate game
            current_game = Cricket(name=start_game.name, players=start_game.players, training_level=start_game.training_level)
            current_game.rungame()

        # Launch spanish
        if start_game.name == '6':
            #instantiate game
            current_game = Spanish(name=start_game.name, players=start_game.players, training_level=start_game.training_level)
            current_game.rungame()

        # Launch ATW
        if start_game.name == '7':
            #instantiate game
            current_game = ATW(name=start_game.name, players=start_game.players, training_level=start_game.training_level)
            current_game.rungame()

    elif len(start_game.players)%2==1:
        #odd games
        start_game.name = input('\nWhat game would you like to play:\n\n1. Legs\n2. Follow the Leader\n3. Golf\n4. Killer\n5. Cutthroat Cricket\n6. Cutthroat\n')

        # Launch legs
        if start_game.name == '1':
            #instantiate game
            start_game.startscore = int(input('\nHow many legs to start?\n'))
            current_game = Legs(name=start_game.name, playernames=start_game.players, startlegs=start_game.startscore)
            current_game.rungame()

        # Follow the leader
        if start_game.name == '2':
            #instantiate game
            start_game.startscore = int(input('\nHow many legs to start?\n'))
            current_game = Follow(name=start_game.name, playernames=start_game.players, startlegs=start_game.startscore)
            current_game.rungame()

        # Golf
        if start_game.name == '3':
            #instantiate game
            start_game.startscore = int(input('\nHow many holes?\n'))
            current_game = Golf(name=start_game.name, playernames=start_game.players, holes=start_game.startscore)
            current_game.rungame()

        # Killer
        if start_game.name == '4':
            #instantiate game
            current_game = Killer(name=start_game.name, playernames=start_game.players)
            current_game.rungame()

        # CutthroatCricket
        if start_game.name == '5':
            #instantiate game
            current_game = CutthroatCricket(name=start_game.name, playernames=start_game.players)
            current_game.rungame()

        # Cutthroat
        if start_game.name == '6':
            #instantiate game
            current_game = Cutthroat(name=start_game.name, playernames=start_game.players)
            current_game.rungame()

    else:
        # all games
        start_game.name = input('''\nWhat game would you like to play:\n\nIndividual Games:\n1.  Legs\n2.  Follow the Leader\n3.  Golf\n4.  Killer\n5.  Cutthroat Cricket\n6.  Cutthroat\n\nTeam Games:\n7.  Cricket\n8.  Spanish\n9.  Minnesota\n10. X01\n11. Around The World\n''')

        # Launch legs
        if start_game.name == '1':
            #instantiate game
            start_game.startscore = int(input('\nHow many legs to start?\n'))
            current_game = Legs(name=start_game.name, playernames=start_game.players, startlegs=start_game.startscore)
            current_game.rungame()

        # Follow the leader
        if start_game.name == '2':
            #instantiate game
            start_game.startscore = int(input('\nHow many legs to start?\n'))
            current_game = Follow(name=start_game.name, playernames=start_game.players, startlegs=start_game.startscore)
            current_game.rungame()

        # Golf
        if start_game.name == '3':
            #instantiate game
            start_game.startscore = int(input('\nHow many holes?\n'))
            current_game = Golf(name=start_game.name, playernames=start_game.players, holes=start_game.startscore)
            current_game.rungame()

        # Killer
        if start_game.name == '4':
            #instantiate game
            current_game = Killer(name=start_game.name, playernames=start_game.players)
            current_game.rungame()

        # CutthroatCricket
        if start_game.name == '5':
            #instantiate game
            current_game = CutthroatCricket(name=start_game.name, playernames=start_game.players)
            current_game.rungame()

        # Cutthroat
        if start_game.name == '6':
            #instantiate game
            current_game = Cutthroat(name=start_game.name, playernames=start_game.players)
            current_game.rungame()

        if start_game.name == '7':
            #instantiate game
            current_game = Cricket(name=start_game.name, players=start_game.players)
            current_game.rungame()

        # Launch spanish
        if start_game.name == '8':
            #instantiate game
            current_game = Spanish(name=start_game.name, players=start_game.players)
            current_game.rungame()

        # Launch minnesota
        if start_game.name == '9':
            #instantiate game
            current_game = Minnesota(name=start_game.name, players=start_game.players)
            current_game.rungame()

        # Launch X01
        if start_game.name == '10':
            start_game.startscore = int(input('What starting score do you want?\n'))
            #instantiate game
            current_game = X01(name=start_game.name, players=start_game.players, startscore=start_game.startscore)
            current_game.rungame()

        # Launch ATW
        if start_game.name == '11':
            #instantiate game
            current_game = ATW(name=start_game.name, players=start_game.players)
            current_game.rungame()

# better understand need for default parameters in constructor methods for subclasses
# there may be some unintentional memory assignments that are not causing problems

main()
