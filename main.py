import random

allCodes = []
answer = []
keyPegs = []

# set initial guess to 1122
guess = [1, 1, 2, 2]

# create the entire set of 1296 possible codes.
for peg1 in range(1, 7):
    for peg2 in range(1, 7):
        for peg3 in range(1, 7):
            for peg4 in range(1, 7):
                allCodes.append([peg1, peg2, peg3, peg4])

# randomly generate the correct answer.
for pos in range(4):
    answer.append(random.randint(1, 6))

print(answer)



def setKeyPegs(guess, answer, keys):
    correctPositions = [False, False, False, False]
    whiteKeyPegs = 0

    for guessPos, guessNum in enumerate(guess):
        for answerPos, answerNum in enumerate(answer):
            if (guessNum == answerNum):
                if (guessPos == answerPos):
                    correctPositions[guessPos] = True

    for guess in correctPositions:
        if guess:
            keys.append('b')
            whiteKeyPegs -= 1
           
