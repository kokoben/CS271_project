import random

def main():
    allCodes = []
    answer = []
    keyPegs = []
    numTurns = 0

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
    playGuess(playerGuess, answer, keyPegs, numTurns)
    checkWin(keyPegs)

def playGuess(guess, ans, key, turns):
    setKeyPegs(guess, ans, key)
    turns += 1

def setKeyPegs(guess, answer, keys):
    nums = []
    tempKeys = []
    keyBuilder = [['n', 0, 0], ['n', 0, 0], ['n', 0, 0], ['n', 0, 0]]
    # keyBuilder indicates which key peg to add for each guess, if any.
    # w = white, b = black, n = none
    # second position = which value was matched.
    # third position = which position in answer the value was found.

    for peg in answer:
        nums.append(peg)
    print(nums)
    print(guess)

    for guessPos, guessNum in enumerate(guess):
        for answerPos, answerNum in enumerate(answer):
            if guessNum == answerNum:
                if guessPos == answerPos:
                    keyBuilder[guessPos] = ['b', guessNum, answerPos]
                else:
                    if keyBuilder[guessPos][0] == 'n':
                        keyBuilder[guessPos] = ['w', guessNum, answerPos]
    print(keyBuilder)

    # construct the final key peg sequence.
    # first add black pegs.
    for peg in keyBuilder:
        if peg[0] == 'b':
            tempKeys.append(peg)
    
    # then reassign any white pegs to 'none' that were assigned for the positions that are now known to be black pegs.
    for peg in keyBuilder:
        for peg2 in tempKeys:
            if peg[0] == 'w':
                if (peg2[0] == 'b') and (peg[1] == peg2[1]):
                    peg[0] = 'n'
    print(keyBuilder)
                
    # then add white pegs.
    for peg in keyBuilder:
        if peg[0] == 'w':
            tempKeys.append(peg)

    # remove duplicate white pegs.
    for peg in tempKeys:
        if peg not in keys:
            keys.append(peg)

def checkWin(key):
    if key == ['b', 'b', 'b', 'b']:
        print("Guesser wins!")
        return True
    else:
        print(key)
        print("Try again")
        return False


if __name__ == '__main__':
    main()
