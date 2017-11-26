import random

def main():
    allCodes = []
    answer = []
    keyPegs = []

    # create the entire set of 1296 possible codes.
    for peg1 in range(1, 7):
        for peg2 in range(1, 7):
            for peg3 in range(1, 7):
                for peg4 in range(1, 7):
                    allCodes.append([peg1, peg2, peg3, peg4])

    # set initial guess to 1122
    playerGuess = [1, 1, 2, 2]

    # randomly generate the correct answer.
    for pos in range(4):
        answer.append(random.randint(1, 6))

    # play the guess.
    print(answer)
    print(playerGuess)
    playGuess(playerGuess, answer, keyPegs)
    checkWin(keyPegs)
    allCodes = getNewCodes(allCodes, playerGuess, keyPegs, answer)

def getNewCodes(codes, lastGuess, lastGuessKeys, answer):
    newCodesList = []

    for code in codes:
        keys = []
        playGuess(lastGuess, code, keys)
        if keys == lastGuessKeys:
            newCodesList.append(code)    

    return newCodesList

def playGuess(guess, ans, keys):
    setKeyPegs(guess, ans, keys)

def setKeyPegs(guess, answer, keys):
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
    
    for peg in tempKeys:
        keys.append(peg)
    
def checkWin(key):
    if key == ['b', 'b', 'b', 'b']:
        print(key)
        print("Guesser wins!")
        return True
    else:
        print(key)
        print("Try again")
        return False

if __name__ == '__main__':
    main()
