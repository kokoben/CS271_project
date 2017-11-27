import random

def main():
    globalAllCodes = []
    allCodes = []
    answer = []
    keyPegs = []
    turn = 1
    won = False

    # create the entire set of 1296 possible codes.
    createCodes(allCodes)
    # do it again for the codes that will be used in the minimax step. this list never shrinks.
    createCodes(globalAllCodes)
    # set initial guess to 1122
    playerGuess = [1, 1, 2, 2]
    # randomly generate the correct answer.
    for pos in range(4):
        answer.append(random.randint(1, 6))

    print("The secret code is: " + str(answer))

    while not won:
        print("Turn " + str(turn) + ":")
        print("----------------------------------------")
        # play the guess and get new code list.
        print("Player's guess: " + str(playerGuess))
        # allCodes = playGuess(playerGuess, answer, keyPegs, allCodes)
        keyPegs = setKeyPegs(playerGuess, answer)
        allCodes = getNewCodes(allCodes, playerGuess, keyPegs)
        won = checkWin(keyPegs)
        if won:
            break
        print("Number of possible codes left: " + str(len(allCodes)))
        playerGuess = applyMinimax(globalAllCodes, allCodes, playerGuess, keyPegs, answer, 4) 
        print('next guess: ' + str(playerGuess))
        turn += 1

    print("The secret code is: " + str(playerGuess))
    print("Solved!")

    return 

def applyMinimax(globalCodes, currentCodes, lastGuess, lastGuessKeys, answer, numPegs):
    # generate all possible key combinations.
    outcomes = []
    
    for i in range(numPegs):
        for j in range(numPegs):
            for k in range(numPegs):
                for l in range(numPegs):
                    outcomes.append([i, j, k, l])
            
    # next guess is max of the min scores.
    nextGuessScore = 0
    possibleNextGuesses = []

    for i, guess in enumerate(currentCodes):
        print(i + 1)
        print(guess)
        hitsPerOutcome = []
        for i in range(len(outcomes)):
            hitsPerOutcome.append(0)

        for pos, outcome in enumerate(outcomes):
            codeKeys = []
            for solution in globalCodes:
               codeKeys = setKeyPegs(guess, solution)
               if codeKeys == outcome:
                hitsPerOutcome[pos] += 1
            score = len(currentCodes) - max(hitsPerOutcome)

        if score == nextGuessScore:
            possibleNextGuesses.append(guess)
        elif score > nextGuessScore:
            possibleNextGuesses = [guess]
            
    # select a guess from the possible next guesses. choose from currentCodes if possible.
    guessesInCurrentCodes = []
    for guess in possibleNextGuesses:
        if guess in currentCodes:
            guessesInCurrentCodes.append(guess)

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

def createCodes(codes):
    for peg1 in range(1, 7):
        for peg2 in range(1, 7):
            for peg3 in range(1, 7):
                for peg4 in range(1, 7):
                    codes.append([peg1, peg2, peg3, peg4])

def setKeyPegs(guess, answer):
    tempGuess = []
    tempAnswer = []
    tempKeys = []

    for peg in guess:
        tempGuess.append(peg)

    for peg in answer:
        tempAnswer.append(peg)

    # add black key pegs. 
    for pos, peg in enumerate(tempGuess):
        for pos2, peg2 in enumerate(tempAnswer):
            if (peg == peg2) and (pos == pos2) and (peg != 'n') and (peg2 != 'n'):
                tempKeys.append('b')
                tempGuess[pos] = 'n'
                tempAnswer[pos2] = 'n'
            
    # add white key pegs.
    for pos, peg in enumerate(tempGuess):
        for pos2, peg2 in enumerate(tempAnswer):
            if (peg == peg2) and (peg != 'n') and (peg2 != 'n'):
                tempKeys.append('w')
                tempGuess[pos] = 'n'
                tempAnswer[pos2] = 'n'
    
    return tempKeys
    
def checkWin(key):
    if key == ['b', 'b', 'b', 'b']:
        return True
    else:
        print("key pegs: " + str(key))
        print("Try again")
        return False

if __name__ == '__main__':
    main()
