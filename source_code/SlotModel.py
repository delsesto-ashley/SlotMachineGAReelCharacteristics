class SlotModel:
	def __init__(self):
		self.symbolList = []
		self.actualSymbolList = []
		self.lines = []
		self.payCombinations = []
		self.includes = []
		self.excludes = []
		self.bonusSymbols = []
		self.symbolsToStack = []
		self.targets = []
		self.numReels = -1
		self.numRows = -1
		self.exclDiff = 30

	def evaluateRTP(self,reels):
		totalPays = 0
		tProduct = 1
		reelProbs = []
		for rNum in range(self.numReels):
			reelProbs.append([])
			for sym in self.symbolList:
				reelProbs[rNum].append(0)
			reelLength = len(reels[rNum])
			for sym in reels[rNum]:
				reelProbs[rNum][self.symbolList.index(sym)]+=(1/reelLength)
			for inclList in self.includes:
				for sym in inclList[1]:
					reelProbs[rNum][self.symbolList.index(sym)]+=reelProbs[rNum][self.symbolList.index(inclList[0])]
			for sym in self.excludes:
				reelProbs[rNum][self.symbolList.index(sym)] = 1 - reelProbs[rNum][self.symbolList.index(sym-self.exclDiff)]
			reelProbs[rNum][len(self.symbolList)-1] = 1
		for payCombo in self.payCombinations:
			tProduct *= payCombo[0]
			for rNum in range(self.numReels):
				tProduct *= reelProbs[rNum][self.symbolList.index(payCombo[1][rNum])]
			totalPays += tProduct
			tProduct = 1
		return totalPays

			
			
			
				