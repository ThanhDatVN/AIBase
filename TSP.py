import random
import math 

# Mã hóa cá thể và khởi tạo quần thể
class Fitness:
	def __init__(self,route):
		self.route = route 
	def ObjectiveFunction(self,num_city,matrixCity):
		distance = 0
		for i in range(num_city-1):
			distance += matrixCity[self.route[i]-1][self.route[i+1]-1]
		return distance 

# tạo một cá thể 
def CreateRoute(num_city):

	cityList = [i for i in range(2,num_city+1)]
	route = random.sample(cityList,len(cityList))
	route = [1] + route
	# route = route +[route[0]]
	return route
# tạo quần thể đầu tiên 
def InitialPopulation(popSize,num_city):
	population = []
	for i in range(popSize):
		population.append(CreateRoute(num_city))
	return population

# lai ghép theo thứ tự 
def CrossOver(parent1, parent2):
	parent1 = parent1[1:]
	parent2 = parent2[1:]
	n = len(parent1)-1
	# crossover
	start = random.randint(1,n-1)
	end = random.randint(start,n)

	left_gen = parent1[:start]
	right_gen = parent1[end:]
	mid_gen = parent1[start:end]
	if len(right_gen) > 1:
		right_gen = [right_gen[0]] + sorted(right_gen[1:],key = lambda x: parent2.index(x))
	left_gen = sorted(left_gen,key = lambda x : parent2.index(x))

	child =  [1]+ left_gen + mid_gen + right_gen

	return child

# ĐỘT Biến bằng đoản đoạn
def Mutation(individual):
	individual = individual[1:]
	i = random.randint(1,len(individual)-2)
	j = random.randint(i+1,len(individual)-1)
	newgence = [1] + individual[:i] + individual[i:j][::-1] + individual[j:]
	return newgence
# creating next poputation:
def NextPopulation(population,crossoverRate,mutationRate,matrixCity,num_city):
	children = population.copy()
	population_size = len(population)

	# creating new individual 
	step = 0
	while step < population_size:
		# chosing random parents:
		parent1 = population[random.randint(0,population_size-1)]
		parent2 = population[random.randint(0,population_size-1)]

		# the probability of crossover
		if random.random() < crossoverRate:
			children.append(CrossOver(parent1,parent2))
			step += 1
		# the probability of mutation
		if random.random() < mutationRate:
			children.append(Mutation(parent1))
			children.append(Mutation(parent2))
	children.sort(key = lambda x: Fitness(x).ObjectiveFunction(num_city,matrixCity))
	return children[:population_size]

def geneticAlgorithm(matrixCity, popSize, crossoverRate, mutationRate, n_generations, maximumLoop):
	num_city = len(matrixCity)
	pop = InitialPopulation(popSize,num_city)
	pop.sort(key = lambda x: Fitness(x).ObjectiveFunction(num_city,matrixCity))
	# print("Initial distance: " +str(Fitness(pop[0]).ObjectiveFunction(num_city,matrixCity)))

	# visualization

	loopNotImprove = 0
	lastDistance = 0
	bestdistance = Fitness(pop[0]).ObjectiveFunction(num_city,matrixCity)
	bestRoute = pop[0]
	# finding best individual throught n generations:
	history = []
	for generation in range(n_generations):
		pop = NextPopulation(pop,crossoverRate,mutationRate,matrixCity,num_city)
		currDistance = Fitness(pop[0]).ObjectiveFunction(num_city,matrixCity)
		history.append(currDistance)
		print("Current distance of generation " + str(generation) + ":" + str(currDistance))
		if currDistance < bestdistance:
			bestdistance = currDistance
			bestRoute = pop[0]
		if lastDistance == currDistance:
			loopNotImprove += 1
		else:
			lastDistance = currDistance
			loopNotImprove = 0
		if loopNotImprove == maximumLoop:
			break
	print("Final distance: " + str(bestdistance))
	print(*bestRoute)
def input_data():
	n = int(input())
	list_point = []
	for i in range(n):
		list_point.append(list(map(int,input().split())))
	matrix = [[0 for _ in range(n)] for _ in range(n)]
	for i in range(n):
		for j in range(i+1,n):
			if matrix[i][j] == 0:
				matrix[i][j] = math.sqrt((list_point[i][0]-list_point[j][0])**2 + (list_point[i][1]-list_point[j][1])**2)
	return matrix 

if __name__ == '__main__':
	matrix_distance = input_data()
	geneticAlgorithm(matrixCity = matrix_distance , popSize=100,crossoverRate = 0.8, mutationRate=0.1, n_generations=200, maximumLoop=100)
