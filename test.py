import random
import math

counter = 0
RAND_MAX = 2147483647
processList = []


# CurrentState of [0] = Ready, [1] = Terminated, [-1] = Complete
class event():
	def __init__(self, totalTime, currentState):
		self.totalTime = totalTime
		self.timeRemaining = totalTime
		self.currentState = currentState
	
	
def urand():
	return (random.randint(0, RAND_MAX)/RAND_MAX)
	
def genexp(lam):
	x = 0
	while x == 0:
		u = urand()
		
		x = (-1/lam)*math.log(u);
	return x
	
	
def eventGenerator(events):
	for i in range(0, events):
		nextTotalTime = random.randint(1,100)
		processList.append(event(nextTotalTime, 0))
	
def checkForCompletion(processList):
	for i in processList:
		if i.currentState == 0:
			return False
		else:
			return True

def printProcessList(processList):
	position = 1
	
	for i in processList:
		printableOutput = "[Process " + str(position) + "]" + ": Total Time: " + str(i.totalTime) + ", Time Remaining: " + str(i.timeRemaining) + ", Current State: " + str(i.currentState)
		print(printableOutput)
		position = position + 1

def sortByTimeRemaning(processList):
	length = len(processList)
	
	for i in range(length):
		for j in range(0, length-i-1):
			if processList[j].timeRemaining > processList[j+1].timeRemaining:
				processList[j].timeRemaining, processList[j+1].timeRemaining = processList[j+1].timeRemaining, processList[j].timeRemaining


		
		
		
		
		
		
		
		
		

#for i in range(0, 10):
	#print(processList[i].totalTime)
	
#print(checkForCompletion(processList))

#eventGenerator(10)
#printProcessList(processList)
#print("\n")
#sortByTimeRemaning(processList)
#printProcessList(processList)

print(genexp(6))
