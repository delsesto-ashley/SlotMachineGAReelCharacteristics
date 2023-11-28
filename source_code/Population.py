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
		# fitness, rtp, symbol diversity, chromosome
		self.max = [-1,-1,-1,[]]
		# initialize population with randomly generated Individuals
		for i in range(options.populationSize):
			self.individuals.append(Individual(options))
			self.individuals[i].populate(options)

	def evaluate(self,slotModel):
		for ind in self.individuals:
			ind.fitness, ind.RTP, ind.symDiversity = Evaluator.Evaluate(ind,slotModel)
		return
			
	def printPop(self):
		i = 0
		for ind in self.individuals:
			print(i, end=": ")
			print (ind.chromosome, " Fit: ", ind.fitness)
			i = i+1
		self.report("")
		return

	def report(self, gen):
		print (gen, round(self.fitnesses[0],5), round(self.fitnesses[1],5), round(self.fitnesses[2],5))
		return

	def statistics(self):
		self.sumFitness = 0
		sumRTP = 0
		sumSymDiversity = 0
		self.fitnesses[1] = 0
		self.RTPs[1] = 0
		self.symDiversities[1] = 0
		tMinFitness = 1000000000
		tMaxFitness = -1
		tMinRTP = 1000000000
		tMaxRTP = -1
		tMinSymDiversity = 1000000000
		tMaxSymDiversity = -1
		for ind in self.individuals:
			self.sumFitness += ind.fitness
			sumRTP += ind.RTP
			sumSymDiversity += ind.symDiversity
			if ind.fitness < tMinFitness:
				tMinFitness = ind.fitness
			if ind.fitness > tMaxFitness:
				tMaxFitness = ind.fitness
			if ind.fitness > self.max[0]:
				self.max[0] = ind.fitness
				self.max[1] = ind.RTP
				self.max[2] = ind.symDiversity
				self.max[3] = ind.chromosome[:]
			if ind.RTP < tMinRTP:
				tMinRTP = ind.RTP
			if ind.RTP > tMaxRTP:
				tMaxRTP = ind.RTP
			if ind.symDiversity < tMinSymDiversity:
				tMinSymDiversity = ind.symDiversity
			if ind.symDiversity > tMaxSymDiversity:
				tMaxSymDiversity = ind.symDiversity
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
		return
		
	def tournamentSelection(self):
		baseIndividuals = self.individuals[:]
		individuals = []
		indices = []
		for i in range(self.options.gLambda):
			individuals.append(Individual(self.options))
			fighters = random.sample(baseIndividuals,self.options.tournamentSize)
			fighters.sort (key = self.comparator, reverse = True)
			individuals[i].recreate(fighters[0])
		return individuals

	def UX(self,pList,cList):
		if Utils.flip(self.options.pCross):
			for rNum in range(self.options.numReels):
				for segNum in range(self.options.chromosomeLength):
					if Utils.flip(self.options.pParentFavor):
						cList[0].chromosome[rNum][segNum] = pList[1].chromosome[rNum][segNum][:]
						cList[1].chromosome[rNum][segNum] = pList[0].chromosome[rNum][segNum][:]
		return cList

	def generation(self,child,slotModel):
		family = []
		for i in range(0,self.options.populationSize, self.options.gLambda):
			pList = self.tournamentSelection()
			cList = pList[:]
			cList = self.UX(pList,cList)
			for j in range(self.options.gLambda):
				cList[j].swapMutate(self.options)
				cList[j].segmentMutate(self.options)
				cList[j].fitness, cList[j].RTP, cList[j].symDiversity = Evaluator.Evaluate(cList[j],slotModel)
				family.append(cList[j])
			family.extend(pList)
			#fix a lot
		return

	def comparator(self, individual):
		return individual.fitness

	def halve(self, child):
		self.individuals.sort (key = self.comparator, reverse = True)
		for i in range(self.options.populationSize):
			del self.individuals[-1]
			child.individuals[i].myCopy(self.individuals[i])
		return
