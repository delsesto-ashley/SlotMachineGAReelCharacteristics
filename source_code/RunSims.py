import secrets
from GA import GA
from Statistics import Statistics
from SlotModel import SlotModel
from Problem import Problem
import FileIO
import threading
import concurrent.futures
from multiprocessing.pool import ThreadPool

class Rngs:
	def __init__(self):
		self.seeds = []
	def CreateSeeds(self,numSeeds):
		if(len(self.seeds)):
			self.seeds.clear()
		for i in range(numSeeds):
			self.seeds.append(secrets.randbits(128))

def work(seed,slotModel,soln):
	#print("Seed Number: ",seed)
	ga = GA(seed, slotModel)
	ga.Init()
	ga.Run()
	soln.allFitnesses.append(ga.fitnesses)
	soln.allRTPs.append(ga.RTPs)
	soln.allSymDiversities.append(ga.symDiversities)
	soln.best.append(ga.best)
	print("Completed Seed ", seed)

if __name__ == "__main__":
	numSeeds = 1
	seedBank = Rngs()
	seedBank.CreateSeeds(numSeeds)
	allStats = Statistics()
	slotModel = SlotModel()
	FileIO.ReadInPaytable(slotModel)
	pool = ThreadPool(1)
	data = [(seed, slotModel,allStats) for seed in seedBank.seeds]
	results = pool.starmap(work,data)
	allStats.FindAvg()
	FileIO.WriteToCSV(allStats)
	FileIO.BestToCSV(allStats)
