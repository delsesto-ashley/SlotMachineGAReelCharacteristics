import math
def Evaluate(individual,slotModel):
	reelStrips = individual.decodeChromosome()

	RTP = slotModel.evaluateRTP(reelStrips)
	nRTP = math.pow(0.5,abs(slotModel.targets[0]-RTP)*20)
	symDiversity = evaluateSymbolDiversity(reelStrips,individual.numRows)
	nSymDiversity = math.pow(0.9,abs(slotModel.targets[1]-symDiversity)*20)

	bonusFrequency = slotModel.evaluateBonusFrequency(reelStrips)
	nBonusFrequency = math.pow(0.9,abs(slotModel.targets[2]-bonusFrequency)*100)
	
	rVal = ((nRTP+nBonusFrequency+nSymDiversity)/3*100)
	rVal = 100 - (math.pow(min(10*abs(slotModel.targets[0]-RTP)/slotModel.targets[0],6),2))
	rVal = rVal - min(2*abs(slotModel.targets[1]-symDiversity)/slotModel.targets[1],1)*28
	rVal = rVal - (math.pow(min(2*abs(slotModel.targets[2]-bonusFrequency)/slotModel.targets[2],6),2))
	return rVal, RTP, symDiversity, bonusFrequency

def evaluateSymbolDiversity(reels,rows):
	rDiversity = []
	tSymbols = []
	tSymbolsCount = []
	nReels = len(reels)
	for i in range(nReels):
		rDiversity.append(0)
		rLength = len(reels[i])
		for j in range(rLength):
			for k in range(rows):
				if reels[i][(j+k)%rLength] in tSymbols:
					tSymbolsCount[tSymbols.index(reels[i][(j+k)%rLength])]+=1
				else:
					tSymbols.append(reels[i][(j+k)%rLength])
					tSymbolsCount.append(1)
			rDiversity[i] += (max(tSymbolsCount)/rows)/rLength
			tSymbols.clear()
			tSymbolsCount.clear()
	totalDiversity = sum(rDiversity)/nReels
	return totalDiversity