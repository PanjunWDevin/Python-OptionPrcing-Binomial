# test binomial tree method 
import numpy as np
import math

# Parameter Initialization
ttm = 3.0      #time to maturity
tSteps = 25    #number of steps used
r = 0.03       #risk free rate
d = 0.02       #dividend Yield
sigma = 0.2    #volatility
strike = 100.0 #strike price
spot = 100.0   #spot price

# time step
dt = ttm / tSteps

# up factor Jarrow Rudd Tree
up = math.exp((r - d - 0.5*sigma*sigma)*dt + sigma*math.sqrt(dt))

# down factor Jarrow Rudd Tree
down = math.exp((r - d - 0.5*sigma*sigma)*dt - sigma*math.sqrt(dt))

discount = math.exp(-r*dt)

# build binomial trees, using numpy matrix
lattice = np.zeros((tSteps+1, tSteps+1))

#set the first node as spot
lattice[0][0] = spot

#set the rest of the matrix
for i in range(tSteps):
    for j in range(i+1):
        lattice[i+1][j+1] = up * lattice[i][j]
    lattice[i+1][0] = down * lattice[i][0]

#calculate each node's payoff, using map function
def payoff_option(spot):
    global strike
    return max(spot - strike,0)

#payoff = map(payoff_option,lattice[tSteps])

for i in range(tSteps,0,-1):
    for j in range (i,0,-1):
        if i == tSteps: #assign boundary conditions
            lattice[i-1][j-1]= 0.5 * discount * (payoff_option(lattice[i,j])+payoff_option(lattice[i][j-1]))
        else:
            lattice[i-1][j-1] = 0.5 * discount * (lattice[i, j] + lattice[i][j - 1])

print lattice[0][0]
