import random
import math

def floor(x, base = 0.5):
	return base * math.floor(x/base)

def sumProduct(list1, list2):
	return sum(map(lambda x, y: x*y, list1, list2))

def flip(prob):
	return random.random() < prob

def randInt(low, high):
	return random.randint(low, high-1)
