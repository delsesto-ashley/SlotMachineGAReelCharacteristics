import random
import Utils
class Individual:
	def __init__(self, options):
		self.chromosome = []
		self.numReels = options.numReels
		self.numRows = options.numRows
		self.chromosomeLength = options.chromosomeLength
		self.fitness = -1
		self.symDiversity = -1
		self.RTP = -1

	def populate(self,options):
		for rNum in range(self.numReels):
			self.chromosome.append([])
			for i in range(self.chromosomeLength):
				self.chromosome[rNum].append([random.choice(options.symbolList),random.choice(options.symbolStackLengths)])

	#inverse mutation
	def mutate(self, options):
		if Utils.flip(options.pMut):
			tList = options.masterList[:]
			posList = []
			pos = random.choice(tList)-1
			length = random.choice(options.mutationOptions)
			for i in range(length):
				posList.append((pos+i)%(options.chromosomeLength))
			for i in range(int(Utils.floor(len(posList)/2,1))):
				tVal = self.chromosome[posList[i]]
				self.chromosome[posList[i]] = self.chromosome[posList[len(posList)-1-i]]
				self.chromosome[posList[len(posList)-1-i]] = tVal

	def swapMutate(self,options):
		for rNum in range(self.numReels):
			if Utils.flip(options.pSwapMut):
				segments = random.sample(range(self.chromosomeLength),2)
				tSegment = self.chromosome[rNum][segments[0]][:]
				self.chromosome[rNum][segments[0]] = self.chromosome[rNum][segments[1]][:]
				self.chromosome[rNum][segments[1]] = tSegment[:]

	def segmentMutate(self,options):
		for rNum in range(self.numReels):
			for segNum in range(self.chromosomeLength):
				if Utils.flip(options.pSegmentMut):
					if Utils.flip(options.pSegmentMutOption):
						curSymbolIndex = options.symbolList.index(self.chromosome[rNum][segNum][0])
						if Utils.flip(options.pSymbol):
							self.chromosome[rNum][segNum][0] = options.symbolList[(curSymbolIndex+1)%len(options.symbolList)]
						else:
							self.chromosome[rNum][segNum][0] = options.symbolList[(curSymbolIndex-1)%len(options.symbolList)]
					else:
						maxStack = max(options.symbolStackLengths)
						if Utils.flip(options.pStack):
							self.chromosome[rNum][segNum][1] = (self.chromosome[rNum][segNum][1])%maxStack + 1
						else:
							self.chromosome[rNum][segNum][1] = (self.chromosome[rNum][segNum][1]+(maxStack-1))%maxStack
			
	def myCopy(self, ind):
		self.fitness = ind.fitness
		self.RTP = ind.RTP
		self.symDiversity = ind.symDiversity
		self.chromosomeLength = ind.chromosomeLength # this should not change!
		for rNum in range(self.numReels):
			for i in range(self.chromosomeLength):
				for j in range(2):
					self.chromosome[rNum][i][j] = ind.chromosome[rNum][i][j]

	def recreate(self,ind):
		self.fitness = ind.fitness
		self.RTP = ind.RTP
		self.symDiversity = ind.symDiversity
		self.chromosomeLength = ind.chromosomeLength # this should not change!
		for rNum in range(self.numReels):
			self.chromosome.append([])
			for i in range(self.chromosomeLength):
				self.chromosome[rNum].append([])
				for j in range(2):
					self.chromosome[rNum][i].append(ind.chromosome[rNum][i][j])