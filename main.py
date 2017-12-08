import random
from itertools import product

def main():
    # prompt user for number of pegs and colors.
    numPegs = 0
    numColors = 0
    while (numPegs < 4) or (numPegs > 8):
        numPegs = int(input("Number of pegs (4-8): "))

    while (numColors < 6) or (numPegs > 12):
        numColors = int(input("Number of colors (6-12): "))

    globalAllCodes = []
    allCodes = []
    answer = []
    keyPegs = []
    playerGuess = []
    turn = 0
    won = False

    # create the entire set of possible codes.
    allCodes = createCodes(numPegs, numColors)
    # do it again for the codes that will be used in the minimax step. this list never shrinks.
    globalAllCodes = createCodes(numPegs, numColors)
    # set initial guess, all peg's colors are either 1 or 2
    for pos in range(numPegs):
        playerGuess.append(random.randint(1, 2))
    # randomly generate the correct answer.
    for pos in range(numPegs):
        answer.append(random.randint(1, numColors))
    # determine key pegs for the initial guess.
    keyPegs = setKeyPegs(playerGuess, answer)
    print("The secret code is: " + str(answer))

    while not won:
        print("----------------------------------------")
        # play the guess and get new code list.
        print("Player's guess: " + str(playerGuess))
        globalAllCodes.remove(tuple(playerGuess) )
        won = checkWin(keyPegs, numPegs, turn)
        if won:
            break
        turn += 1
        print("Turn " + str(turn) + ":")
        print("Shrinking possible codes...")
        allCodes = getNewCodes(allCodes, playerGuess, keyPegs)
        print("Number of possible codes left: " + str(len(allCodes)))
        print("Applying minimax to remaining codes...")
        playerGuess = applyMinimax(globalAllCodes, allCodes, playerGuess, keyPegs, answer, numPegs)
        print('next guess: ' + str(playerGuess))
        print("Determining keys for new guess...")
        keyPegs = setKeyPegs(playerGuess, answer)

    print('\n')
    print('Finished!')
    print("The guess is: " + str(playerGuess))
    print("The secret answer is: " + str(answer))
    print("Solved in " + str(turn) + " turn(s)!")

    return 

def applyMinimax(globalCodes, currentCodes, lastGuess, lastGuessKeys, answer, numPegs):
    # generate all possible key combinations.
    outcomes = []
    for i in range(0,numPegs+1):
        for key in product(('b', 'w'), repeat = i):
            outcomes.append(list(key) )
            
    # next guess is max of the min scores.
    nextGuessScore = 0
    possibleNextGuesses = []

    for i, guess in enumerate(globalCodes):
        #print(i + 1)
        #print(guess)
        hitsPerOutcome = []
        for i in range(len(outcomes)):
            hitsPerOutcome.append(0)

        ## calculates number of hits for each value of outcome, for a given guess
        for node in currentCodes:
           codeKeys = setKeyPegs(node, guess)
           pos = outcomes.index(codeKeys)
           hitsPerOutcome[pos] += 1

        score = len(currentCodes) - max(hitsPerOutcome)

        if score == nextGuessScore:
            possibleNextGuesses.append(guess)
        elif score > nextGuessScore:
            possibleNextGuesses = [guess]
            nextGuessScore = score
            
    # select a guess from the possible next guesses. choose from currentCodes if possible.
    guessesInCurrentCodes = []
    for guess in possibleNextGuesses:
        if guess in currentCodes:
            guessesInCurrentCodes.append(guess)
            break           # since we need only the 1st guess

    if guessesInCurrentCodes != []:
        nextGuess = guessesInCurrentCodes[0]
    else:
        nextGuess = possibleNextGuesses[0]
        
    return nextGuess

def getNewCodes(codes, guess, guessKeys):
    newCodesList = []

    for code in codes:
        keys = []
        keys = setKeyPegs(guess, code)
        if keys == guessKeys:
            newCodesList.append(code)    

    return newCodesList

def createCodes(numPegs, numColors):
    codes = []

    for code in product(range(1, numColors + 1), repeat = numPegs):
        codes.append(code)

    return codes

def setKeyPegs(guess, answer):
    tempGuess = []
    tempAnswer = []
    tempKeys = []
    numPegs = len(guess)

    for peg in guess:
        tempGuess.append(peg)

    for peg in answer:
        tempAnswer.append(peg)

    # add black key pegs.
    for pos in range(numPegs):
        if (tempGuess[pos] == tempAnswer[pos]):
            tempKeys.append('b')
            tempGuess[pos] = None
            tempAnswer[pos] = None
            
    # add white key pegs.
    for pos, peg in enumerate(tempGuess):
        for pos2, peg2 in enumerate(tempAnswer):
            if (peg == peg2) and (peg != None) and (peg2 != None):
                tempKeys.append('w')
                tempGuess[pos] = None 
                tempAnswer[pos2] = None
                break       # break from inner loop
    return tempKeys
    
def checkWin(key, numPegs, turn):
    correctKey = []

    for peg in range(numPegs):
        correctKey.append('b')

    if key == correctKey:
        print("key pegs: " + str(key))
        return True
    else:
        print("key pegs: " + str(key))
        if turn != 0:
            print("Try again")
        return False

if __name__ == '__main__':
    main()
