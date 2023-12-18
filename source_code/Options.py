import math
class Options:
	def __init__(self,rSeed, slotModel):
		self.numReels = slotModel.numReels
		self.numRows = slotModel.numRows
		self.symbolList = slotModel.actualSymbolList[:]
		self.symbolStackLengths = [1,1,1,1,2]
		self.maxStack = max(self.symbolStackLengths)
		self.minStackStack = slotModel.numRows
		self.maxStackStack = 5
		self.bonusSymbols = slotModel.bonusSymbols[:]
		self.symbolsToStack = slotModel.symbolsToStack[:]
		self.chromosomeLength = 100
		self.populationSize = 50
		self.maxGen = 100
		self.pCross = 0.9
		self.pParentFavor = 0.5
		self.pSwapMut = 0.1
		self.pSegmentMut = 0.001
		self.pSegmentMutOption = 0.5
		self.pSymbol = 0.5
		self.pStack = 0.5
		self.tournamentSize = 2
		self.gLambda = 2
		self.randomSeed = rSeed