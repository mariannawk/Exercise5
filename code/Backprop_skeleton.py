import math
import random
import copy

#The transfer function of neurons, g(x)
def logFunc(x):
    return (1.0/(1.0+math.exp(-x)))

#The derivative of the transfer function, g'(x)
def logFuncDerivative(x):
    return math.exp(-x)/(pow(math.exp(-x)+1,2))

def randomFloat(low,high):
    return random.random()*(high-low) + low

#Initializes a matrix of all zeros
def makeMatrix(I, J):
    m = []
    for i in range(I):
        m.append([0]*J)
    return m

class NN: #Neural Network
    def __init__(self, numInputs, numHidden, learningRate=0.001):
        #Inputs: number of input and hidden nodes. Assuming a single output node.
        # +1 for bias node: A node with a constant input of 1. Used to shift the transfer function.
        self.numInputs = numInputs + 1
        self.numHidden = numHidden

        # Current activation levels for nodes (in other words, the nodes' output value)
        self.inputActivations = [1.0]*self.numInputs
        self.hiddenActivations = [1.0]*self.numHidden
        self.outputActivation = 1.0 #Assuming a single output.
        self.learningRate = learningRate

        # create weights
        #A matrix with all weights from input layer to hidden layer
        self.weightsInput = makeMatrix(self.numInputs,self.numHidden)
        #A list with all weights from hidden layer to the single output neuron.
        self.weightsOutput = [0 for i in range(self.numHidden)]# Assuming single output
        # set them to random vaules
        for i in range(self.numInputs):
            for j in range(self.numHidden):
                self.weightsInput[i][j] = randomFloat(-0.5, 0.5)
        for j in range(self.numHidden):
            self.weightsOutput[j] = randomFloat(-0.5, 0.5)

        #Data for the backpropagation step in RankNets.
        #For storing the previous activation levels (output levels) of all neurons
        self.prevInputActivations = []
        self.prevHiddenActivations = []
        self.prevOutputActivation = 0
        #For storing the previous delta in the output and hidden layer
        self.prevDeltaOutput = 0
        self.prevDeltaHidden = [0 for i in range(self.numHidden)]
        #For storing the current delta in the same layers
        self.deltaOutput = 0
        self.deltaHidden = [0 for i in range(self.numHidden)]

    def propagate(self, inputs):
        if len(inputs) != self.numInputs-1:
            raise ValueError('wrong number of inputs')

        # input activations
        self.prevInputActivations=copy.deepcopy(self.inputActivations)
        for i in range(self.numInputs-1):
            self.inputActivations[i] = inputs[i]
        self.inputActivations[-1] = 1 #Set bias node to -1.

        # hidden activations
        self.prevHiddenActivations=copy.deepcopy(self.hiddenActivations)
        for j in range(self.numHidden):
            sum = 0.0
            for i in range(self.numInputs):
                #print self.ai[i] ," * " , self.wi[i][j]
                sum = sum + self.inputActivations[i] * self.weightsInput[i][j]
            self.hiddenActivations[j] = logFunc(sum)

        # output activations
        self.prevOutputActivation=self.outputActivation
        sum = 0.0
        for j in range(self.numHidden):
            sum = sum + self.hiddenActivations[j] * self.weightsOutput[j]
        self.outputActivation = logFunc(sum)
        return self.outputActivation

    def computeOutputDelta(self):
        #TODO: Implement the delta function for the output layer (see exercise text)
        ### OUR CODE START ###
        # a is fed in first and hence previous
        o_a = self.prevOutputActivation
        o_b = self.outputActivation
        
        p = 1/(1+math.exp(o_b - o_a))

        self.prevDeltaOutput = logFuncDerivative(o_a)*(1-p)
        self.deltaOutput = logFuncDerivative(o_b)*(1-p)        
        ### OUR CODE STOP ###

    def computeHiddenDelta(self):
        #TODO: Implement the delta function for the hidden layer (see exercise text)
        ### OUR CODE START ###
        diff = self.prevDeltaOutput - self.deltaOutput

        for i in range(self.numHidden):
            self.prevDeltaHidden[i] = logFuncDerivative(self.prevHiddenActivations[i])*self.weightsOutput[i]*diff
            self.deltaHidden[i] = logFuncDerivative(self.hiddenActivations[i])*self.weightsOutput[i]*diff
            
        ### OUR CODE STOP ###

    def updateWeights(self):
        alpha = self.learningRate
        #TODO: Update the weights of the network using the deltas (see exercise text)

        ### OUR CODE START ###
        #S: o_a og o_b er aktivasjonsnivået til noden vi går fra.
        #Så den skal være input activation på input-hidden, og
        #hidden på hidden-output
        # iterate over output weights:
        for i in range(self.numHidden):
            o_a = self.prevHiddenActivations[i]
            o_b = self.hiddenActivations[i]
            self.weightsOutput[i] += alpha*(self.prevDeltaOutput*o_a - self.deltaOutput*o_b)

        
        # iterate over input weights:
        for i in range(self.numInputs):
            o_a = self.prevInputActivations[i]
            o_b = self.inputActivations[i]
            for j in range(self.numHidden):
                
                self.weightsInput[i][j] += alpha*(self.prevDeltaHidden[j]*o_a - self.deltaHidden[j]*o_b)
        
        ### OUR CODE STOP ###

    def backpropagate(self):
        self.computeOutputDelta()
        self.computeHiddenDelta()
        self.updateWeights()

    #Prints the network weights
    def weights(self):
        print('Input weights:')
        for i in range(self.numInputs):
            print(self.weightsInput[i])
        print()
        print('Output weights:')
        print(self.weightsOutput)

    def train(self, patterns, iterations=1):
        #TODO: Train the network on all patterns for a number of iterations.
        #To measure performance each iteration: Run for 1 iteration, then count misordered pairs.
        #TODO: Training is done  like this (details in exercise text):
        #-Propagate A
        #-Propagate B
        #-Backpropagate

        ### OUR CODE START ###
        errorLog = []
        for i in range(iterations):
            for pair in patterns:
                self.propagate(pair[0]) # returns stuff so might throw an error
                self.propagate(pair[1])
                self.backpropagate()
            errorRate = self.countMisorderedPairs(patterns)
            errorLog.append(errorRate)

        return errorLog
        ### OUR CODE STOP ###
        
    def countMisorderedPairs(self, patterns):
        #TODO: Let the network classify all pairs of patterns. The highest output determines the winner.
        #for each pair, do
        #Propagate A
        #Propagate B
        #if A>B: A wins. If B>A: B wins
        #if rating(winner) > rating(loser): numRight++
        #else: numMisses++
        #end of for
        #TODO: Calculate the ratio of correct answers:
        #errorRate = numMisses/(numRight+numMisses)

        ### OUR CODE START ###
        # a and b are features only, fed in without rating
        # they are fed in such that a is better than b
        numRight = 0
        numMisses = 0
        for pair in patterns:
            outA = self.propagate(pair[0])
            outB = self.propagate(pair[1])
            if outA > outB:
                numRight+=1
            else:
                numMisses+=1

                
        return numMisses/(numRight+numMisses)
        ### OUR CODE STOP ###
