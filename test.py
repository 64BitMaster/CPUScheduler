import random
import math
import datetime
from enum import Enum, auto

StartTime = datetime.datetime.now()
CurrentTime = StartTime
elapsedMilliseconds = 0
counter = 0
TOTAL_PROCESSES = 10000
RAND_MAX = 2147483647

readyQueue = []
eventQueue = []
finishedList = []

currentLambda = 1



class eventTypes(Enum):
	CREATE_PROCESSES = auto()
	MOVE_TO_READY = auto()
	MARK_AS_COMPLETE = auto()
	RETURN_TO_READY = auto()
	
class event():
	def __init__(self, eventType):
		self.eventType = eventType
	timeCreated = datetime.datetime.now()
	
class process():
	def __init__(self, totalTime):
		self.totalTime = totalTime
		self.timeRemaining = totalTime
		
currentProcess = process(0)
	

def scheduleEvent(event):
	eventQueue.append(event)

def eventHandler():

	currentEvent = eventQueue.pop(0)
	if currentEvent.eventType == "CREATE_PROCESSES":
		createProcesses()
	elif currentEvent.eventType == "MOVE_TO_READY":
		selectNextProcess()
		CPUSimulator()
	elif currentEvent.eventType == "MARK_AS_COMPLETE":
		markAsComplete()
	elif currentEvent.eventType == "RETURN_TO_READY":
		returnToReady()
	else:
		return -1

def simulator():

	while checkForCompletion() == False:
		scheduleEvent(event("CREATE_PROCESSES"))
		scheduleEvent(event("MOVE_TO_READY"))
		eventHandler()
		
		
		
		
			
			
			
		
def createProcesses():
	processGenerator(currentLambda)
	
def selectNextProcess():
	global currentProcess
	currentProcess = readyQueue.pop(0)
	
def markAsComplete():
	finishedList.append(currentProcess)
	
def returnToReady():
	readyQueue.append(currentProcess)
	
def CPUSimulator():
	global elapsedMilliseconds
	global counter
	global readyQueue
	
	global currentProcess
	print("Time Remaining: " + str(currentProcess.timeRemaining))
	elapsedMilliseconds = elapsedMilliseconds + (currentProcess.timeRemaining/1000)
	currentProcess.timeRemaining = 0
	counter = counter + 1
	
	scheduleEvent(event("MARK_AS_COMPLETE"))
	
	
	

	
def urand():
	return (random.randint(0, RAND_MAX)/RAND_MAX)
	
def genexp(lam):
	x = 0
	while x == 0:
		u = urand()
		
		x = (-1/lam)*math.log(u);
	return x
	
	
def processGenerator(numberOfProcesses):
	for i in range(0, numberOfProcesses):
		nextTotalTime = int(1000*genexp(1/0.06))
		if nextTotalTime == 0:
			nextTotalTime = 1
		print(nextTotalTime)
		readyQueue.append(process(nextTotalTime))
	
def checkForCompletion():
		if counter < TOTAL_PROCESSES:
			return False
		else:
			return True


def sortByTimeRemaning(readyQueue):
	length = len(readyQueue)
	
	for i in range(length):
		for j in range(0, length-i-1):
			if readyQueue[j].timeRemaining > readyQueue[j+1].timeRemaining:
				readyQueue[j].timeRemaining, readyQueue[j+1].timeRemaining = readyQueue[j+1].timeRemaining, readyQueue[j].timeRemaining



print(str(int(1000*genexp(1/0.06))) + " milliseconds")

simulator()
print(StartTime)
print(elapsedMilliseconds)
