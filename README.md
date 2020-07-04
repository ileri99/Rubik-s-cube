# Rubik-s-cube
Using reinforcement learning to solve the Rubik's cube

My implementation uses Q-learning to solve the 2x2x2 Rubik's cube. Since there are less than 4 million legal states it can be represented in a Q table.
This version plots the average results of only 5 agents over 1 million training episodes. It requires 4-5 hours to finish running. This implementation can be updated continuously plot the latest data in real time.

My code is messy - I need to clean up the format and remove functions no longer being used. Also, set epsilon to zero while collecting data to be plot.

Next steps: comparing Q-learning agent to neural network agent. How do their solutions differ? 
