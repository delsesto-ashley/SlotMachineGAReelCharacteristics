from Population import Population
import Options
import random
class GA:
	def __init__(self,rSeed,seedIDX, slotModel):
		self.slotModel = slotModel
		self.options = Options.Options(rSeed, slotModel)
		random.seed(rSeed)
		self.fitnesses = []
		self.RTPs = []
		self.symDiversities = []
		self.bonusFrequencies = []
		self.seedIDX = seedIDX
		# gen, fitness, RTP, symbol diversity, bonus frequency, decoded chromosome
		self.best = [0,-1,-1,-1,-1,[]]

	def Init(self):
		self.parent = Population(self.options)
		self.parent.evaluate(self.slotModel)
		self.parent.statistics()
		self.parent.report(0,self.seedIDX)
		self.fitnesses.append(self.parent.fitnesses[:])
		self.RTPs.append(self.parent.RTPs[:])
		self.symDiversities.append(self.parent.symDiversities[:])
		self.bonusFrequencies.append(self.parent.bonusFrequencies[:])
		self.best[1] = self.parent.max[0]
		self.best[2] = self.parent.max[1]
		self.best[3] = self.parent.max[2]
		self.best[4] = self.parent.max[3]
		self.best[5] = self.parent.max[4][:]
		self.child = Population(self.options)
		return

	def Run(self):
		for	i in range(1, self.options.maxGen):
			self.parent.generation(self.child,self.slotModel)
			self.child.statistics()
			self.child.report(i, self.seedIDX)
			self.fitnesses.append(self.child.fitnesses[:])
			self.RTPs.append(self.child.RTPs[:])
			self.symDiversities.append(self.child.symDiversities[:])
			self.bonusFrequencies.append(self.child.bonusFrequencies[:])
			if self.child.max[0] > self.best[1]:
				self.best[0] = i
				self.best[1] = self.child.max[0]
				self.best[2] = self.child.max[1]
				self.best[3] = self.child.max[2]
				self.best[4] = self.child.max[3]
				self.best[5] = self.child.max[4][:]
			tmp = self.parent
			self.parent = self.child
			self.child = tmp
		return