import random
import numpy

allColors = range(1,numColors+1)
numPegs = 4

def main():
    global allColors
    global numPegs
    # prompt user for number of pegs and colors.
    numPegs = 4
    numColors = 0
    #while (numPegs < 4) or (numPegs > 8):
     #   numPegs = int(input("Number of pegs (4-8): "))

    while (numColors < 6) or (numColors > 12):
        numColors = int(input("Number of colors (6-12): "))
        
    allColors = range(1,numColors+1)
    answer = []
    keyPegs = []
    playerGuess = []
    won = False
    numBlack = 0
    numWhite = 0
    
    #generate the secret code
    for pos in range(numPegs):
        answer.append(random.randint(1, numColors))
        
    for pos in range(numPegs):
        playerGuess.append(random.randint(1, numColors))

    playerGuess = [1,1,2,2]

    CFG = playerGuess
    turns = 1
    # determine key pegs for the initial guess.
    CFGkeyPegs, CFGnumBlack, CFGnumWhite = getKeyPegs(playerGuess, answer)
    scoreCFG = getScore(CFGnumBlack, CFGnumWhite)
    print("The secret code is: " + str(answer))
    
    print("----------------------------------------")
    # play the guess and get new code list.
    print("Player's guess: " + str(playerGuess))
    if scoreCFG==0:
        cfgColors = []
        for i in CFG:
            if i not in cfgColors:
                cfgColors.append(i)
        for i in cfgColors:
                allColors.remove(i)
        playerGuess = []
        turns+=1
        for pos in range(numPegs):
            rand = random.sample(set(allColors),1)
            playerGuess.append(rand[0])
                
    if scoreCFG==13:
        print("The secret answer is: " + str(answer))
        return
    
    won = False
    
    while not won:
        npg = getNewGuessHillClimbing(CFG, CFGkeyPegs, CFGnumBlack, CFGnumWhite, scoreCFG)
        turns += 1
        print('next guess: ' + str(npg))
        print("Determining keys for new guess...")

        #NPG scores
        npgkeyPegs,temp_npg_numBlack,temp_npg_numWhite = getKeyPegs(npg, answer)
        print "keyPegs"+str(npgkeyPegs)
        scoreNPG = getScore(temp_npg_numBlack,temp_npg_numWhite)

        #CFG scores
        cfgkeyPegs, temp_cfg_numBlack, temp_cfg_numWhite = getKeyPegs(CFG, answer)
        scoreCFG = getScore(temp_cfg_numBlack, temp_cfg_numWhite)

        if (scoreNPG==0):
            cfgColors = []
            for i in npg:
                if i not in cfgColors:
                    cfgColors.append(i)
            for i in cfgColors:
                if i in allColors:
                    allColors.remove(i)
            CFG=[]
            for pos in range(numPegs):
                temp = random.sample(set(allColors), 1)
                CFG.append(temp[0])
            keyPegs, numBlack, numWhite = getKeyPegs(CFG, answer)

                
        print ('NPG score:'+str(scoreNPG))
        print ('CFG score:'+str(scoreCFG))
        if(scoreNPG > scoreCFG):
            CFG = npg
            CFGkeyPegs, CFGnumBlack, CFGnumWhite = npgkeyPegs,temp_npg_numBlack,temp_npg_numWhite

        if scoreNPG == 13:
            won = True

    print('\n')
    print('Finished!')
    print("The guess is: " + str(npg))
    print("The secret answer is: " + str(answer))
    print("Solved in " + str(turns) + " turn(s)!")

    return

    
'''cfg = current favourite guess
npg = next potential guess '''
def getNewGuessHillClimbing(lastGuess,lastkeyPegs,cfgnumBlack,cfgnumWhite, scoreCFG):
    global allColors
    global numPegs
    cfg = lastGuess
    count =0
    while True:
        npg = newPotentialGuess(cfg,cfgnumBlack,cfgnumWhite, scoreCFG)
        keyPegs,numBlack,numWhite = getKeyPegs(npg, cfg)
        print "keyPegs"+str(keyPegs)
        print "LastkeyPegs"+str(lastkeyPegs)
        if (keyPegs==lastkeyPegs):
            return npg
        #else:
            # count+=1
            # if count > 3:
            #     count =0
            #     cfg=[]
            #     for pos in range(numPegs):
            #         temp = random.sample(set(allColors), 1)
            #         cfg.append(temp[0])
            #     keyPegs, numBlack, numWhite = setKeyPegs(cfg, answer)

    
def newPotentialGuess(cfg,numBlack,numWhite, scoreCFG):
    global allColors
    global numColors
    localColors = range(1,numColors+1)
    npg = [0,0,0,0]
    init = [0,1,2,3]
    rand = random.sample(set([0,1,2,3]), numBlack)
    for pos in rand:
        npg[pos]=cfg[pos]
    for i in rand:
        init.remove(i)
    randWhite=random.sample(set(init), numWhite)


    for pos in randWhite:
        r=random.sample(set(init), 1)
        r=r[0]
        if(pos!=r):
            npg[r]=cfg[pos]
            init.remove(r)
        else:
            r = random.sample(set(init), 1)
            r = r[0]
            npg[r] = cfg[pos]
            init.remove(r)

    #find distinct
    cfgColors = []
    for i in cfg:
        if i not in cfgColors:
            cfgColors.append(i)

    p = getProbabilityDist(cfg, npg)


    for pos in init:
        npg[pos] = numpy.random.choice(numpy.array(allColors), p=p)
         
    return npg
'''heuristtic = [0,0] = 0, [0,1]=1,[1,0]=2,[0,2]=3,[1,1]=4,[2,0]=5, [0,3]=6,[1,2]=7,[2,1]=8,[3,0]=9,[0,4]=10, 
[1,3] = 11, [2,2] = 12 and [4,0] = 13'''

def getProbabilityDist(cfg, npg):
    global allColors
    prob_dict = {}
    for i in allColors:
        prob_dict.update({i:0.00})

    p=prob_dict

    for i in cfg:
        if i in allColors:
            p[i] += 145

    for i in npg:
        if i!=0 and i in allColors:
            p[i] -= 100

    for i in allColors:
        p[i] = 100-p[i]
        if p[i]<0:
            p[i] = 1

    total_value = 0

    for key,value in p.items():
        total_value+=value

    for key,value in p.iteritems():
        p[key] = (value/total_value)

    total_percent = 0

    for key,value in p.iteritems():
        total_percent += value

    amount_less_to_cent = 1 - total_percent

    for key,value in p.iteritems():
        p[key] += amount_less_to_cent
        break

    return p.values()


def getScore(numBlack,numWhite):
    scoreMap = {"00":0,"01":1,"10":2,"02":3,"11":4,"20":5,"03":6,"12":7,"21":8,"30":9,"04":10,"13":11,"22":12,"40":13}
    scoreStr = str(numBlack)+str(numWhite)
    return scoreMap[scoreStr]


def getKeyPegs(guess, answer):
    tempGuess = []
    tempAnswer = []
    tempKeys = []
#    numPegs = len(guess)
    numPegs = 4
    numBlack = 0
    numWhite = 0

    for peg in guess:
        tempGuess.append(peg)

    for peg in answer:
        tempAnswer.append(peg)

    # add black key pegs.
    for pos in range(numPegs):
        if (tempGuess[pos] == tempAnswer[pos]):
            tempKeys.append('b')
            numBlack +=1
            tempGuess[pos] = None
            tempAnswer[pos] = None
            
    # add white key pegs.
    for pos, peg in enumerate(tempGuess):
        for pos2, peg2 in enumerate(tempAnswer):
            if (peg == peg2) and (peg != None) and (peg2 != None):
                tempKeys.append('w')
                numWhite +=1
                tempGuess[pos] = None 
                tempAnswer[pos2] = None
                break       # break from inner loop
    return tempKeys,numBlack,numWhite


if __name__ == '__main__':
    main()
