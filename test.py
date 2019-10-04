import random
import math
import datetime
from enum import Enum, auto

StartTime = datetime.datetime.now()
CurrentTime = StartTime
elapsedMilliseconds = 0
millisecondCounter = 0
counter = 0
TOTAL_PROCESSES = 10000
RAND_MAX = 2147483647

CPUEmpty = True

sort = True
RR = False

currentQuantum = 0.001

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
	
def printProcesses(readyQueue):
	for i in range(len(readyQueue)):
		print("Process[" + str(i+1) + "]: Time Left: " + str(readyQueue[i].timeRemaining))




def scheduleEvent(event):
	eventQueue.append(event)

def eventHandler():
	global CPUEmpty
	global millisecondCounter
	if eventQueue:
		
		currentEvent = eventQueue.pop(0)
		#print("Current Event: " + str(currentEvent.eventType))
		if currentEvent.eventType == "CREATE_PROCESSES":
			#print("Creating Processes")
			createProcesses()
		elif (currentEvent.eventType == "MOVE_TO_READY" and readyQueue):
			#print("Selecting next process")
			selectNextProcess()
			CPUSimulator()
			CPUEmpty = False
		elif currentEvent.eventType == "MARK_AS_COMPLETE":
			#print("Marking process as complete")
			markAsComplete()
			CPUEmpty = True
		elif currentEvent.eventType == "RETURN_TO_READY":
			#print("fuck4")
			returnToReady()
			CPUEmpty = True
		else:
			return -1
	else:
		millisecondCounter = millisecondCounter + 1

def simulator():
	global millisecondCounter
	global CPUEmpty
	#scheduleEvent(event("CREATE_PROCESSES"))
	
	while checkForCompletion() == False:
	
		if millisecondCounter >= 1000:
			millisecondCounter = 0
			scheduleEvent(event("CREATE_PROCESSES"))
			#print("fuck")
		
		if readyQueue and CPUEmpty:
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
	global readyQueue
	global currentProcess
	readyQueue.append(currentProcess)
	
def CPUSimulator():
	global elapsedMilliseconds
	global counter
	global readyQueue
	global millisecondCounter
	global RR
	global currentQuantum
	global currentProcess
	#print("Current Process Time Remaining: " + str(currentProcess.timeRemaining))
	
	#printProcesses(readyQueue)
	
	
	if RR == True:
		# calculate how much work the CPU will do this cycle, idk: do we just use the Quantum as the number for milliseconds?
		#I'll just use 100ms for now, because ¯\_(ツ)_/¯
		workDone = currentQuantum*1000
		if (workDone >= currentProcess.timeRemaining):
			elapsedMilliseconds = elapsedMilliseconds + currentProcess.timeRemaining
			millisecondCounter = millisecondCounter + currentProcess.timeRemaining
			currentProcess.timeRemaining = 0
			counter = counter + 1
			#print("Current Process Time Remaining: " + str(currentProcess.timeRemaining))
			scheduleEvent(event("MARK_AS_COMPLETE"))
		else:
			currentProcess.timeRemaining = currentProcess.timeRemaining - workDone
			elapsedMilliseconds = elapsedMilliseconds + workDone
			millisecondCounter = millisecondCounter + workDone
			#print("Not done\n")
			scheduleEvent(event("RETURN_TO_READY"))
		
		
	else:
		elapsedMilliseconds = elapsedMilliseconds + (currentProcess.timeRemaining)
		millisecondCounter = millisecondCounter + (currentProcess.timeRemaining)
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
	
def sortInsert(toBeInserted, readyQueue):
	if not readyQueue:
		readyQueue.append(toBeInserted)
	else:
		for j in range(len(readyQueue)):
		#print(str(j) + "\n" + str(len(readyQueue)))
			if readyQueue[j].timeRemaining > toBeInserted.timeRemaining:
				readyQueue.insert(j, toBeInserted)
				break
	
	
	
def processGenerator(numberOfProcesses):
	global sort
	global currentProcess
	for i in range(0, numberOfProcesses):
		nextTotalTime = int(1000*genexp(1/0.06))
		
		
		if nextTotalTime == 0:
			nextTotalTime = 1
			
		newProcess = process(nextTotalTime)
			
		if sort == True:
		
			sortInsert(newProcess, readyQueue)
			
			if currentProcess.timeRemaining > readyQueue[0].timeRemaining:
				temp = currentProcess
				currentProcess = readyQueue[0].pop()
				sortInsert(temp, readyQueue)
		else:
			readyQueue.append(process(nextTotalTime))
	
def checkForCompletion():
	global counter
	global TOTAL_PROCESSES
	
	#print("\nCurrent Counter: " + str(counter))
	#print("Total: " + str(TOTAL_PROCESSES))
	
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


def resetSimulator():
	global eventQueue
	global readyQueue
	global elapsedMilliseconds
	global counter
	global StartTime
	global millisecondCounter
	global CPUEmpty
	eventQueue.clear()
	readyQueue.clear()
	elapsedMilliseconds = 0
	millisecondCounter = 0
	counter = 0
	StartTime = datetime.datetime.now()
	CPUEmpty = True
	

#print(str(int(1000*genexp(1/0.06))) + " milliseconds")






for i in range(1, 31):
	#print(i)
	currentLambda = i
	simulator()
	print("\nCurrent Lambda: " + str(i))
	print("Start Time: " + str(StartTime))
	print("Total Milliseconds: " + str(elapsedMilliseconds))
	print("Final Length of readyQueue: " + str(len(readyQueue)))
	#printProcesses(readyQueue)
	resetSimulator()
	
	

