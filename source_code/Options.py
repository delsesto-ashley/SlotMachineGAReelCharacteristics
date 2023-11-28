import math
class Options:
	def __init__(self,rSeed, slotModel):
		self.numReels = slotModel.numReels
		self.numRows = slotModel.numRows
		self.symbolList = slotModel.actualSymbolList[:]
		self.chromosomeLength = 100
		self.populationSize = 50
		self.symbolStackLengths = [1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,4,5]
		self.maxGen = 10
		self.pCross = 0.8
		self.pParentFavor = 0.5
		self.pSwapMut = 0.1
		self.pSegmentMut = 0.001
		self.pSegmentMutOption = 0.5
		self.pSymbol = 0.5
		self.pStack = 0.5
		self.tournamentSize = 2
		self.gLambda = 2
		self.randomSeed = rSeed