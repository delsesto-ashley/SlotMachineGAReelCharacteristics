class Statistics():
	def __init__(self):
		self.allFitnesses = []
		self.allRTPs = []
		self.allSymDiversities = []
		self.allBonusFrequencies = []
		self.avgFitnesses = []
		self.avgRTPs = []
		self.avgSymDiversities = []
		self.avgBonusFrequencies = []
		# run --> gen fitness objective chromosome
		self.best = []
		self.indices = []
		for i in range(3):
			self.avgFitnesses.append([])
			self.avgRTPs.append([])
			self.avgSymDiversities.append([])
			self.avgBonusFrequencies.append([])
		self.lGen = 0
		self.lSeeds = 0

	def FindAvg(self):
		self.lGen = len(self.allFitnesses[0])
		self.lSeeds = len(self.allFitnesses)
		param = 3
		tNum = [0,0,0,0]
		for y in range(self.lGen):
			for z in range(param):
				for x in range(self.lSeeds):
					tNum[0] += self.allFitnesses[x][y][z]
					tNum[1] += self.allRTPs[x][y][z]
					tNum[2] += self.allSymDiversities[x][y][z]
					tNum[3] += self.allBonusFrequencies[x][y][z]
				for i in range(len(tNum)):
					tNum[i] = tNum[i]/self.lSeeds
				self.avgFitnesses[z].append(tNum[0])
				self.avgRTPs[z].append(tNum[1])
				self.avgSymDiversities[z].append(tNum[2])
				self.avgBonusFrequencies[z].append(tNum[3])
				for i in range(len(tNum)):
					tNum[i] = 0
		for x in range(self.lGen):
			self.indices.append(x)