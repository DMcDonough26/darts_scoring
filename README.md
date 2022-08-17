# darts_scoring
Python program designed to score various darts games from the command line

During COVID, some buddies and I began playing darts over zoom. I created this program so that I should share my screen and we could easily score various dart games.

** 2/1/2022 I've added a play-against-the-computer mode where you can specify the desired level of opposition for Legs, Golf, X01, and Cricket

** August 2022 - Streamlined menu, added undo functionality to training mode and cutthroat, fixed bug in multiple mode for games eligible for training,
added error message or exception handling, enhanced scratch bringback functionality for cutthroat.

## How to use
The program is admittedly not super intuitive, so I've included some detailed instructions on how to use

-- At startup, enter player names with comma and space separating
<br> -- Example:
<br> -- Player1, Player2
<br> -- Teams are randomly assigned for games so no need to worry about input order
<br> -- If only one player is provided, you will then be prompted to specify the level of computer opponent you wish to play

## Cricket
<br> -- darts are scored with a lowercase 't','d','s' and then the number scored and a comma separating darts
<br> -- here is an example of triple 20, 19, 18 in the same turn
<br> t20,t19,t18

<br> -- if an error is thrown the user will be reprompted to enter the darts
<br> -- if you accidently score the wrong darts you can type "undo" and the previous turn will be restored
<br> -- if you miss all three darts you can type "miss" to advance to the next turn
<br> -- to exit the game you can type "exit"

## Spanish
<br> -- same instructions as cricket

## Minnesota
<br> -- same instructions as cricket
<br> -- after entering your darts you will be prompted for an extra score
<br> -- this is providing you the option to record points scored on a closed triple, double or bed
<br> -- for example, let's say I've closed 20s as has my opponent, but I've also closed beds
<br> -- if I hit three single 20s I would score my turn as "miss" and then enter 60 as the extra score to be scored

## X01
<br> -- simply enter the number of points scored on that turn

## Legs
<br> -- simply enter the number of points scored on that turn

## Follow the leader
<br> -- darts are scored with a lowercase 't','d','s' and then the number scored and a comma separating darts
<br> -- if the dart is missed type "miss", if it is hit then input the new dart to hit
<br> -- for example if the dart to hit is single 20, and I hit this dart and then a double 5, I would simply enter d5

## Golf
<br> -- simply enter the number of points scored for that hole

## Killer
<br> -- enter comma separated inputs with the following order:
<br> -- number of own darts hit, player targeted, number of their darts hit
<br> -- this can be repeated for multiple other players targeted
<br> -- for example let's say I have 2 lives and each of my opponents has 1 life left
<br> -- I could win the game with the following sequence:
<br> -- 1,Player 2,1,Player 3,1

## Cutthroat cricket
<br> -- same instructions as cricket
<br> -- for those unfamiliar this is a multi-player version of the game where the goal is to have the lowest number of points
<br> -- for example: if I've closed 20s and no one else has and I hit a single 20, then my score remains the same but all of my opponents have their scores increased by 20

## Cutthroat
<br> -- this game is modeled off of the multi-player pool game cutthroat
<br> -- entering your darts follows the same approach as cricket
<br> -- the goal is to hit other player's numbers without hitting your own
<br> -- if you do hit your own number you will have scratched, and your opponents will each get to bring that many darts back
<br> -- currently you can only bring darts back on a single numbers per person, but I may expand the functionality so you can add scratch darts back to multiple numbers
<br> -- for example if an opponent scratches hitting a triple being able to bring back 1 live on three separate numbers rather than 3 on a single number

## Planned future enhancements
<br> -- moving this program from the command line to the browser, and then potentially hosting on a server and allowing clients to access directly rather than through screen share
<br> -- adding user profiles and history, so that statistics can be tracked across sessions and league-style play can be supported
<br> -- adding an AI-based training mode where opponent play is simulated and is adaptive to the user's performance
