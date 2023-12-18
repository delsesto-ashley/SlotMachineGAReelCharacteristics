import random
import Utils
class Individual:
	def __init__(self, options):
		self.chromosome = []
		self.numReels = options.numReels
		self.numRows = options.numRows
		self.chromosomeLength = options.chromosomeLength
		self.maxStack = options.maxStack
		self.maxStackStack = options.maxStackStack
		self.minStackStack = options.minStackStack
		self.bonusSymbols = options.bonusSymbols[:]
		self.symbolsToStack = options.symbolsToStack[:]
		self.fitness = -1
		self.symDiversity = -1
		self.bonusFrequency = -1
		self.RTP = -1

	def populate(self,options):
		for rNum in range(self.numReels):
			self.chromosome.append([])
			for i in range(self.chromosomeLength):
				self.chromosome[rNum].append([random.choice(options.symbolList),random.choice(options.symbolStackLengths)])

	def mutate(self, options):
		self.swapMutate(options)
		self.segmentMutate(options)

	def swapMutate(self,options):
		if Utils.flip(options.pSwapMut):
			segmentIndices = random.sample(range(int(self.chromosomeLength*self.numReels)),2)
			tSegment = self.chromosome[segmentIndices[0]//self.chromosomeLength][segmentIndices[0]%self.chromosomeLength][:]
			self.chromosome[segmentIndices[0]//self.chromosomeLength][segmentIndices[0]%self.chromosomeLength] = self.chromosome[segmentIndices[1]//self.chromosomeLength][segmentIndices[1]%self.chromosomeLength][:]
			self.chromosome[segmentIndices[1]//self.chromosomeLength][segmentIndices[1]%self.chromosomeLength] = tSegment[:]

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
						if Utils.flip(options.pStack):
							if self.chromosome[rNum][segNum][0] in self.symbolsToStack:
								self.chromosome[rNum][segNum][1] = (self.chromosome[rNum][segNum][1]+1)%(self.maxStackStack + 1)
							else:
								self.chromosome[rNum][segNum][1] = (self.chromosome[rNum][segNum][1]+1)%(self.maxStack + 1)
						else:
							if self.chromosome[rNum][segNum][0] in self.symbolsToStack:
								self.chromosome[rNum][segNum][1] = (self.chromosome[rNum][segNum][1]+(self.maxStackStack))%(self.maxStackStack+1)
							else:
								self.chromosome[rNum][segNum][1] = (self.chromosome[rNum][segNum][1]+(self.maxStack))%(self.maxStack+1)
			
	def myCopy(self, ind):
		self.fitness = ind.fitness
		self.RTP = ind.RTP
		self.symDiversity = ind.symDiversity
		self.bonusFrequency = ind.bonusFrequency
		self.chromosomeLength = ind.chromosomeLength # this should not change!
		for rNum in range(self.numReels):
			for i in range(self.chromosomeLength):
				for j in range(2):
					self.chromosome[rNum][i][j] = ind.chromosome[rNum][i][j]

	def recreate(self,ind):
		self.fitness = ind.fitness
		self.RTP = ind.RTP
		self.symDiversity = ind.symDiversity
		self.bonusFrequency = ind.bonusFrequency
		self.chromosomeLength = ind.chromosomeLength # this should not change!
		self.chromosome = self.copyChromosome(ind.chromosome)

	def copyChromosome(self,chromosome):
		newChromosome = []
		for rNum in range(self.numReels):
			newChromosome.append([])
			for i in range(self.chromosomeLength):
				newChromosome[rNum].append([])
				for j in range(2):
					newChromosome[rNum][i].append(chromosome[rNum][i][j])
		return newChromosome
	
	def adjustChromosome(self):
		directionIter = [-1,1]
		#process chromosome
		for rNum in range(self.numReels):
			for segmentNum in range(self.chromosomeLength):
				if self.chromosome[rNum][segmentNum][0] in self.bonusSymbols:
					self.chromosome[rNum][segmentNum][1] = 1
				elif self.chromosome[rNum][segmentNum][0] in self.symbolsToStack:
					self.chromosome[rNum][segmentNum][1] = max(self.chromosome[rNum][segmentNum][1],self.minStackStack)
				else:
					self.chromosome[rNum][segmentNum][1] = min(self.chromosome[rNum][segmentNum][1],self.maxStack)
		for rNum in range(self.numReels):
			for segmentNum in range(self.chromosomeLength):
				if self.chromosome[rNum][segmentNum][0] in self.bonusSymbols and self.chromosome[rNum][segmentNum][1]:
					bonusFound = 0
					for dir in directionIter:
						tCounter = 0
						tNumber = (segmentNum + dir)%self.chromosomeLength
						while tCounter < self.numRows:
							if self.chromosome[rNum][tNumber][0] in self.bonusSymbols and self.chromosome[rNum][tNumber][1]:
								bonusFound = 1
							tCounter += self.chromosome[rNum][tNumber][1]
							tNumber = (tNumber+dir)%self.chromosomeLength
					if bonusFound:
						self.chromosome[rNum][segmentNum][1] = 0
				elif self.chromosome[rNum][segmentNum][1]:
					sameLength = self.chromosome[rNum][segmentNum][1]
					for dir in directionIter:
						tNumber = (segmentNum + dir)%self.chromosomeLength
						sameSymbol = 1
						while sameSymbol:
							if self.chromosome[rNum][tNumber][0] != self.chromosome[rNum][segmentNum][0] and self.chromosome[rNum][tNumber][1]:
								sameSymbol = 0
							elif self.chromosome[rNum][tNumber][0] == self.chromosome[rNum][segmentNum][0]:
								sameLength += self.chromosome[rNum][tNumber][1]
							tNumber = (tNumber + dir)%self.chromosomeLength
					if self.chromosome[rNum][segmentNum][0] in self.symbolsToStack and sameLength > self.maxStackStack:
						self.chromosome[rNum][segmentNum][1] = max(self.chromosome[rNum][segmentNum][1]-(sameLength - self.maxStackStack),0)
					elif self.chromosome[rNum][segmentNum][0] not in self.symbolsToStack and sameLength > self.maxStack:
						self.chromosome[rNum][segmentNum][1] = max(self.chromosome[rNum][segmentNum][1]-(sameLength - self.maxStack),0)
		

	def decodeChromosome(self):
		expandedReels = []
		for rNum in range(self.numReels):
			expandedReels.append([])
			for segment in self.chromosome[rNum]:
				for l in range(segment[1]):
					expandedReels[rNum].append(segment[0])
		return expandedReels