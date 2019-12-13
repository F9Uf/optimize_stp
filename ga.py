import time
from random import shuffle, randint
import pymongo

def ox_crossover(parent_1, parent_2, N = 15):
    start = randint(0, N-1)
    end = randint(start, N-1)
    if(end-start == N-1):
        end = end - 1
    subParent_1 = parent_1[start:end+1]
    subParent_2 = parent_2[start:end+1]
    child_1 = parent_1
    child_2 = parent_2
    parent_1 = [ x for x in parent_1 if x not in subParent_2]
    parent_2 = [ x for x in parent_2 if x not in subParent_1]
    if(end != N-1):
        child_1[end+1:N] = parent_2[len(parent_2)-N+end+1:]
        child_2[end+1:N] = parent_1[len(parent_1)-N+end+1:]
    child_1[:start] = parent_2[:start]
    child_2[:start] = parent_1[:start]
    return [child_1, child_2]

def generateChromosome(n):
    x = list(range(n))
    shuffle(x)
    return x

def generatePopulation(M=10, N=15):
    # M is populationsize (default 10)
    # N is length of chromosome (default 15)
    populations = [] # parent
    while len(populations) < M:
        newChromosome = generateChromosome(N)
        if newChromosome not in populations:
            populations.append(newChromosome)
    return populations

def calculateDistance(distance, chromosome):
    d = 0
    for i in range(len(chromosome) -1):
        d += distance[chromosome[i]][chromosome[i+1]]
    return d

def sorted_min_distance_chromosome(chromosomes):
    length = len(chromosomes)
    distance_each_chromosome = []
    for n in range(length):
        distance_each_chromosome.append((chromosomes[n],calculateDistance(data, chromosomes[n])))
    sorted_distance = sorted(distance_each_chromosome, key=lambda tup: tup[1])
#     selected_one = distance_each_chromosome.index(min_distance)
    return sorted_distance

def GA(data, N, pop_size, generation):
    populations = generatePopulation(pop_size, N) # generate populations
    populations = [ (x, calculateDistance(data, x)) for x in populations]
    
    bestChromosome = None

    for gen in range(generations):
        new_populations = []

        populations = sorted(populations, key=lambda x: x[1])[:pop_size]
        for i in range(0, len(populations)-1,2):
            if bestChromosome == None or bestChromosome[1]>populations[i][1]:
                bestChromosome = populations[i]
                # print(str(gen) + ") " + str(bestChromosome))

            chromosome1 = populations[i][0]
            chromosome2 = populations[i+1][0]
            child1, child2 = ox_crossover(chromosome1, chromosome2, N)
            new_populations.append((child1, calculateDistance(data, child1)))
            new_populations.append((child2, calculateDistance(data, child2)))

        for i in range(len(populations))[::-1]:
            del populations[i]

        populations = new_populations

    return bestChromosome

if __name__ == "__main__":
    data = [
        [0,262,398,172,601,392,185,158,181,353,557,682,249,408,491], 
        [262,0,410,186,512,310,90,324,258,342,475,532,167,258,409], 
        [400,414,0,476,313,209,322,256,220,48,288,598,246,342,253], 
        [161,185,472,0,574,371,158,329,267,404,537,655,228,381,470],
        [594,515,313,577,0,209,423,491,434,331,73,518,336,327,126],
        [392,312,209,374,209,0,221,289,231,155,184,415,145,220,117],
        [186,90,319,158,421,218,0,237,171,251,384,502,75,228,317],
        [158,322,249,330,491,289,235,0,72,234,454,634,196,360,388],
        [181,255,228,265,436,234,167,72,0,179,399,579,140,305,332],
        [155,271,48,416,73,155,263,301,177,0,320,552,187,282,254],
        [557,478,287,540,75,184,387,521,397,320,0,545,311,354,153],
        [676,532,606,649,520,416,495,720,575,555,547,0,437,318,397],
        [249,167,246,228,348,145,75,283,140,187,311,437,0,160,243],
        [408,258,348,372,327,225,230,360,305,282,354,318,162,0,204],
        [473,365,253,473,126,117,320,388,330,253,153,396,244,205,0] 
    ]
    myclient = pymongo.MongoClient("mongodb://157.230.44.229:27017/", username='root', password='root', authSource='logs', authMechanism='SCRAM-SHA-256')
    mydb = myclient["logs"]
    mycol = mydb["ga"]
    max_N = 15
    pop_size = 500
    generations = 5000
    rounds = 5
    for n in range(6, max_N + 1):
        for r in range(rounds):
            start = time.time()
            best = GA(data, n, pop_size, generations)
            end = time.time()
            print('N: %d | round: %d | shortest path: %s : %dkm | time: %8.10fs' % (n, r+1, best[0], best[1], (end - start)))
            x = mycol.insert_one({ 'N': n, 'round': r+1, 'chromosome': str(best[0]), 'distance': best[1], 'time': (end - start) })
