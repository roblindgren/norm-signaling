## Created: 2015/10/17
## Revised: 2017/04/15
## Author: Robert Lindgren
## Filename: CodeSample-RobertLindgren.py

## Description:
##
## This is an agent-based simulation of the plural signaling game outlined in 
## "An Evolutionary Signaling Model of Social Norms" (Lindgren 2015). A population of players 
## is generated according to the model parameters, pairs of players are 
## assigned to play one another in one of two subgames (A or B) for 1000
## rounds, and the data is recorded to the folder containing this Python file 
## for later analysis. Typically, we would run the simulation 1000+ times, but 
## for this code sample I set the parameters so that the game would only run once,
## therefore creating only one data file. 
##
## This version of the simulation will test weight and PropPlayingA1 variables, 
## while holding all other variables constant. weight is a multiplier for the 
## Game B payoff matrix. If Game A has payoffs of 3, weight=2 will create a 
## Game B matrix with payoffs of 6. It will set a weight and then loop through 20 
## different PropPlayingA1 values, between 0 and 0.45. Then it will increment 
## through different weight values, 1 through 100, looping through PropPlayingA1 
## values each time.
##
## This agent-based simulation is modeled after "Simulating Evolutionary Games: 
## A Python-Based Introduction" (Isaac 2008).

from __future__ import division
import random
import pickle

__author__ = 'Robert Lindgren'

## DECLARE GLOBAL VARIABLES

POPSIZE = 1000 ## Number of players in population
NUMROUNDS = 1000 ## Number of rounds per game
MAXMULT = 1 ## Maximum multiplier of PropTypeA1
MAXWEIGHT = 1 ## Largest multiplier of Game B payoffs
PROPTYPE1 = 0.5 #Proportion of Type 1 players in population
PROPTYPE2 = 1 - PROPTYPE1 #Proportion of Type 2 players in population


## BEGIN CLASS DEFINITIONS

class SimplePlayer:  
    """Defines our basic player."""
    
    def __init__(self, z, playerlistType1, playerlistType2, weight, roundAgg):
        """Initializes players.
        
        Argument(s): 
            z -- integer, player index.
            playerlistType1 -- list, of Type1 player indices.
            playerlistType2 -- list, of Type2 player indices.
            weight -- integer, multiplies Game B payoffs.
            roundAgg -- dict, key-value pairs that represent the state of the population in current round.  
            
        Return(s): 
            none.
        """
        
        global PROPTYPE1
        
        self.playerindex = z
        self.playertype = self.getplayertype() ## Assigns a playertype of 1 or 2
        self.actionA = self.getactionA(roundAgg) ## Assigns an intial Game A action of 1 or 2
        self.actionB = self.getactionB(roundAgg) ## Assigns an intial Game B action of 1 or 2
        self.numGameA = 0 ## This counts how many A Games the player has played
        self.numGameB = 0 ## This counts how many B Games the player has played
        self.lastActionA = self.actionA
        self.lastActionB = self.actionB
        self.lastGameAPay = random.uniform(0, 3)
        self.lastGameBPay = random.uniform(0, (3*weight))
        self.lastOppGameA = random.uniform(0, 3)
        self.lastOppGameB = random.uniform(0, (3*weight))
        self.lastOppGameBLastActionA = random.randint(1,2)
        if self.playertype == 1:
            playerlistType1.append(self.playerindex)
        else:
            playerlistType2.append(self.playerindex)

    def getplayertype(self):
        """
        Randomly chooses a player type with probability Type1.
        
        Argument(s): 
            none.  
            
        Return(s): 
            integer, 1 if player is Type 1 or 2 if player is Type 2.
        """
        
        global PROPTYPE1
        
        if random.uniform(0,1) < PROPTYPE1:  ## If a randomly drawn number between 0 and 1 is less than PROPTYPE1, playertype returns 1 to indicate the player is Type 1
            return (1)
        else:
            return (2)  ## If the random number is greater than PROPTYPE1, playertype returns 2 to indicate player is of type 2
    
    def getactionA(self, roundAgg):
        """
        Randomly chooses an initial Game A action based on the input parameters.
            
        Argument(s): 
            roundAgg -- dict, key-value pairs that represent the state of the population in current round.
            
        Return(s): 
            integer, 1 for action A1 or 2 for action A2.
        """
                
        Type1PlayingA1=roundAgg['Type1PlayingA1']
        Type2PlayingA1=roundAgg['Type2PlayingA1']
        
        if self.playertype == 1:
            if random.uniform(0,1) < Type1PlayingA1:  ## If a randomly drawn number between 0 and 1 is less than Type1PlayingA1, actionA returns 1
                return (1)
            else:
                return (2)  ## If the random number is greater than PROPTYPE1, playertype returns 2 to indicate player is of type 2
        if self.playertype == 2:
            if random.uniform(0,1) < Type2PlayingA1:  ## If a randomly drawn number between 0 and 1 is less than Type2PlayingA1, actionA returns 1
                return (1)
            else:
                return (2)  ## If the random number is greater than PROPTYPE1, playertype returns 2 to indicate player is of type 2
    
    def getactionB(self, roundAgg):
        """
        Randomly chooses an initial Game B action given the input parameters.
        
        Argument(s): 
            roundAgg -- dict, key-value pairs that represent the state of the population in current round.
            
        Return(s): 
            integer, 1 for action B1 or 2 for action B2.
        """
                
        Type1PlayingB1=roundAgg['Type1PlayingB1'] 
        Type2PlayingB1=roundAgg['Type2PlayingB1']
        
        if self.playertype == 1:
            if random.uniform(0,1) < Type1PlayingB1:  ## If a randomly drawn number between 0 and 1 is less than Type1PlayingB1, actionB returns 1
                return (1)
            return (2)  ## If the random number is greater than PROPTYPE1, playertype returns 2 to indicate player is of type 2
        if self.playertype == 2:
            if random.uniform(0,1) < Type2PlayingB1:  ## If a randomly drawn number between 0 and 1 is less than Type2PlayingB1, actionB returns 1
                return (1)
            return (2)  ## If the random number is greater than PROPTYPE1, playertype returns 2 to indicate player is of type 2

    
    def moveA(self, opp_index, GameA_PAYOFFMAT, GameB1_PAYOFFMAT, GameB2_PAYOFFMAT, playerlistType1, 
              playerlistType2, playerdict, roundAgg):
        """
        Determines an action in Game A.
        
        Argument(s): 
            opp_index -- integer, opponent's player index.
            GameA_PAYOFFMAT -- dict, payoff matrix for Game A, all players.
            GameB1_PAYOFFMAT -- dict, payoff matrix for Game B, Type 1.
            GameB2_PAYOFFMAT -- dict, payoff matrix for Game B, Type 2.
            playerlistType1 -- list, of Type 1 player indices.
            playerlistType2 -- list, of Type 2 player indices.
            playerdict -- dict, of players
            roundAgg -- dict, key-value pairs that represent the state of the population in current round.
            
        Return(s): 
            integer, 1 for action B1 or 2 for action B2.
        """
                        
        PropPlayingA1=roundAgg['PropPlayingA1']
        PropPlayingA2=roundAgg['PropPlayingA2']
        proptype1otherA1playB1=roundAgg['proptype1otherA1playB1']
        proptype1otherA1playB2=roundAgg['proptype1otherA1playB2']
        proptype1otherA2playB1=roundAgg['proptype1otherA2playB1']
        proptype1otherA2playB2=roundAgg['proptype1otherA2playB2']
        proptype2otherA1playB1=roundAgg['proptype2otherA1playB1']
        proptype2otherA1playB2=roundAgg['proptype2otherA1playB2']
        proptype2otherA2playB1=roundAgg['proptype2otherA2playB1']
        proptype2otherA2playB2=roundAgg['proptype2otherA2playB2']
        
        if self.numGameA == 0:
            self.numGameA = self.numGameA + 1
            if self.playertype == 1:
                local_payoffmat = GameB1_PAYOFFMAT
            else:
                local_payoffmat = GameB2_PAYOFFMAT
            if (self.lastActionB == 1):
                indirectPayA1 = PROPTYPE1*(proptype1otherA1playB1*local_payoffmat['B1B1']+proptype1otherA1playB2*local_payoffmat['B1B2'])+PROPTYPE2*(proptype2otherA1playB1*local_payoffmat['B1B1']+proptype2otherA1playB2*local_payoffmat['B1B2'])
                indirectPayA2 = PROPTYPE1*(proptype1otherA2playB1*local_payoffmat['B1B1']+proptype1otherA2playB2*local_payoffmat['B1B2'])+PROPTYPE2*(proptype2otherA2playB1*local_payoffmat['B1B1']+proptype2otherA2playB2*local_payoffmat['B1B2'])
            elif (self.lastActionB == 2):
                indirectPayA1 = PROPTYPE1*(proptype1otherA1playB1*local_payoffmat['B2B1']+proptype1otherA1playB2*local_payoffmat['B2B2'])+PROPTYPE2*(proptype2otherA1playB1*local_payoffmat['B2B1']+proptype2otherA1playB2*local_payoffmat['B2B2'])
                indirectPayA2 = PROPTYPE1*(proptype1otherA2playB1*local_payoffmat['B2B1']+proptype1otherA2playB2*local_payoffmat['B2B2'])+PROPTYPE2*(proptype2otherA2playB1*local_payoffmat['B2B1']+proptype2otherA2playB2*local_payoffmat['B2B2'])
            evfora1 = PropPlayingA1*GameA_PAYOFFMAT.get('A1A1') + PropPlayingA2*GameA_PAYOFFMAT.get('A1A2') + indirectPayA1
            evfora2 = PropPlayingA1*GameA_PAYOFFMAT.get('A2A1') + PropPlayingA2*GameA_PAYOFFMAT.get('A2A2') + indirectPayA2
            EVdictA = {1: evfora1, 2: evfora2}
            actionA = max(EVdictA, key=EVdictA.get)
            self.lastActionA = actionA
            self.lastGameAPay = EVdictA.get(actionA)
            self.lastOppGameA = opp_index
            return(actionA)
        else:
            self.numGameA = self.numGameA + 1    
            
            ## Gets revision probability   
            MyAction = self.lastActionA
            if self.playertype == 1:
                ObservedPlayerIndex = random.choice(playerlistType1)
            elif self.playertype == 2:
                ObservedPlayerIndex = random.choice(playerlistType2)
            if playerdict[ObservedPlayerIndex].lastActionA == MyAction:
                return (MyAction)
            revisionProb = max(0, ((playerdict[ObservedPlayerIndex].lastGameAPay - self.lastGameAPay)/3))
            
            ## Uses revision probability to decide whether or not to change strategies
            if random.uniform(0,1) > revisionProb:  ## If a randomly drawn number between 0 and 1 is less than Type1PlayingA1, actionA returns 1
                return (self.lastActionA)
            else:  
                if self.playertype == 1:
                    local_payoffmat = GameB1_PAYOFFMAT
                else:
                    local_payoffmat = GameB2_PAYOFFMAT
                if (self.lastActionB == 1):
                    indirectPayA1 = PROPTYPE1*(proptype1otherA1playB1*local_payoffmat.get('B1B1')+proptype1otherA1playB2*local_payoffmat.get('B1B2'))+PROPTYPE2*(proptype2otherA1playB1*local_payoffmat.get('B1B1')+proptype2otherA1playB2*local_payoffmat.get('B1B2'))
                    indirectPayA2 = PROPTYPE1*(proptype1otherA2playB1*local_payoffmat.get('B1B1')+proptype1otherA2playB2*local_payoffmat.get('B1B2'))+PROPTYPE2*(proptype2otherA2playB1*local_payoffmat.get('B1B1')+proptype2otherA2playB2*local_payoffmat.get('B1B2'))
                elif (self.lastActionB == 2):
                    indirectPayA1 = PROPTYPE1*(proptype1otherA1playB1*local_payoffmat.get('B2B1')+proptype1otherA1playB2*local_payoffmat.get('B2B2'))+PROPTYPE2*(proptype2otherA1playB1*local_payoffmat.get('B2B1')+proptype2otherA1playB2*local_payoffmat.get('B2B2'))
                    indirectPayA2 = PROPTYPE1*(proptype1otherA2playB1*local_payoffmat.get('B2B1')+proptype1otherA2playB2*local_payoffmat.get('B2B2'))+PROPTYPE2*(proptype2otherA2playB1*local_payoffmat.get('B2B1')+proptype2otherA2playB2*local_payoffmat.get('B2B2'))
                evfora1 = PropPlayingA1*GameA_PAYOFFMAT.get('A1A1') + PropPlayingA2*GameA_PAYOFFMAT.get('A1A2') + indirectPayA1
                evfora2 = PropPlayingA1*GameA_PAYOFFMAT.get('A2A1') + PropPlayingA2*GameA_PAYOFFMAT.get('A2A2') + indirectPayA2
                EVdictA = {1: evfora1, 2: evfora2}
                actionA = max(EVdictA, key=EVdictA.get)
                self.lastActionA = actionA
                self.lastGameAPay = EVdictA.get(actionA)
                self.lastOppGameA = opp_index
                return(actionA)
                
    
    def moveB(self, opp_index, GameA_PAYOFFMAT, GameB1_PAYOFFMAT, GameB2_PAYOFFMAT, playerlistType1, 
              playerlistType2, playerdict, roundAgg):
        """
        Determines an action in GameB.
        
        Argument(s): 
            opp_index -- integer, opponent's player index.
            GameA_PAYOFFMAT -- dict, payoff matrix for Game A, all players.
            GameB1_PAYOFFMAT -- dict, payoff matrix for Game B, Type 1.
            GameB2_PAYOFFMAT -- dict, payoff matrix for Game B, Type 2.
            playerlistType1 -- list, of Type 1 player indices.
            playerlistType2 -- list, of Type 2 player indices.
            playerdict -- dict, of players
            roundAgg -- dict, key-value pairs that represent the state of the population in current round.
            
        Return(s): 
            integer, 1 for action B1 or 2 for action B2.
        """
        
        ProbType1GivenA1=roundAgg['ProbType1GivenA1']
        ProbType2GivenA1=roundAgg['ProbType2GivenA1']
        ProbType1GivenA2=roundAgg['ProbType1GivenA2']
        ProbType2GivenA2=roundAgg['ProbType2GivenA2']
        Type1PlayingB1=roundAgg['Type1PlayingB1']
        Type1PlayingB2=roundAgg['Type1PlayingB2']
        Type2PlayingB1=roundAgg['Type2PlayingB1']
        Type2PlayingB2=roundAgg['Type2PlayingB2']    
        
        if self.numGameB == 0:
            self.numGameB = self.numGameB + 1
            if self.playertype == 1:
                local_payoffmat = GameB1_PAYOFFMAT
            elif self.playertype == 2:
                local_payoffmat = GameB2_PAYOFFMAT
            if playerdict[opp_index].lastActionA == 1:
                evforb1 = ProbType1GivenA1*((Type1PlayingB1*local_payoffmat['B1B1'])+(Type1PlayingB2*local_payoffmat['B1B2']))+ProbType2GivenA1*((Type2PlayingB1*local_payoffmat['B1B1'])+(Type2PlayingB2*local_payoffmat['B1B2'])) # payoff function for a player playing action B1
                evforb2 = ProbType1GivenA1*((Type1PlayingB1*local_payoffmat['B2B1'])+(Type1PlayingB2*local_payoffmat['B2B2']))+ProbType2GivenA1*((Type2PlayingB1*local_payoffmat['B2B1'])+(Type2PlayingB2*local_payoffmat['B2B2'])) # payoff function for a player playing action B2
            elif playerdict[opp_index].lastActionA == 2:
                evforb1 = ProbType1GivenA2*((Type1PlayingB1*local_payoffmat['B1B1'])+(Type1PlayingB2*local_payoffmat['B1B2']))+ProbType2GivenA2*((Type2PlayingB1*local_payoffmat['B1B1'])+(Type2PlayingB2*local_payoffmat['B1B2'])) # payoff function for a player playing action B1
                evforb2 = ProbType1GivenA2*((Type1PlayingB1*local_payoffmat['B2B1'])+(Type1PlayingB2*local_payoffmat['B2B2']))+ProbType2GivenA2*((Type2PlayingB1*local_payoffmat['B2B1'])+(Type2PlayingB2*local_payoffmat['B2B2'])) # payoff function for a player playing action B2
            EVdictB = {1: evforb1, 2: evforb2}
            actionB = max(EVdictB, key=EVdictB.get)
            self.lastActionB = actionB
            self.lastGameBPay = EVdictB.get(actionB)
            self.lastOppGameB = opp_index
            return(actionB)
        else:
            self.numGameB = self.numGameB + 1            
            MyAction = self.lastActionB
            if self.playertype == 1:
                ObservedPlayerIndex = random.choice(playerlistType1)
            elif self.playertype == 2:
                ObservedPlayerIndex = random.choice(playerlistType2)
            if playerdict[ObservedPlayerIndex].lastActionB == MyAction:
                return(MyAction)
            revisionProb = max(0, ((playerdict[ObservedPlayerIndex].lastGameBPay - self.lastGameBPay)/3))
            if random.uniform(0,1) > revisionProb:
                return (self.lastActionB)
            else:       
                if self.playertype == 1:
                    local_payoffmat = GameB1_PAYOFFMAT
                elif self.playertype == 2:
                    local_payoffmat = GameB2_PAYOFFMAT    
                if playerdict[opp_index].lastActionA == 1:
                    evforb1 = ProbType1GivenA1*((Type1PlayingB1*local_payoffmat['B1B1'])+(Type1PlayingB2*local_payoffmat['B1B2']))+ProbType2GivenA1*((Type2PlayingB1*local_payoffmat['B1B1'])+(Type2PlayingB2*local_payoffmat['B1B2'])) # payoff function for a player playing action B1
                    evforb2 = ProbType1GivenA1*((Type1PlayingB1*local_payoffmat['B2B1'])+(Type1PlayingB2*local_payoffmat['B2B2']))+ProbType2GivenA1*((Type2PlayingB1*local_payoffmat['B2B1'])+(Type2PlayingB2*local_payoffmat['B2B2'])) # payoff function for a player playing action B2
                elif playerdict[opp_index].lastActionA == 2:
                    evforb1 = ProbType1GivenA2*((Type1PlayingB1*local_payoffmat['B1B1'])+(Type1PlayingB2*local_payoffmat['B1B2']))+ProbType2GivenA2*((Type2PlayingB1*local_payoffmat['B1B1'])+(Type2PlayingB2*local_payoffmat['B1B2'])) # payoff function for a player playing action B1
                    evforb2 = ProbType1GivenA2*((Type1PlayingB1*local_payoffmat['B2B1'])+(Type1PlayingB2*local_payoffmat['B2B2']))+ProbType2GivenA2*((Type2PlayingB1*local_payoffmat['B2B1'])+(Type2PlayingB2*local_payoffmat['B2B2'])) # payoff function for a player playing action B2  
                EVdictB = {1: evforb1, 2: evforb2}
                actionB = max(EVdictB, key=EVdictB.get)
                self.lastActionB = actionB
                self.lastGameBPay = EVdictB.get(actionB)
                self.lastOppGameB = opp_index
                return(actionB)


## BEGIN FUNCTION DEFINITIONS
 
def GeneratePlayers(playerdict, playerlistType1, playerlistType2, weight, roundAgg):
    """
    Fills playerdict{} with a population of players.
    
    Argument(s):
        playerdict -- dict, of players.
        playerlistType1 -- list, of Type 1 player indices.
        playerlistType2 -- list, of Type 2 player indices.
        weight -- integer, multiplies Game B payoffs.
        roundAgg -- dict, key-value pairs that represent the state of the population in current round.
            
    Return(s): 
        none.    
    """  
    
    for z in range(1,POPSIZE+1):
        playerdict[z] = SimplePlayer(z, playerlistType1, playerlistType2, weight, roundAgg)

def playGameA(p1index, p2index, GameA_PAYOFFMAT, GameB1_PAYOFFMAT, GameB2_PAYOFFMAT, playerlistType1, playerlistType2, 
              playerdict, roundAgg):
    """
    Gets player moves for GameA and stores game history.
    
    Argument(s): 
        p1index -- integer, index of player 1.
        p2index -- integer, index of player 2.
        GameA_PAYOFFMAT -- dict, payoff matrix for Game A, all players.
        GameB1_PAYOFFMAT -- dict, payoff matrix for Game B, Type 1.
        GameB2_PAYOFFMAT -- dict, payoff matrix for Game B, Type 2.
        playerlistType1 -- list, of Type 1 player indices.
        playerlistType2 -- list, of Type 2 player indices.
        playerdict -- dict, of players
        roundAgg -- dict, key-value pairs that represent the state of the population in current round.
        
    Return(s): 
        none.
    """     
    
    player1action = playerdict[p1index].moveA(p2index, GameA_PAYOFFMAT, GameB1_PAYOFFMAT, GameB2_PAYOFFMAT, 
                              playerlistType1, playerlistType2, playerdict, roundAgg)
    player2action = playerdict[p2index].moveA(p1index, GameA_PAYOFFMAT, GameB1_PAYOFFMAT, GameB2_PAYOFFMAT, 
                              playerlistType1, playerlistType2, playerdict, roundAgg)
    playerdict[p1index].lastActionA = player1action
    playerdict[p2index].lastActionA = player2action
    playerdict[p1index].lastOppGameA = p2index
    playerdict[p2index].lastOppGameA = p1index

def playGameB(p1index, p2index, GameA_PAYOFFMAT, GameB1_PAYOFFMAT, GameB2_PAYOFFMAT, playerlistType1, playerlistType2, 
              playerdict, roundAgg):
    """
    Gets player moves for GameB and stores game history.
    
    Argument(s): 
        p1index -- integer, index of player 1.
        p2index -- integer, index of player 2.
        GameA_PAYOFFMAT -- dict, payoff matrix for Game A, all players.
        GameB1_PAYOFFMAT -- dict, payoff matrix for Game B, Type 1.
        GameB2_PAYOFFMAT -- dict, payoff matrix for Game B, Type 2.
        playerlistType1 -- list, of Type 1 player indices.
        playerlistType2 -- list, of Type 2 player indices.
        playerdict -- dict, of players.
        roundAgg -- dict, key-value pairs that represent the state of the population in current round.
        
    Return(s): 
        none.
    """      
    
    player1action = playerdict[p1index].moveB(p2index, GameA_PAYOFFMAT, GameB1_PAYOFFMAT, GameB2_PAYOFFMAT, playerlistType1, 
                              playerlistType2, playerdict, roundAgg)
    player2action = playerdict[p2index].moveB(p1index, GameA_PAYOFFMAT, GameB1_PAYOFFMAT, GameB2_PAYOFFMAT, playerlistType1, 
                              playerlistType2, playerdict, roundAgg)
    playerdict[p1index].lastActionB = player1action
    playerdict[p2index].lastActionB = player2action
    playerdict[p1index].lastOppGameB = p2index
    playerdict[p2index].lastOppGameB = p1index
    playerdict[p1index].lastOppGameBLastActionA = playerdict[p2index].lastActionA
    playerdict[p2index].lastOppGameBLastActionA = playerdict[p1index].lastActionA
 
def divide(num, den):
    """
    A division operator that returns 0 when the quotient is undefined.
    
    Argument(s): 
        num -- floating point, numerator of quotient.
        den -- floating point, denominator of quotient.
        
    Return(s): 
        floating point, either quotient num/dem or 0 for undefined.
    """        
    
    if den == 0:
        return 0
    else:
        return (num/den)
 
def countAggs(playerdict, numType1, numType2):
    """
    Counts aggregrate variables and stores them in roundAgg.
    
    Argument(s): 
        playerdict -- dictionary, holds all players.
        numType1 -- integer, number of Type 1 players.
        numType2 -- integer, number of Type 2 players.
        
    Return(s): 
        none.
    """      

    ## Initialize all counting variables to 0
    numType1PlayingA1 = 0
    numType1PlayingA2 = 0
    numType2PlayingA1 = 0
    numType2PlayingA2 = 0
    numType1PlayingB1 = 0
    numType1PlayingB2 = 0
    numType2PlayingB1 = 0
    numType2PlayingB2 = 0
    numtype1otherA1 = 0
    numtype1otherA2 = 0
    numtype2otherA1 = 0
    numtype2otherA2 = 0
    numtype1otherA1playB1 = 0
    numtype1otherA1playB2 = 0
    numtype1otherA2playB1 = 0
    numtype1otherA2playB2 = 0
    numtype2otherA1playB1 = 0
    numtype2otherA1playB2 = 0
    numtype2otherA2playB1 = 0
    numtype2otherA2playB2 = 0
    
    ##Create dictionary for one round of aggregate values
    roundAgg={}
    
    ## Gets aggregate counts from this round
    for z in range (1, POPSIZE):
        
            if (playerdict[z].playertype == 1 and playerdict[z].lastOppGameBLastActionA == 1):
                numtype1otherA1 = numtype1otherA1 + 1
                if (playerdict[z].lastActionB == 1):
                    numtype1otherA1playB1 = numtype1otherA1playB1 + 1
                elif (playerdict[z].lastActionB == 2):
                    numtype1otherA1playB2 = numtype1otherA1playB2 + 1
            if (playerdict[z].playertype == 1 and playerdict[z].lastOppGameBLastActionA == 2):
                numtype1otherA2 = numtype1otherA2 + 1
                if (playerdict[z].lastActionB == 1):
                    numtype1otherA2playB1 = numtype1otherA2playB1 + 1
                elif (playerdict[z].lastActionB == 2):
                    numtype1otherA2playB2 = numtype1otherA2playB2 + 1
            if (playerdict[z].playertype == 2 and playerdict[z].lastOppGameBLastActionA == 1):
                numtype2otherA1 = numtype2otherA1 + 1
                if (playerdict[z].lastActionB == 1):
                    numtype2otherA1playB1 = numtype2otherA1playB1 + 1
                elif (playerdict[z].lastActionB == 2):
                    numtype2otherA1playB2 = numtype2otherA1playB2 + 1
            if (playerdict[z].playertype == 2 and playerdict[z].lastOppGameBLastActionA == 2):
                numtype2otherA2 = numtype2otherA2 + 1
                if (playerdict[z].lastActionB == 1):
                    numtype2otherA2playB1 = numtype2otherA2playB1 + 1
                elif (playerdict[z].lastActionB == 2):
                    numtype2otherA2playB2 = numtype2otherA2playB2 + 1
            if playerdict[z].playertype == 1 and playerdict[z].lastActionA == 1:
                numType1PlayingA1 = numType1PlayingA1 + 1
            if playerdict[z].playertype == 1 and playerdict[z].lastActionA == 2:
                numType1PlayingA2 = numType1PlayingA2 + 1
            if (playerdict[z].playertype == 2 and playerdict[z].lastActionA == 1):
                numType2PlayingA1 = numType2PlayingA1 + 1
            if (playerdict[z].playertype == 2 and playerdict[z].lastActionA == 2):
                numType2PlayingA2 = numType2PlayingA2 + 1
            if (playerdict[z].playertype == 1 and playerdict[z].lastActionB == 1):
                numType1PlayingB1 = numType1PlayingB1 + 1
            if (playerdict[z].playertype == 1 and playerdict[z].lastActionB == 2):
                numType1PlayingB2 = numType1PlayingB2 + 1
            if (playerdict[z].playertype == 2 and playerdict[z].lastActionB == 1):
                numType2PlayingB1 = numType2PlayingB1 + 1
            if (playerdict[z].playertype == 2 and playerdict[z].lastActionB == 2):
                numType2PlayingB2 = numType2PlayingB2 + 1

    ## Calculates aggregate proportions from counts
    roundAgg['proptype1otherA1playB1'] = divide(numtype1otherA1playB1, numtype1otherA1)
    roundAgg['proptype1otherA1playB2'] = divide(numtype1otherA1playB2, numtype1otherA1)
    roundAgg['proptype1otherA2playB1'] = divide(numtype1otherA2playB1, numtype1otherA2) 
    roundAgg['proptype1otherA2playB2'] = divide(numtype1otherA2playB2, numtype1otherA2) 
    roundAgg['proptype2otherA1playB1'] = divide(numtype2otherA1playB1, numtype2otherA1) 
    roundAgg['proptype2otherA1playB2'] = divide(numtype2otherA1playB2, numtype2otherA1) 
    roundAgg['proptype2otherA2playB1'] = divide(numtype2otherA2playB1, numtype2otherA2) 
    roundAgg['proptype2otherA2playB2'] = divide(numtype2otherA2playB2, numtype2otherA2) 
    roundAgg['Type1PlayingA1'] = divide(numType1PlayingA1, numType1)
    roundAgg['Type1PlayingA2'] = divide(numType1PlayingA2, numType1)
    roundAgg['Type2PlayingA1'] = divide(numType2PlayingA1, numType2)
    roundAgg['Type2PlayingA2'] = divide(numType2PlayingA2, numType2)
    roundAgg['Type1PlayingB1'] = divide(numType1PlayingB1, numType1)
    roundAgg['Type1PlayingB2'] = divide(numType1PlayingB2, numType1)
    roundAgg['Type2PlayingB1'] = divide(numType2PlayingB1, numType2)
    roundAgg['Type2PlayingB2'] = divide(numType2PlayingB2, numType2)
    roundAgg['PropPlayingA1'] = (roundAgg['Type1PlayingA1']*PROPTYPE1)+(roundAgg['Type2PlayingA1']*PROPTYPE2)
    roundAgg['PropPlayingA2'] = (roundAgg['Type1PlayingA2']*PROPTYPE1)+(roundAgg['Type2PlayingA2']*PROPTYPE2)
    roundAgg['PropPlayingB1'] = (roundAgg['Type1PlayingB1']*PROPTYPE1)+(roundAgg['Type2PlayingB1']*PROPTYPE2)
    roundAgg['PropPlayingB2'] = (roundAgg['Type1PlayingB2']*PROPTYPE1)+(roundAgg['Type2PlayingB2']*PROPTYPE2)
    roundAgg['ProbType1GivenA1'] = divide((PROPTYPE1*roundAgg['Type1PlayingA1']), (PROPTYPE1*roundAgg['Type1PlayingA1'])+(PROPTYPE2*roundAgg['Type2PlayingA1']))
    roundAgg['ProbType2GivenA1'] = divide((PROPTYPE2*roundAgg['Type2PlayingA1']), (PROPTYPE1*roundAgg['Type1PlayingA1'])+(PROPTYPE2*roundAgg['Type2PlayingA1']))
    roundAgg['ProbType1GivenA2'] = divide((PROPTYPE1*roundAgg['Type1PlayingA2']), (PROPTYPE1*roundAgg['Type1PlayingA2'])+(PROPTYPE2*roundAgg['Type2PlayingA2']))
    roundAgg['ProbType2GivenA2'] = divide((PROPTYPE2*roundAgg['Type2PlayingA2']), (PROPTYPE1*roundAgg['Type1PlayingA2'])+(PROPTYPE2*roundAgg['Type2PlayingA2']))
    
def main():
    """
    Main function
    """
    for w in range(1, MAXWEIGHT+1):
        
        weight = w ## Multiplies the Game B payoffs
        
        for u in range(1, MAXMULT+1):

            A1 = (u*0.05) ## Proportion of all players with initial Game A action A1
            
            ## Initialize variables
            Type1PlayingA1 = A1
            Type1PlayingA2 = 1 - Type1PlayingA1
            Type2PlayingA1 = A1
            Type2PlayingA2 = 1 - Type2PlayingA1
            Type1PlayingB1 = 0.5
            Type1PlayingB2 = 1 - Type1PlayingB1
            Type2PlayingB1 = 0.5
            Type2PlayingB2 = 1 - Type2PlayingB1
            
            # Initialize Type1 and Type2 counters
            numType1 = 0
            numType2 = 0   
            
            ## Create dictionaries and lists
            playerdict = {} ## Players
            aggVarsDict = {} # Aggregate variables
            playerlistType1 = list() ## List of players Type 1
            playerlistType2 = list() ## List of players Type 2
            
            ## Initializes aggregate variables for round      
            roundAgg={'PropPlayingA1': (Type1PlayingA1*PROPTYPE1)+(Type2PlayingA1*PROPTYPE2),
                      'PropPlayingA2': (Type1PlayingA2*PROPTYPE1)+(Type2PlayingA2*PROPTYPE2), 
                      'PropPlayingB1': (Type1PlayingB1*PROPTYPE1)+(Type2PlayingB1*PROPTYPE2), 
                      'PropPlayingB2': (Type1PlayingB2*PROPTYPE1)+(Type2PlayingB2*PROPTYPE2), 
                      'ProbType1GivenA1': (PROPTYPE1*Type1PlayingA1)/((PROPTYPE1*Type1PlayingA1)+(PROPTYPE2*Type2PlayingA1)), 
                      'ProbType2GivenA1': (PROPTYPE2*Type2PlayingA1)/((PROPTYPE1*Type1PlayingA1)+(PROPTYPE2*Type2PlayingA1)), 
                      'ProbType1GivenA2': (PROPTYPE1*Type1PlayingA2)/((PROPTYPE1*Type1PlayingA2)+(PROPTYPE2*Type2PlayingA2)), 
                      'ProbType2GivenA2': (PROPTYPE2*Type2PlayingA2)/((PROPTYPE1*Type1PlayingA2)+(PROPTYPE2*Type2PlayingA2)),
                      'Type1PlayingA1': Type1PlayingA1, 'Type1PlayingA2': Type1PlayingA2, 'Type2PlayingA1': Type2PlayingA1,
                      'Type2PlayingA2': Type2PlayingA2, 'Type1PlayingB1': Type1PlayingB1, 'Type1PlayingB2': Type1PlayingB2,
                      'Type2PlayingB1': Type2PlayingB1, 'Type2PlayingB2': Type2PlayingB2, 'proptype1otherA1playB1': 0.5, 
                      'proptype1otherA1playB2': 0.5, 'proptype1otherA2playB1': 0.5, 'proptype1otherA2playB2': 0.5, 
                      'proptype2otherA1playB1': 0.5, 'proptype2otherA1playB2': 0.5, 'proptype2otherA2playB1': 0.5, 
                      'proptype2otherA2playB2': 0.5}
            
            ## Initializes aggVarsDict as a dictionary of lists that will track aggregate variables for through the game
            for key in roundAgg:
                aggVarsDict['%s' % key]=[roundAgg['%s' % key]]
                    
            ## Defines Game A and B payoff matrices (B1 for Game B for a type 1 player, B2 is Game B for a type 2 player)
            GameA_PAYOFFMAT = {'A1A1': 3, 'A1A2': 0, 'A2A1': 0, 'A2A2' : 3} ## Creates Game A payoff matrix as a dictionary
            GameB1_PAYOFFMAT = {'B1B1': weight*3, 'B1B2': 0, 'B2B1': 0, 'B2B2' : weight*3} ## defines payoff matrix Game B for type 1 player, as a dictionary
            GameB2_PAYOFFMAT = {'B1B1': 0, 'B1B2': weight*3, 'B2B1': weight*3, 'B2B2' : 0} ## defines payoff matrix Game B for type 2 player, as a dictionary
            
            ## Creates a population of players
            GeneratePlayers(playerdict, playerlistType1, playerlistType2, weight, roundAgg)
            
            for v in range (1, POPSIZE+1):
                if playerdict[v].playertype == 1:
                        numType1 = numType1 + 1
                elif playerdict[v].playertype == 2:
                        numType2 = numType2 + 1  
              
            gamenames = ('A','B') ## Creates list of game names A and B
            
            ## Play game
            for x in range(1,NUMROUNDS+1):
            
                ## Randomly select players and games for a subset of the population
                for y in range(1, int(POPSIZE/20)):
                    p1index = random.randint(1,POPSIZE)
                    p2index = random.randint(1,POPSIZE)
                    Game = random.choice(gamenames) ## Randomly chooses from list "gamenames" and assigns to Game
                    
                    if Game == 'A':
                        playGameA(p1index, p2index, GameA_PAYOFFMAT, GameB1_PAYOFFMAT, GameB2_PAYOFFMAT, 
                                  playerlistType1, playerlistType2, playerdict, roundAgg)
                    elif Game == 'B':
                        playGameB(p1index, p2index, GameA_PAYOFFMAT, GameB1_PAYOFFMAT, GameB2_PAYOFFMAT, 
                                  playerlistType1, playerlistType2, playerdict, roundAgg)
               
                ## Compute aggregate variables for round
                countAggs(playerdict, numType1, numType2)
                
                ## Store aggregate variables
                for k in aggVarsDict:
                    aggVarsDict[k].append(roundAgg[k])
                
            print('Pickle') 
            
            ## Save aggregate variables dictionary to file
            with open(('weight.%d PropPlayingA1.%d' % (w, u)), 'wb') as handle:
                pickle.dump(aggVarsDict, handle)
            print('Game complete. Weight=%d PropPlayingA1=%f' % (w, A1))
    
    print('PROCESS COMPLETE')

main()