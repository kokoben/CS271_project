import random
import numpy

global turnsList
numColors = 0
allColors = range(1, numColors + 1)
allPreviousGuesses = [[]]
sumturns = 0
turnsList = []


def main():
    global allColors
    global numColors
    global allPreviousGuesses
    # prompt user for number of pegs and colors.
    numPegs = 0
    numColors = 0
    while (numPegs < 4) or (numPegs > 8):
       numPegs = int(input("Number of pegs (4-8): "))

    while (numColors < 6) or (numColors > 12):
        numColors = int(input("Number of colors (6-12): "))

    allColors = range(1, numColors + 1)
    answer = []
    playerGuess = []
    blackPegs = [0]  ## contains black pegs for all previous guesses
    whitePegs = [0]  ## contains black pegs for all previous guesses
    won = False

    # generate the secret code
    for pos in range(numPegs):
        answer.append(random.randint(1, numColors))

    print("The secret code is: " + str(answer))

    for pos in range(numPegs):
        playerGuess.append(random.randint(1, 2))

    cfg = playerGuess

    # determine key pegs and score for initial guess.
    CFGkeyPegs, CFGnumBlack, CFGnumWhite = getKeyPegs(playerGuess, answer)
    blackPegs.append(CFGnumBlack)
    whitePegs.append(CFGnumWhite)
    scoreCFG = getScore(CFGnumBlack, CFGnumWhite)
    allPreviousGuesses.append(cfg)
    turns = 1

    print("----------------------------------------")
    print("Player's first guess: " + str(playerGuess))

    if (numPegs == 4 and scoreCFG == 14):
        print("The secret answer is: " + str(answer))
        return
    if (numPegs == 5 and scoreCFG == 20):
        print("The secret answer is: " + str(answer))
        return
    if (numPegs == 6 and scoreCFG == 27):
        print("The secret answer is: " + str(answer))
        return
    if (numPegs == 7 and scoreCFG == 35):
        print("The secret answer is: " + str(answer))
        return
    if (numPegs == 8 and scoreCFG == 43):
        print("The secret answer is: " + str(answer))
        return

    print('Player guess: ' + str(cfg) + ' keyPegs' + str(CFGkeyPegs) + ' score ' + str(scoreCFG))
    won = False

    while not won:

        # NPG
        npg = newPotentialGuess(cfg, CFGnumBlack, CFGnumWhite, scoreCFG)
        loop_count = 0
        while not is_consistent(npg, allPreviousGuesses,blackPegs,whitePegs,turns) and loop_count<1000:
            npg = newPotentialGuess(cfg, CFGnumBlack, CFGnumWhite, scoreCFG)
            loop_count+=1
        allPreviousGuesses.append(npg)
        turns += 1

        # NPG scores
        npgkeyPegs, temp_npg_numBlack, temp_npg_numWhite = getKeyPegs(npg, answer)
        blackPegs.append(temp_npg_numBlack)
        whitePegs.append(temp_npg_numWhite)
        scoreNPG = getScore(temp_npg_numBlack, temp_npg_numWhite)

        print('Player guess: ' + str(npg) + ' keyPegs' + str(npgkeyPegs) + ' score ' + str(scoreNPG))

        if (numPegs == 4 and scoreNPG == 14):
            won = True
        elif (numPegs == 5 and scoreNPG == 20):
            won = True
        elif (numPegs == 6 and scoreNPG == 27):
            won = True
        elif (numPegs == 7 and scoreNPG == 35):
            won = True
        elif (numPegs == 8 and scoreNPG == 43):
            won = True
        elif (scoreNPG == 0):
            cfgColors = []
            for i in npg:
                if i not in cfgColors:
                    cfgColors.append(i)
            for i in cfgColors:
                if i in allColors:
                    allColors.remove(i)
            cfg = []
            # take first 2 distinct colors
            allColors2num = [allColors[0], allColors[1]]
            for pos in range(numPegs):
                temp = random.sample(allColors2num, 1)
                cfg.append(temp[0])

            loop_count = 0
            while not is_consistent(cfg,allPreviousGuesses,blackPegs,whitePegs,turns) and loop_count<1000:
                cfg = []
                loop_count+=1
                for pos in range(numPegs):
                    temp = random.sample(allColors2num, 1)
                    cfg.append(temp[0])

            CFGkeyPegs, CFGnumBlack, CFGnumWhite = getKeyPegs(cfg, answer)
            scoreCFG = getScore(CFGnumBlack, CFGnumWhite)
        elif (scoreNPG >= scoreCFG):
            scoreCFG = scoreNPG
            cfg = npg
            CFGkeyPegs, CFGnumBlack, CFGnumWhite = npgkeyPegs, temp_npg_numBlack, temp_npg_numWhite

    print('\n')
    print('Finished!')
    print("The guess is: " + str(npg))
    print("The secret answer is: " + str(answer))
    print("Solved in " + str(turns) + " turn(s)!")

    return turns


'''cfg = current favourite guess
npg = next potential guess '''


def getNewGuessHillClimbing(lastGuess, lastkeyPegs, cfgnumBlack, cfgnumWhite, scoreCFG):
    global allColors
    cfg = lastGuess
    global allPreviousGuesses
    while True:
        npg = newPotentialGuess(cfg, cfgnumBlack, cfgnumWhite, scoreCFG)
        keyPegs, numBlack, numWhite = getKeyPegs(npg, cfg)
        # print "keyPegs"+str(keyPegs)
        # print "LastkeyPegs"+str(lastkeyPegs)
        if (keyPegs == lastkeyPegs) and npg not in allPreviousGuesses:
            return npg
            # else:
            # count+=1
            # if count > 3:
            #     count =0
            #     cfg=[]
            #     for pos in range(numPegs):
            #         temp = random.sample(set(allColors), 1)
            #         cfg.append(temp[0])
            #     keyPegs, numBlack, numWhite = setKeyPegs(cfg, answer)


def is_consistent(npg, allPreviousGuesses, blackPegs, whitePegs, turns):
    blackPegsDiff = 0
    whitePegsDiff = 0
    for g in range(1,turns+1):
        keyPegs, b, w = getKeyPegs(allPreviousGuesses[g],npg)
        blackPegsDiff+=abs(blackPegs[g] - b)
        whitePegsDiff += abs(whitePegs[g] - w)

    if(blackPegsDiff>0 or whitePegsDiff>0):
        return False
    else:
        return True


def newPotentialGuess(cfg, numBlack, numWhite, scoreCFG):
    global allColors
    global numColors
    npg = range(0, len(cfg))
    index = range(0, len(cfg))
    rand = random.sample(index, numBlack)
    colors_to_remove = []
    for pos in rand:
        npg[pos] = cfg[pos]
        colors_to_remove.append(npg[pos])
    for i in rand:
        index.remove(i)
    randWhite = random.sample(index, numWhite)

    for pos in randWhite:
        r = pos
        while (pos == r):
            r = random.sample(index, 1)
            r = r[0]

        npg[r] = cfg[pos]
        colors_to_remove.append(npg[r])
        index.remove(r)

    # find distinct
    cfgColors = []
    for i in allColors:
        if i not in colors_to_remove:
            cfgColors.append(i)

    #p = getProbabilityDist(cfg, npg)

    for pos in index:
        npg[pos] = numpy.random.choice(numpy.array(allColors))

    return npg


def getProbabilityDist(cfg, npg):
    global allColors
    prob_dict = {}
    for i in allColors:
        prob_dict.update({i: 0.00})

    p = prob_dict

    for i in cfg:
        if i in allColors:
            p[i] += 145

    for i in npg:
        if i != 0 and i in allColors:
            p[i] -= 100

    for i in allColors:
        p[i] = 100 - p[i]
        if p[i] < 0:
            p[i] = 1

    total_value = 0

    for key, value in p.items():
        total_value += value

    for key, value in p.iteritems():
        p[key] = (value / total_value)

    total_percent = 0

    for key, value in p.iteritems():
        total_percent += value

    amount_less_to_cent = 1 - total_percent

    for key, value in p.iteritems():
        p[key] += amount_less_to_cent
        break

    return p.values()


def getScore(numBlack, numWhite):
    scoreMap = {"00": 0, "01": 1, "10": 2, "02": 3, "11": 4, "20": 5, "03": 6, "12": 7, "21": 8, "30": 9, "04": 10, "13": 11, "22": 12, "31": 13, "40": 14, "05": 15, "14": 16, "23": 17, "32": 18, "41": 19, "50": 20, "06": 21, "15": 22, "24": 23, "33": 24, "42": 25, "51": 26, "60": 27, "07": 28, "16": 29, "25": 30, "34": 31, "43": 32, "52": 33, "61": 34, "70": 35, "08": 36, "17": 37, "26": 38,
                "35": 39, "44": 40, "53": 41, "62": 42, "80": 43}
    scoreStr = str(numBlack) + str(numWhite)
    return scoreMap[scoreStr]


def getKeyPegs(guess, answer):
    tempGuess = []
    tempAnswer = []
    tempKeys = []
    numBlack = 0
    numWhite = 0
    numPegs = len(answer)

    for peg in guess:
        tempGuess.append(peg)

    for peg in answer:
        tempAnswer.append(peg)

    # add black key pegs.
    for pos in range(numPegs):
        if (tempGuess[pos] == tempAnswer[pos]):
            tempKeys.append('b')
            numBlack += 1
            tempGuess[pos] = None
            tempAnswer[pos] = None

    # add white key pegs.
    for pos, peg in enumerate(tempGuess):
        for pos2, peg2 in enumerate(tempAnswer):
            if (peg == peg2) and (peg != None) and (peg2 != None):
                tempKeys.append('w')
                numWhite += 1
                tempGuess[pos] = None
                tempAnswer[pos2] = None
                break  # break from inner loop
    return tempKeys, numBlack, numWhite


if __name__ == '__main__':
    main()