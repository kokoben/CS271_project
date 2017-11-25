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
    guess = [1, 1, 2, 2]

    # randomly generate the correct answer.
    for pos in range(4):
        answer.append(random.randint(1, 6))

    # play the guess.
    playGuess(guess, answer, keyPegs, numTurns)
    checkWin(keyPegs)

def playGuess(gue, ans, key, turns):
    setKeyPegs(gue, ans, key)
    turns += 1

def setKeyPegs(guess, answer, keys):
    nums = []
    
    for peg in answer:
        nums.append(peg)

    for guessPos, guessNum in enumerate(guess):
        for answerPos, answerNum in enumerate(answer):
            if guessNum in nums:
                if guessPos == answerPos:
                    keys.append('b')
                keys.append('w')
                nums.remove(guessNum)
                break

def checkWin(key):
    if key == ['b', 'b', 'b', 'b']:
        print("Guesser wins!")
        return True
    else:
        print("Try again")
        return False


if __name__ == '__main__':
    main()
