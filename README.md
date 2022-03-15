# norm-signaling
## Agent-based simulation for "An Evolutionary Signaling Model of the Emergence of Norms"

This is an agent-based simulation of the plural signaling game outlined in 
"An Evolutionary Signaling Model of Social Norms" (Lindgren 2015). A population of players 
is generated according to the model parameters, pairs of players are 
assigned to play one another in one of two subgames (A or B) for 1000
rounds, and the data is recorded to the folder containing this Python file 
for later analysis. Typically, we would run the simulation 1000+ times, but 
for this code sample I set the parameters so that the game would only run once,
therefore creating only one data file. 

This version of the simulation will test weight and PropPlayingA1 variables, 
while holding all other variables constant. weight is a multiplier for the 
Game B payoff matrix. If Game A has payoffs of 3, weight=2 will create a 
Game B matrix with payoffs of 6. It will set a weight and then loop through 20 
different PropPlayingA1 values, between 0 and 0.45. Then it will increment 
through different weight values, 1 through 100, looping through PropPlayingA1 
values each time.

This agent-based simulation is modeled after "Simulating Evolutionary Games: 
A Python-Based Introduction" (Isaac 2008).
