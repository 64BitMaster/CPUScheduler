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

currentQuantum = 0.2

readyQueue = []
eventQueue = []
finishedList = []

currentLambda = 1

class eventTypes(Enum):
	CREATE_PROCESSES = auto()
	MOVE_TO_READY = auto()
	MARK_AS_COMPLETE = auto()
	RETURN_TO_READY = auto()
	
class runTypes(Enum):
	FCFS = auto()
	SRTF = auto()
	RR02 = auto()
	RR001 = auto()
	
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



	#### Helper function for the eventHandler() ###
	# Take the currentLambda and create that many processes
def createProcesses():
	global currentLambda
	processGenerator(currentLambda)
	
	# Move the next process in the readyQueue into the currentProcess
def selectNextProcess():
	global currentProcess
	global readyQueue
	currentProcess = readyQueue.pop(0)
	
	# Move the currentProcess into the finishedList
def markAsComplete():
	global currentProcess
	global finishedList
	finishedList.append(currentProcess)
	
	# Move the currentProcess back into the readyQueue
	# Since this is only used the Round Robin algorithm, we never have to worry about sorting these
def returnToReady():
	global readyQueue
	global currentProcess
	readyQueue.append(currentProcess)
	### ### ### ### ### ### ### ### ### ### ### ###


	# Adds event to the end of the event list
def scheduleEvent(event):
	eventQueue.append(event)

	# Pops the next event from the eventQueue and process it
def eventHandler():
	global CPUEmpty
	global millisecondCounter
	
	# Runs as long as the event is not empty
	if eventQueue:
		
		currentEvent = eventQueue.pop(0)
		
			# Creates more processes to be added to the readyQueue
		if currentEvent.eventType == "CREATE_PROCESSES":
			createProcesses()
			
			# Only runs if the readyQueue is not empty, and then prevents anymore 'MOVE' events from being created
		elif (currentEvent.eventType == "MOVE_TO_READY" and readyQueue):
			selectNextProcess()
			CPUSimulator()
			CPUEmpty = False
			
			# Allows 'MOVE' events to be created, as the CPU is now finished with its current task
		elif currentEvent.eventType == "MARK_AS_COMPLETE":
			markAsComplete()
			CPUEmpty = True
			
			# Allows 'RETURN' events to be created, as the CPU is now finished with its current task
		elif currentEvent.eventType == "RETURN_TO_READY":
			returnToReady()
			CPUEmpty = True
			
			# lol this shouldn't ever run, if it does ¯\_(ツ)_/¯
		else:
			print("something went really wrong lmao")
			return -1
	else:
		# If the eventQueue is empty, add a millisecond to the counter until the next 'CREATE' event is made
		millisecondCounter = millisecondCounter + 1

	# This is the main() of the simulation, which calls the eventHandler every cycle
def simulator():
	global millisecondCounter
	global readyQueue
	global CPUEmpty
	
		# Run until the processes completed reaches the 'TOTAL_PROCESS' global variable
	while checkForCompletion() == False:
	
			# Every second schedule a 'CREATE' even
		if millisecondCounter >= 1000:
			millisecondCounter = 0
			scheduleEvent(event("CREATE_PROCESSES"))
		
			# Move the next process into the CPU if the processQueue is not empty and CPU is
		if readyQueue and CPUEmpty:
			scheduleEvent(event("MOVE_TO_READY"))
			
			# Handle the next event in the eventQueue
		eventHandler()
		
	# The CPU handler, which determines if the current event will be complete by the current algorithm
def CPUSimulator():
	global elapsedMilliseconds
	global counter
	global readyQueue
	global millisecondCounter
	global RR
	global currentQuantum
	global currentProcess
	
		# If Round Robin is set to true, we keep track of how much work can be done, and if the event is finsihed or not
	if RR == True:
	
		workDone = currentQuantum*1000
			
			# If the work done is greater than or equal to the currentProcess.timeRemaining, we can mark it as complete and schedule the event to move it to the finishedList
		if (workDone >= currentProcess.timeRemaining):
			elapsedMilliseconds = elapsedMilliseconds + currentProcess.timeRemaining
			millisecondCounter = millisecondCounter + currentProcess.timeRemaining
			currentProcess.timeRemaining = 0
			counter = counter + 1
			
			scheduleEvent(event("MARK_AS_COMPLETE"))
			
			# Otherwise, we subtract the work done, and schedule the event to move it back to the readyQueue
		else:
			currentProcess.timeRemaining = currentProcess.timeRemaining - workDone
			elapsedMilliseconds = elapsedMilliseconds + workDone
			millisecondCounter = millisecondCounter + workDone
			
			scheduleEvent(event("RETURN_TO_READY"))
		
		# If Round Robin is false, we allow the process to fully complete, and then mark it as finished
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
			if readyQueue[j].timeRemaining > toBeInserted.timeRemaining:
				readyQueue.insert(j, toBeInserted)
				break
	
	# Called when you need to create new processes to be added to the readyQueue
def processGenerator(numberOfProcesses):
	global sort
	global currentProcess
	global readyQueue
	
	# Creates the number of processes determined by the current Lambda, with the timeRemaining set a random range always greater than zero
	for i in range(0, numberOfProcesses):
		nextTotalTime = int(1000*genexp(1/0.06))
		if nextTotalTime == 0:
			nextTotalTime = 1
			
		newProcess = process(nextTotalTime)
			
			# If we're keeping the readyQueue sorted, we just sort them during the insert so we don't have to worry about it later
		if sort == True:
		
			sortInsert(newProcess, readyQueue)
			
				# We also check if the currentProcesses.timeRemaining is larger than the first process in the sorted readyQueue, and swap if necessary
			if currentProcess.timeRemaining > readyQueue[0].timeRemaining:
				temp = currentProcess
				currentProcess = readyQueue[0].pop()
				sortInsert(temp, readyQueue)
			# Otherwise, we don't need to sort, so the event can be added to the end of the readyQueue
		else:
			readyQueue.append(process(nextTotalTime))
	
	# This is the main check to see if we're done processing yet
def checkForCompletion():
	global counter
	global TOTAL_PROCESSES
	
	if counter < TOTAL_PROCESSES:
		return False
	else:
		return True


	# Resets the simulator
def resetSimulator():
	global eventQueue
	global readyQueue
	global elapsedMilliseconds
	global millisecondCounter
	global counter
	global StartTime
	global CPUEmpty
	
	eventQueue.clear()
	readyQueue.clear()
	elapsedMilliseconds = 0
	millisecondCounter = 0
	counter = 0
	StartTime = datetime.datetime.now()
	CPUEmpty = True
	
	
	# Sets the currentRunType
def setRunType(selectedRunType):
	
	if selectedRunType == "FCFS":
		sort = False
		RR = False
		
	elif selectedRunType == "SRTF":
		sort = True
		RR = False
		
	elif selectedRunType == "RR02":
		sort = False
		RR = True
		currentQuantum = 0.2
		
	elif selectedRunType == "RR001":
		sort = False
		RR = True
		currentQuantum = 0.01
		
	else:
		print("something is broken lol")

	# Runs the simulator all 30 times
def runSimulation():

	for i in range(1, 31):

		currentLambda = i
		print("\nCurrent Lambda: " + str(i))
		print("Start Time: " + str(StartTime))

		simulator()
	
		print("Total Milliseconds: " + str(elapsedMilliseconds))
		print("Final Length of readyQueue: " + str(len(readyQueue)))
	
		resetSimulator()



setRunType("FCFS")
runSimulation()

setRunType("SRTF")
runSimulation()

setRunType("RR02")
runSimulation()

setRunType("RR001")
runSimulation()
