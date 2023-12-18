from Individual import Individual
import Evaluator
import random
import Utils

class Population(object):

	def	__init__(self, options):
		self.options = options
		self.individuals = []
		self.sumFitness = 0
		# min, avg, max
		self.fitnesses = [-1,-1,-1]
		self.RTPs = [-1, -1, -1]
		self.symDiversities = [-1, -1, -1]
		self.bonusFrequencies = [-1, -1, -1]
		# fitness, rtp, symbol diversity, bonus frequency, decoded chromosome
		self.max = [-1,-1,-1,-1,[]]
		# initialize population with randomly generated Individuals
		for i in range(options.populationSize):
			self.individuals.append(Individual(options))
			self.individuals[i].populate(options)
			self.individuals[i].adjustChromosome()

	def evaluate(self,slotModel):
		for ind in self.individuals:
			ind.fitness, ind.RTP, ind.symDiversity, ind.bonusFrequency = Evaluator.Evaluate(ind,slotModel)
		return
			
	def printPop(self):
		i = 0
		for ind in self.individuals:
			print(i, end=": ")
			print (ind.chromosome, " Fit: ", ind.fitness)
			i = i+1
		self.report("")
		return

	def report(self, gen, seedIDX):
		print (seedIDX, gen, round(self.fitnesses[0],5), round(self.fitnesses[1],5), round(self.fitnesses[2],5))
		return

	def statistics(self):
		self.sumFitness = 0
		sumRTP = 0
		sumSymDiversity = 0
		sumBonusFrequency = 0
		self.fitnesses[1] = 0
		self.RTPs[1] = 0
		self.symDiversities[1] = 0
		self.bonusFrequencies[1] = 0
		tMinFitness = 1000000000
		tMaxFitness = -1
		tMinRTP = 1000000000
		tMaxRTP = -1
		tMinSymDiversity = 1000000000
		tMaxSymDiversity = -1
		tMinBonusFrequency = 1000000000
		tMaxBonusFrequency = -1
		for ind in self.individuals:
			self.sumFitness += ind.fitness
			sumRTP += ind.RTP
			sumSymDiversity += ind.symDiversity
			sumBonusFrequency += ind.bonusFrequency
			if ind.fitness < tMinFitness:
				tMinFitness = ind.fitness
			if ind.fitness > tMaxFitness:
				tMaxFitness = ind.fitness
			if ind.fitness > self.max[0]:
				self.max[0] = ind.fitness
				self.max[1] = ind.RTP
				self.max[2] = ind.symDiversity
				self.max[3] = ind.bonusFrequency
				self.max[4] = ind.decodeChromosome()
			if ind.RTP < tMinRTP:
				tMinRTP = ind.RTP
			if ind.RTP > tMaxRTP:
				tMaxRTP = ind.RTP
			if ind.symDiversity < tMinSymDiversity:
				tMinSymDiversity = ind.symDiversity
			if ind.symDiversity > tMaxSymDiversity:
				tMaxSymDiversity = ind.symDiversity
			if ind.bonusFrequency < tMinBonusFrequency:
				tMinBonusFrequency = ind.bonusFrequency
			if ind.bonusFrequency > tMaxBonusFrequency:
				tMaxBonusFrequency = ind.bonusFrequency
		self.fitnesses[0] = tMinFitness
		self.fitnesses[1] = self.sumFitness/len(self.individuals)
		if tMaxFitness < self.fitnesses[2]:
			f = 0
		self.fitnesses[2] = tMaxFitness

		self.RTPs[0] = tMinRTP
		self.RTPs[1] = sumRTP/len(self.individuals)
		self.RTPs[2] = tMaxRTP

		self.symDiversities[0] = tMinSymDiversity
		self.symDiversities[1] = sumSymDiversity/len(self.individuals)
		self.symDiversities[2] = tMaxSymDiversity

		self.bonusFrequencies[0] = tMinBonusFrequency
		self.bonusFrequencies[1] = sumBonusFrequency/len(self.individuals)
		self.bonusFrequencies[2] = tMaxBonusFrequency
		return
		
	def tournamentSelection(self,slotModel):
		baseIndividuals = self.individuals[:]
		newIndividuals = []
		for t in range(0,self.options.populationSize, 2):
			parents = []
			children = []
			individuals = []
			for i in range(2):
				newIndividuals.append(Individual(self.options))
				parents.append(Individual(self.options))
				if len(baseIndividuals) < self.options.tournamentSize:
					parents[i].recreate(baseIndividuals[0])
					del baseIndividuals[0]
				else:
					fighters = random.sample(baseIndividuals,self.options.tournamentSize)
					fighters.sort (key = self.comparator, reverse = True)
					parents[i].recreate(fighters[0])
					del baseIndividuals[baseIndividuals.index(fighters[0])]
				individuals.append(parents[i])
				children.append(Individual(self.options))
				children[i].recreate(parents[i])
			children = self.UX(parents,children)
			for i in range(2):
				children[i].mutate(self.options)
				children[i].adjustChromosome()
				children[i].fitness, children[i].RTP, children[i].symDiversity, children[i].bonusFrequency = Evaluator.Evaluate(children[i],slotModel)
				individuals.append(children[i])
			individuals.sort (key = self.comparator, reverse = True)
			for i in range(2):
				newIndividuals[t+i].recreate(individuals[i])
		return newIndividuals

	def UX(self,pList,cList):
		if Utils.flip(self.options.pCross):
			for rNum in range(self.options.numReels):
				for segNum in range(self.options.chromosomeLength):
					if Utils.flip(self.options.pParentFavor):
						cList[0].chromosome[rNum][segNum] = pList[1].chromosome[rNum][segNum][:]
						cList[1].chromosome[rNum][segNum] = pList[0].chromosome[rNum][segNum][:]
		return cList

	def generation(self,child,slotModel):
		children = self.tournamentSelection(slotModel)
		for i in range(0,self.options.populationSize):
			child.individuals[i].myCopy(children[i])
		child.individuals.sort (key = self.comparator, reverse = True)
		return

	def comparator(self, individual):
		return individual.fitness

