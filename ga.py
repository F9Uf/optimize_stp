from random import shuffle

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

def crossover():
    return None

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


def calculateDistance(distance, chomosome):
    d = 0
    for i in range(len(chomosome) -1):
        d += distance[chomosome[i]][chomosome[i+1]]
    return d

if __name__ == '__main__':
    N = 15 # number of chromosome
    pop_size = 10 # number of parent
    populations = generatePopulation(pop_size, N)
    print(*populations, sep='\n')