import numpy as np
import random
import timeit


def benchmark(num_iters = 3, numColors = 0, numPegs = 0, answer = None):

    # prompt user for number of pegs and colors.
    populationSize = 200
    maxGen = 150             ## maximum number of populations generated for each guess
    maxSize = 100             ## maximum size of eligibleCodes for each guess
    avg_guesses = np.zeros((num_iters, 1))
    run_time = np.zeros((num_iters, 1))

    if numPegs==0:
        while (numPegs < 4) or (numPegs > 8):
            numPegs = int(input("Number of pegs (4-8): "))

    if numColors==0:
        while (numColors < 6) or (numPegs > 12):
            numColors = int(input("Number of colors (6-12): "))

    if answer == None:
        for pos in range(numPegs):
            answer.append(random.randint(1, numColors))

    for times in range(num_iters):
        # randomly generate the correct answer.
        blackPegs = [0]  ## contains black pegs for all previous guesses
        whitePegs = [0]  ## contains black pegs for all previous guesses
        eligibleCodes = [[]]  ## contains eligible codes for each turn
        playerGuess = []
        guesses = [[]]
        population = None

        if answer==None:
            for pos in range(numPegs):
                answer.append(random.randint(1, numColors))

        print "Secret Code: " + str(answer)

        start = timeit.default_timer()
        turn = 1
        # play initial guess
        for pos in range(numPegs):
            playerGuess.append(random.randint(1, 2))

        print "intial guess: "+str(playerGuess)
        guesses.append(playerGuess)
        b, w = setKeyPegs(playerGuess, answer)
        blackPegs.append(b)
        whitePegs.append(w)

        while (blackPegs[turn] != numPegs):
            turn+=1
            h = 1                                    ## h = generation's number
            E = []                                   ## set of eligible codes for ith guess

            #initialize population randomly
            population = generateRandomCodes(populationSize,numPegs,numColors)

            while(h<=maxGen and len(E)<maxSize):
                # calculate fitness of the population, and eligible codes in this population
                #print "h:"+str(h)
                fitness = calculateFitness(population, guesses, blackPegs, whitePegs,turn-1)

                # list of codes whose fitness score is 0
                eligibleCodesList = [ fitness[i][0] for i in range(len(fitness)) if fitness[i][1]==0 ]

                # add eligible codes to E (if not yet contained in E)
                e2 = [ eligibleCodesList[i] for i in range(len(eligibleCodesList)) if eligibleCodesList[i] not in E]

                E.extend(e2)

                # generate new population using crossover, mutation, permutation and inversion
                newPopulation = []
                for i in range(populationSize):
                    x, y = getParentsFromPopulation(fitness, populationSize)
                    child = reproduce(x, y, numPegs, numColors)
                    #if child already in population, generate a random code and add to population
                    if child in newPopulation:
                        while(child in newPopulation):
                            child = generateRandomCodes(1,numPegs,numColors)[0]

                    newPopulation.append(child)

                population = newPopulation
                #print population
                h+=1

            # play next guess from E
            if len(E)!=0:
                playerGuess,score = getNextGuessFromEligibleCodes(E),0
            else:
                fitness.sort(key=lambda code: code[1])
                playerGuess,score = fitness[0][0], fitness[0][1]

            print("Player's guess: %s, score: %d" %(str(playerGuess),score) )
            guesses.append(playerGuess)
            # get response (blackPegs, whitePegs)
            b, w = setKeyPegs(playerGuess, answer)
            blackPegs.append(b)
            whitePegs.append(w)

        stop = timeit.default_timer()
        run_time[times] = stop - start
        avg_guesses[times] = turn
        print('\n')
        print('Finished!')
        print("The guess is: " + str(playerGuess))
        print("The secret answer is: " + str(answer))
        print("Solved in " + str(turn) + " turn(s)!")

    print "Average number of guesses: %.2f" % np.average(avg_guesses)
    print "Minimum number of guesses: %d" % np.min(avg_guesses)
    print "Maximum number of guesses: %d" % np.max(avg_guesses)

    print "Average run time: %.2f second(s)" % np.average(run_time)
    print "Minimum run time: %.2f second(s)" % np.min(run_time)
    print "Maximum run time: %.2f second(s)" % np.max(run_time)

    return


def getNextGuessFromEligibleCodes(E):

    # returning random guess, ideally should return code which eliminates most eligible codes from E
    nextGuess = random.choice(E)
    return nextGuess

def calculateFitness(population, guesses, blackPegs, whitePegs, numGuesses):
    fitness = []
    for code in population:
        blackPegsDiff = 0
        whitePegsDiff = 0
        for g in range(1,numGuesses+1):
            b, w = setKeyPegs(guesses[g],code)
            blackPegsDiff+=abs(blackPegs[g] - b)
            whitePegsDiff += abs(whitePegs[g] - w)

        fitness.append([code,2*blackPegsDiff+whitePegsDiff])

    return fitness

# returns parents with lower score codes having more probability of being selected
def getParentsFromPopulation(fitness, populationSize):
    x = None
    y = None
    codes = []
    maxScore = max([fitness[i][1] for i in range(populationSize)])
    for code,fitness_score in fitness:
        for i in range(maxScore-fitness_score+1):
            codes.append(code)

    #random.shuffle(codes)
    x = random.choice(codes)
    y = x
    while y==x:
        y = random.choice(codes)
    return x, y

## generate all possible codes
def generateRandomCodes(populationSize, numPegs, numColors):
    codes = []

    while(len(codes)<populationSize):
        code = []
        for j in range(numPegs):
            code.append(random.randint(1,numColors))
        if( code not in codes):
            codes.append(code)

    return codes

## return number of black and white pegs for the current guess, given the answer
def setKeyPegs(guess, answer):
    tempGuess = []
    tempAnswer = []
    tempKeys = []
    numPegs = len(guess)
    blackPegs = 0
    whitePegs = 0
    for peg in guess:
        tempGuess.append(peg)

    for peg2 in answer:
        tempAnswer.append(peg2)

    #print answer
    #if len(tempAnswer)<4:
        #print "short:" + str(tempAnswer)
    # add black key pegs
    for pos in range(numPegs):
        try:
            if (tempGuess[pos] == tempAnswer[pos]):
                blackPegs+=1
                tempGuess[pos] = None
                tempAnswer[pos] = None
        except:
            print "failing now"
            print tempGuess
            print tempAnswer
            print pos

    # add white key pegs.
    for pos, peg in enumerate(tempGuess):
        for pos2, peg2 in enumerate(tempAnswer):
            if (peg == peg2) and (peg != None) and (peg2 != None):
                whitePegs+=1
                tempGuess[pos] = None
                tempAnswer[pos2] = None
                break  # break from inner loop
    return blackPegs,whitePegs

## combines two parent codes
def reproduce(x, y, numPegs, numColors):

    crossoverProbability = 0.5
    mutationProbability = 0.03
    permutationProbability = 0.03
    inversionProbability = 0.02

    # single-crossover/two-crossover
    prob = random.random()
    if prob<crossoverProbability:
        # do single crossover
        cross_point = random.randint(0,numPegs-2)
        z = x[:cross_point+1] + y[cross_point+1:]
    else:
        # do double cross-over
        pos1 = random.randint(1, numPegs - 3)
        pos2 = random.randint(pos1+1, numPegs - 2)
        z = x[:pos1] + y[pos1:pos2+1] + x[pos2+1:]

    #mutation
    prob = random.random()
    if(prob<mutationProbability):
        #randomly choose one position and change its value
        pos = random.randint(0,numPegs-1)
        pegColor = random.randint(1,numColors)
        z[pos] = pegColor

    # permutation
    prob = random.random()
    if (prob < permutationProbability):
        pos1 = random.randint(0, numPegs - 2)
        pos2 = random.randint(pos1 + 1, numPegs - 1)
        z[pos1], z[pos2] = z[pos2], z[pos1]

    # inversion
    prob = random.random()
    if(prob<inversionProbability):
        pos1 = random.randint(0, numPegs - 2)
        pos2 = random.randint(pos1 + 1, numPegs - 1)
        l = z[pos1:pos2+1]
        l.reverse()
        z[pos1:pos2 + 1] = l

    return z


if __name__ == '__main__':
    colors = None
    code = None
    list_colors = []
    secret_code = []
    while len(list_colors)<6 or len(list_colors)>12:
        colors = raw_input("Enter list of colors(6-12 colors,comma separated): ")
        list_colors = colors.split(',')

    while len(secret_code)<4 or len(secret_code)>8:
        code = raw_input("Enter the secret code(4-8 length,comma separated): ")
        secret_code = code.split(',')

    num_colors = len(list_colors)
    num_pegs = len(secret_code)
    secret_digit_code = []
    for i in range(len(secret_code)):
        secret_digit_code.append(list_colors.index(secret_code[i])+1)

    benchmark(numColors=num_colors, numPegs=num_pegs, answer=secret_digit_code)
