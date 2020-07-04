import random
import matplotlib.pyplot as plt
from tqdm import tqdm


msg = "hello world"

#---------------------------------------------------------------------------------------
#using a class to create an agent that will learn

class agent:
    #neet to learn use of alpha beta and epsilson again. hard code values here
    def __init__(self,alpha, beta, epsilon):

        self.alpha = alpha
        self.beta = beta
        self.epsilon = epsilon

        self.tbl = {}
        self.prevState = None
        self.state = None
        self.prevAction = None
        self.reward = None
        self.wins = []

        self.x = []
        self.y = []

        self.ty = []

        #combine these into string array so q learning can be applied. if not redo w method you made w jie
        self.face  =  ['g','g','g','g']
        self.back  =  ['b','b','b','b']
        self.left  =  ['o','o','o','o']
        self.right =  ['r','r','r','r']
        self.up    =  ['w','w','w','w']
        self.down  =  ['y','y','y','y']  

        #using this to store goal state
        self.goalState = str([self.face, self.back, self.left, self.right, self.up, self.down])

        self.y_average = []

        self.movesUsed = []

        self.ortega = 0


    #-----------------------------------------------------------------------------------
    #implementing moves for Rubiks cube here. made inside class function
    #in theory these should never be touched again

    def upMove(self):

        st1 = self.face[0] 
        st2 = self.face[1]

        self.face[0] = self.right[0]
        self.face[1] = self.right[1]

        self.right[0] = self.back[0]
        self.right[1] = self.back[1]

        self.back[0] = self.left[0]
        self.back[1] = self.left[1]

        self.left[0] = st1
        self.left[1] = st2

        st3 = self.up[0]

        self.up[0] = self.up[2]
        self.up[2] = self.up[3]
        self.up[3] = self.up[1]
        self.up[1] = st3

    
    def faceMove(self):
    
        st1 = self.up[2]
        st2 = self.up[3]

        self.up[2] = self.left[3]
        self.up[3] = self.left[1]

        self.left[3] = self.down[1]
        self.left[1] = self.down[0]

        self.down[0] = self.right[2]
        self.down[1] = self.right[0]

        self.right[0] = st1
        self.right[2] = st2

        st3 = self.face[0]

        self.face[0] = self.face[2]
        self.face[2] = self.face[3]
        self.face[3] = self.face[1]
        self.face[1] = st3

    
    def rightMove(self):

        st1 = self.back[0]
        st2 = self.back[2]

        self.back[0] = self.up[3]
        self.back[2] = self.up[1]

        self.up[1] = self.face[1]
        self.up[3] = self.face[3]

        self.face[1] = self.down[1]
        self.face[3] = self.down[3]

        self.down[1] = st2
        self.down[3] = st1

        st3 = self.right[0]
        
        self.right[0] = self.right[2]
        self.right[2] = self.right[3]
        self.right[3] = self.right[1]
        self.right[1] = st3

    
    def counterUp(self):
    
        st1 = self.face[0]
        st2 = self.face[1]

        self.face[0] = self.left[0]
        self.face[1] = self.left[1]

        self.left[0] = self.back[0]
        self.left[1] = self.back[1]

        self.back[0] = self.right[0]
        self.back[1] = self.right[1]

        self.right[0] = st1
        self.right[1] = st2

        st3 = self.up[0]

        self.up[0] = self.up[1]
        self.up[1] = self.up[3]
        self.up[3] = self.up[2]
        self.up[2] = st3

    
    def counterFace(self):
    
        st1 = self.up[2]
        st2 = self.up[3]

        self.up[2] = self.right[0]
        self.up[3] = self.right[2]

        self.right[0] = self.down[1]
        self.right[2] = self.down[0]

        self.down[0] = self.left[1]
        self.down[1] = self.left[3]

        self.left[1] = st2
        self.left[3] = st1

        st3 = self.face[0]

        self.face[0] = self.face[1]
        self.face[1] = self.face[3]
        self.face[3] = self.face[2]
        self.face[2] = st3

    
    def counterRight(self):
    
        st1 = self.back[0]
        st2 = self.back[2]

        self.back[0] = self.down[3]
        self.back[2] = self.down[1]

        self.down[1] = self.face[1]
        self.down[3] = self.face[3]

        self.face[1] = self.up[1]
        self.face[3] = self.up[3]

        self.up[1] = st2
        self.up[3] = st1

        st3 = self.right[0]

        self.right[0] = self.right[1]
        self.right[1] = self.right[3]
        self.right[3] = self.right[2]
        self.right[2] = st3

    #-----------------------------------------------------------------------------------
    #function to print cube in specific format
    def printCube(self):

        print()
    
        print("    ",self.up[0], self.up[1])
        print("    ",self.up[2], self.up[3])

        print(self.left[0],self.left[1],"",self.face[0],self.face[1],"",self.right[0],self.right[1],"",self.back[0],self.back[1])
        print(self.left[2],self.left[3],"",self.face[2],self.face[3],"",self.right[2],self.right[3],"",self.back[2],self.back[3])

        print("    ",self.down[0],self.down[1])
        print("    ",self.down[2],self.down[3]) 

    #-----------------------------------------------------------------------------------
    def makeMove(self, move):

        if move == 0:
            self.upMove()
            #print("upmove")

        elif move == 1:
            self.faceMove()
            #print("facemove")

        elif move == 2:
            self.rightMove()
            #print("rightmove")

        elif move == 3:
            self.counterUp()
            #print("counterup")

        elif move == 4:
            self.counterRight()
            #print("counterright")

        elif move == 5:
            self.counterFace()
            #print("counterface")   
    
    
    #function to randomise cube
    def randomise(self):

        #cube will be turned 10 to 20 times
        turns = random.randint(20,30)

        for i in range(0, turns):
            self.makeMove(random.randint(0,6))
            
    
    #-----------------------------------------------------------------------------------
    def reset(self):
        
        self.face  = ['g','g','g','g']
        self.back  = ['b','b','b','b']
        self.left  = ['o','o','o','o']
        self.right = ['r','r','r','r']
        self.up    = ['w','w','w','w']
        self.down  = ['y','y','y','y']

        #need to also reset object values 

        self.prevState = None
        self.state = None
        self.prevAction = None
        self.reward = None

    #-----------------------------------------------------------------------------------
    def smartMove(self, train):
        #always returns a number that will correspond to next move

        self.prevState = str([self.face, self.back, self.left, self.right, self.up, self.down])

        if self.prevState not in self.tbl:
            self.tbl[self.prevState] = [0.0,0.0,0.0,0.0,0.0,0.0]
            self.prevAction = random.randint(0,5)
            return self.prevAction

        else:
            #if statement to allow random chance of testing other moves
            if (random.randint(1,10) == 1) and train == True:
                self.prevAction = random.randint(0,5)
                return self.prevAction

            choices = []
            highest = -50

            for i in range(0,6):
                if self.tbl[self.prevState][i] > highest:
                    choices = []
                    choices.append(i)
                    highest = self.tbl[self.prevState][i] 
                elif self.tbl[self.prevState][i] == highest:
                    choices.append(i)

            self.prevAction = random.choice(choices)

            if train == False:
                self.movesUsed.append(self.prevAction)

            return self.prevAction

    #-----------------------------------------------------------------------------------
        #q learning function, updates q table here. doesnt need updating, should work perfectly 
    def maxAlpha(self, state):
        if state in self.tbl:
            return max(self.tbl[state])
        return 0.0

    def update(self, reward, state):   
        self.tbl[self.prevState][self.prevAction] += self.alpha  * (reward + self.epsilon * (self.maxAlpha(state)) - self.tbl[self.prevState][self.prevAction])


    #-----------------------------------------------------------------------------------
    #function calculates reward based on current state, then updates q table (another function)
    def checkState(self):
        
        if str([self.face, self.back, self.left, self.right, self.up, self.down]) == self.goalState:
            self.reward = 100
            #print("success. might actully do well in dissertation")
            return True
            #lead to update function now to updaet q table, then return

        #if not update q table with reward = -1
        self.reward = -1
        return False


    #-----------------------------------------------------------------------------------   
#    def check_ortega(self):
#        #if a whole side is done before terminating might resemble ortega
#        if self.up[0] == self.up[1] and self.up[0] == self.up[2] and self.up[0] == self.up[3]:
#            print("it happened, looks human")
#            self.ortega += 1
#        elif self.down[0] == self.down[1] and self.down[0] == self.down[2] and self.down[0] == self.down[3]:
#            print("it happened, looks human")
#            self.ortega += 1
#        elif self.left[0] == self.left[1] and self.left[0] == self.left[2] and self.left[0] == self.left[3]:
#            print("it happened, looks human")
#            self.ortega += 1
#        elif self.right[0] == self.right[1] and self.right[0] == self.right[2] and self.right[0] == self.right[3]:
#            print("it happened, looks human")
#            self.ortega += 1
#        elif self.face[0] == self.face[1] and self.face[0] == self.face[2] and self.face[0] == self.face[3]:
#            print("it happened, looks human")
#            self.ortega += 1
#        elif self.back[0] == self.back[1] and self.back[0] == self.back[2] and self.back[0] == self.back[3]:
#            print("it happened, looks human")
#            self.ortega += 1

    #-----------------------------------------------------------------------------------
    #make a move on cube then calculate reward, check if youve won
    #function used by both train and game 
    #i think i ended up not using this function
    def match(self, counter):

        play1.makeMove(play1.smartMove(True))

        #need to check result of move, update q table
        play1.checkState()

        if counter < 50:
            ...

#---------------------------------------------------------------------------------------
#this method may not be needed, may merge with training
#changed to just print out how agent is solving one game
def test(numGames, numWins):

        for i in range(1,11):

            play1.reset()
            counter = 1

            play1.randomise()

            print("starting game: ")
            print()
            play1.printCube()

            while True:

                play1.makeMove(play1.smartMove(False))#sets epsilon to zero
                print()
                print()
                play1.printCube()
                wins = play1.checkState()
                play1.update(play1.reward, str([play1.face, play1.back, play1.left, play1.right, play1.up, play1.down]))

                if wins == True:
                    print("cube solved in ", counter, " moves")
                    break

                #play1.check_ortega()
                
                counter += 1


    #print("during test cube was solved ", numWins, " times out of ", numGames, " attempts")

#---------------------------------------------------------------------------------------
#the game should work out here, while the states belong to the player


def training(play1, episodes):
    #need a counter to decide how many practice games
    numWins = 0
    games = 1

    #while games <= episodes:
    for i in tqdm(range(1,episodes)):
    #for i in range(0, episodes):

        play1.reset()
        counter = 1
        #print(len(play1.tbl))

        play1.randomise()
        #play1.printCube()
        #print(len(play1.tbl))
        solved = False

        #cube has been reset, loop here to try and solve cube
        #now need to check if the agent has solved cube 
        while solved == False:

            play1.makeMove(play1.smartMove(True))
            win = play1.checkState()
            play1.update(play1.reward, str([play1.face, play1.back, play1.left, play1.right, play1.up, play1.down]))

            if win == True:
                #print("rubiks cube solved in", counter, " number of moves")
                numWins += 1

                #this was added to not include extremely high results
                #if games > 1000:
                #    play1.x.append(games - 1000)
                #    play1.y.append(counter)
                
                play1.x.append(games)
                play1.y.append((counter * -1) + 100)

                if len(play1.y) == 20:
                    play1.y_average.append(sum(play1.y)/len(play1.y))
                    play1.y = []

                #counter = 1001
                games += 1
                solved = True

            else:     
                counter += 1


    
    #print("during training cube was solved ",numWins," times out of ",numGames, "attempts")
    #training(numGames + 1)




#---------------------------------------------------------------------------------------
def start(play1):
    a = input("enter train or test: ")

    if a == "train":
        #numTrain()
        training(1_000_001)

        #after training print size of q learning table 
        print("size of q learning table is currently ", len(play1.tbl))



        start(play1)
    elif a == "test":
        #play1.ortega = 0
        test(numGames = 0, numWins = 0)

        print("moves used were: ", play1.movesUsed)
        play1.movesUsed = []

        #print("number of solves similar to ortega method: ", play1.ortega, " out of 10 episodes",)

        start(play1)

    elif a == "exit":
        return
#---------------------------------------------------------------------------------------
print(msg)

play1 = agent(0.9,0.9,1)
"""play1.printCube()
print()
play1.randomise()
play1.printCube()"""



#play1.training(numGames = 1)
 
#start(play1)

#change this, collect results for steps against episodes
#while its training each time it solves cube plot steps required

agents = [agent(0.9,0.9,0.1) for i in range(0,5)]

for a in agents:
    training(a,1_000_001)

#plotList = [ agent.y_average[i] for agent in agents for i in range(0, len(agents[0].y_average / 10 ) ) ] 
plotList = []

for i in range(0, len(agents[0].y_average)):
    s = 0
    for a in agents:
        s += a.y_average[i]
    s/=len(agents)
    plotList.append(s)
    

#training(1_000_001) 
#start(play1)

#print(play1.x)
#print(play1.y)

#print(len(play1.y))

plt.axhline(y = 86, color = "green", label = "optimal reward")
plt.axhline(y = 80, color = "red", label = "human reward")
plt.grid(which = "both")

plt.xlabel("Episode")
plt.ylabel("Average episode reward over 20 games")
plt.title("Average episode reward of agent over time")

#this line will override play1.x
#play1.x = [i for i in range(0,len(play1.y_average))]
x = [i for i in range(0,len(plotList))]

#plt.plot(play1.x, play1.y_average)
plt.plot(x, plotList )
plt.show()

#need to run code again without average to show bumps


#need to remove agent making random moves during testing, it will skew with results 7