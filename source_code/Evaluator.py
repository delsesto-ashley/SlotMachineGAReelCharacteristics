import math
def Evaluate(individual,slotModel):
	expandedReels = []
	for rNum in range(individual.numReels):
		expandedReels.append([])
		for segment in individual.chromosome[rNum]:
			for i in range(segment[1]):
				expandedReels[rNum].append(segment[0])
	RTP = slotModel.evaluateRTP(expandedReels)
	nRTP = math.pow(0.9,abs(slotModel.targets[0]-RTP)*10)
	symDiversity = 0
	rVal = (nRTP*100)
	return rVal, RTP, symDiversity
