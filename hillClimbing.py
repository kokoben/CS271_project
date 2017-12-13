#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 18:07:16 2017

@author: ahuddar
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 18:02:28 2017

@author: ahuddar
"""

import random
import numpy

global turnsList
numColors = 0
allColors = range(1,numColors+1)
allPreviousGuesses = []
sumturns = 0
turnsList = []

def main():
    global allColors
    global numColors
    global allPreviousGuesses
    # prompt user for number of pegs and colors.
    numPegs = 4
    numColors = 6
    #while (numPegs < 4) or (numPegs > 8):
    #    numPegs = int(input("Number of pegs (4-8): "))

    #while (numColors < 6) or (numColors > 12):
    #numColors = int(input("Number of colors (6-12): "))

    #import pdb
    #pdb.set_trace()

    allColors = range(1,numColors+1)
    answer = []
    playerGuess = []
    won = False

    #generate the secret code
    for pos in range(numPegs):
        answer.append(random.randint(1, numColors))

    for pos in range(numPegs):
        playerGuess.append(random.randint(1,2))
    
    '''Problem1 : 4 pegs/6 colors
    colors: A,B,C,D,E,F
    secret code: F,C,E,D

    Problem2 : 4 pegs/6 colors
    colors: A,B,C,D,E,F
    secret code: E,A,C,B

    Problem3 : 6 pegs/9 colors
    colors: A,B,C,D,E,F,G,H,I
    secret code: H,I,I,F,D,A
    
    Problem4 : 6 pegs/9 colors
    colors: A,B,C,D,E,F,G,H,I
    secret code: I,D,C,B,F,A
    
    Problem5 : 8 pegs/12 colors
    colors: A,B,C,D,E,F,G,H,I,J,K,L
    secret code: L,H,I,G,L,L,K,E
    
    Problem6 : 8 pegs/12 colors
    colors: A,B,C,D,E,F,G,H,I,J,K,L
    secret code: K,K,A,C,L,I,G,F'''
       
    #answer = [6,3,5,4]
    #answer = [5,1,3,2]
    #answer = [7,9,9,6,4,1]
    #answer = [9,4,3,2,6,1]
    #answer = [12,8,9,7,12,12,11,5]
    #answer = [11,11,1,3,12,9,7,6]
    
    #playerGuess = [1,1,2,2]

    cfg = playerGuess
    turns = 1

    # determine key pegs and score for initial guess.
    CFGkeyPegs, CFGnumBlack, CFGnumWhite = getKeyPegs(playerGuess, answer)
    scoreCFG = getScore(CFGnumBlack, CFGnumWhite)
    print("The secret code is: " + str(answer))

    print("----------------------------------------")
    print("Player's first guess: " + str(playerGuess))

    # if score is 0, generate new random CFG
    if scoreCFG==0:
        cfgColors = []
        for i in cfg:
            if i not in cfgColors:
                cfgColors.append(i)
        for i in cfgColors:
                allColors.remove(i)
        playerGuess = []
        turns+=1
        cfg=[]
        if (len(allColors)!=1):
            allColors2num = [allColors[0],allColors[1]]
            for pos in range(numPegs):
                temp = random.sample(set(allColors2num), 1)
                cfg.append(temp[0])
        else :
            for pos in range(numPegs):
                temp = random.sample(set(allColors), 1)
                cfg.append(temp[0])
                    
    allPreviousGuesses.append(cfg)

    if (numPegs==4 and scoreCFG==14):
        print("The secret answer is: " + str(answer))
        return
    if (numPegs==5 and scoreCFG==20):
        print("The secret answer is: " + str(answer))
        return
    if (numPegs==6 and scoreCFG==27):
        print("The secret answer is: " + str(answer))
        return
    if (numPegs==7 and scoreCFG==35):
        print("The secret answer is: " + str(answer))
        return
    if (numPegs==8 and scoreCFG==43):
        print("The secret answer is: " + str(answer))
        return
    
    won = False


    while not won:
        #CFG scores
        #print "CFG = "+str(cfg)
        #cfgkeyPegs, temp_cfg_numBlack, temp_cfg_numWhite = getKeyPegs(cfg, answer)
        #scoreCFG = getScore(temp_cfg_numBlack, temp_cfg_numWhite)
        #print "CFG comparison with secret code CFG Keypegs "+str(cfgkeyPegs)
        #print "CFG keyPegs score with secret code CFG score "+str(scoreCFG)
        print('cfg: ' + str(cfg)+'cfg keyPegs'+str(CFGkeyPegs)+'cfg score '+str(scoreCFG))
        #NPG
        npg = getNewGuessHillClimbing(cfg, CFGkeyPegs, CFGnumBlack, CFGnumWhite, scoreCFG)

        allPreviousGuesses.append(npg)

        #NPG scores
        npgkeyPegs,temp_npg_numBlack,temp_npg_numWhite = getKeyPegs(npg, answer)
        scoreNPG = getScore(temp_npg_numBlack,temp_npg_numWhite)
        turns += 1
        print('npg: ' + str(npg)+'NPG keyPegs'+str(npgkeyPegs)+'NPG score '+str(scoreNPG))

        #print "turns = "+str(turns)
        #print "NPG comparison with secret code NPG keyPegs "+str(npgkeyPegs)
        #print "NPG keyPegs score with secret code NPG score "+str(scoreNPG)

        if (numPegs==4 and scoreNPG==14):
            won = True
        if (numPegs==5 and scoreNPG==20):
            won = True
        if (numPegs==6 and scoreNPG==27):
            won = True
        if (numPegs==7 and scoreNPG==35):
            won = True
        if (numPegs==8 and scoreNPG==43):
            won = True


        if (scoreNPG==0):
            cfgColors = []
            for i in npg:
                if i not in cfgColors:
                    cfgColors.append(i)
            for i in cfgColors:
                if i in allColors:
                    allColors.remove(i)
            cfg=[]
            #take first 2 distinct colors
            allColors2num = [allColors[0],allColors[1]]
            for pos in range(numPegs):
                temp = random.sample(set(allColors2num), 1)
                cfg.append(temp[0])
            CFGkeyPegs, CFGnumBlack, CFGnumWhite = getKeyPegs(cfg, answer)
            scoreCFG = getScore(CFGnumBlack, CFGnumWhite)



        #print("Determining keys for new guess...")
        #print ('NPG score:'+str(scoreNPG))
        #print ('CFG score:'+str(scoreCFG))
        if(scoreNPG >= scoreCFG):
            scoreCFG = scoreNPG
            cfg = npg
            CFGkeyPegs, CFGnumBlack, CFGnumWhite = npgkeyPegs,temp_npg_numBlack,temp_npg_numWhite

        #if scoreNPG == 13:
         #   won = True

    print('\n')
    print('Finished!')
    print("The guess is: " + str(npg))
    print("The secret answer is: " + str(answer))
    print("Solved in " + str(turns) + " turn(s)!")

    return turns


'''cfg = current favourite guess
npg = next potential guess '''
def getNewGuessHillClimbing(lastGuess,lastkeyPegs,cfgnumBlack,cfgnumWhite, scoreCFG):
    global allColors
    cfg = lastGuess
    global allPreviousGuesses
    while True:
        npg = newPotentialGuess(cfg,cfgnumBlack,cfgnumWhite, scoreCFG)
        keyPegs,numBlack,numWhite = getKeyPegs(npg, cfg)
        #print "keyPegs"+str(keyPegs)
        #print "LastkeyPegs"+str(lastkeyPegs)
        if (keyPegs==lastkeyPegs) and npg not in allPreviousGuesses:
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
    npg = range(0,len(cfg))
    index = range(0,len(cfg))
    rand = random.sample(index, numBlack)
    for pos in rand:
        npg[pos]=cfg[pos]
    for i in rand:
        index.remove(i)
    randWhite=random.sample(index, numWhite)


    for pos in randWhite:
        r=random.sample(index, 1)
        r=r[0]
        if(pos!=r):
            npg[r]=cfg[pos]
            index.remove(r)
        else:
            r = random.sample(index, 1)
            r = r[0]
            npg[r] = cfg[pos]
            index.remove(r)

    #find distinct
    cfgColors = []
    for i in cfg:
        if i not in cfgColors:
            cfgColors.append(i)

    p = getProbabilityDist(cfg, npg)


    for pos in index:
        npg[pos] = numpy.random.choice(numpy.array(allColors), p=p)

    return npg

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

'''heuristic for 5numpegs = [0,0]=0; [0,1]=1; [1,0]=2; [0,2]=3; [1,1]=4; [2,0]=5; [0,3]=6; [1,2]=7;
[2,1]=8; [3,0]=9; [0,4]=10; [1,3]=11; [2,2]=12; [3,1]=13; [4,0]=14; [0,5]=15; [1,4]=16; [2,3]=17;
[3,2]=18; [5,0]=19 '''

def getScore(numBlack,numWhite):
    scoreMap = {"00":0,"01":1,"10":2,"02":3,"11":4,"20":5,"03":6,"12":7,"21":8,"30":9,"04":10,"13":11,"22":12,"31":13,"40":14,"05":15,"14":16,"23":17,"32":18,"41":19,"50":20,"06":21,"15":22,"24":23,"33":24,"42":25,"51":26,"60":27,"07":28,"16":29,"25":30,"34":31,"43":32,"52":33,"61":34,"70":35,"08":36,"17":37,"26":38,"35":39,"44":40,"53":41,"62":42,"80":43}
    scoreStr = str(numBlack)+str(numWhite)
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
        
    
