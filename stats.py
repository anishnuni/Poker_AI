import numpy as np
import json
import random

deck = []
for j in range(0,4):
    for i in range(1,14):
        deck.append([i,j])


#bvalue returns the value of the player's hand at the end of the round (represented by a number) given the table.
#The higher the number, the better the hand
#this is used to compare hands when the game simulation is run
def bvalue(hand,table):
    set = table[:]
    set.extend(hand)
    value = 0
    nnumbers = np.zeros(14)
    nsuit = np.zeros(4)
    nlist = []
    numbers = []
    done = 0
    for i in range(0,7):
        [x,y] = set[i]
        nnumbers[x] += 1
        nsuit[y] += 1
        nlist.append(x)
        numbers.append(x)
        if done == 0 and x == 1:
            numbers.append(14)
            done = 1
    nlist.sort()
    numbers.sort()
    if np.amax(nsuit) >= 5:
        suittype = np.argmax(nsuit)
        fhand_nlist = []
        fhand_done = 0
        for run in range(0,7):
            [x,y] = set[run]
            if y == suittype:
                fhand_nlist.append(x)
                if x == 1:
                    fhand_nlist.append(14)
        fhand_nlist.sort()
        value = 50000+100*fhand_nlist[-1]+fhand_nlist[-2]
        new = fhand_nlist[:]
        for i in range(1,len(new)):
            if new[i] == new[(i-1)]:
                fhand_nlist.remove(new[i])
        n = 0
        straightmax = 0
        for i in range(1,len(fhand_nlist)):
            cn = fhand_nlist[(i-1)]
            if (cn+1) == fhand_nlist[i]:
                n+= 1
                cn +=1
                if cn > straightmax:
                    straightmax = cn
            else:
                if n < 4:
                    n=0
        if n >=4:
            value = 80000+100*straightmax+(straightmax-1)
    if value < 80000 and (np.amax(nnumbers) == 4):
        fnumber = np.argmax(nnumbers)
        #WPNRONGOIASFOIJOWENGOIJASDPJ
        if fnumber == 1:
            fnumber = 14
        value = 70000 + fnumber * 100
        max = numbers[-1]
        if max != fnumber:
            value += max
        else:
            if max == 14:
                value += numbers[-2]
            else:
                value += numbers[(len(numbers)-5)]
    if value < 70000 and (np.amax(nnumbers) == 3) and np.partition(nnumbers.flatten(), -2)[-2] >= 2:
        x = np.argmax(nnumbers)
        if x == 1:
            value = 61400
            nnumbers[np.argmax(nnumbers)] = 0
            value += np.argmax(nnumbers)
        else:
            value = 60000 + 100*x
            nnumbers[x] = 0
            x2 = np.argmax(nnumbers)
            if x2 == 1:
                value += 14
            else:
                value += x2
    if value <50000:
        newnumbers = numbers[:]
        for i in range(1,len(numbers)):
            if numbers[i] == numbers[(i-1)]:
                newnumbers.remove(numbers[i])
        n = 0
        if len(newnumbers) >=5:
            for i in range(1,len(newnumbers)):
                cn = newnumbers[(i-1)]
                if (cn+1) == newnumbers[i]:
                    n+= 1
                    cn +=1
                else:
                    if n < 4:
                        n=0
        if n >=4:
            value = 40000 + cn*100+cn-1
        else:
            if (np.amax(nnumbers) == 3):
                n = np.argmax(nnumbers)
                if n == 1:
                    value = 31400+numbers[-2]
                else:
                    value = 30000+100*n
                    if numbers[-1] != n:
                        value += numbers[-1]
                    else:
                        value+=numbers[-4]
            elif  (np.amax(nnumbers) == 2) and np.partition(nnumbers.flatten(), -2)[-2] == 2:
                x1=np.argmax(nnumbers)
                nnumbers[x1] = 0
                x2 = np.argmax(nnumbers)
                if x1 == 1:
                    value = 21400+x2
                else:
                    value = 20000+100*x2+x1
            elif  (np.amax(nnumbers) == 2):
                rnu = np.argmax(nnumbers)
                numbers.remove(rnu)
                numbers.remove(rnu)
                if rnu == 1:
                    value = 11400+numbers[-2]
                else:
                    value = 10000+100*rnu+numbers[-1]
            else:
                value  = 100*int(numbers[-1]) + int(numbers[-2])
    return int(value)



def memoize_probs(func):
    with open('probs_data.json') as json_file:
        cache = json.load(json_file)
    def memoized_func(hand,table1,n):
        all = [hand,table1,n]
        key = str(all)
        if key in cache:
            return cache[key]
        result = func(hand,table1,n)
        cache[str(all)] = result
        with open('probs_data.json', 'w') as fp:
            json.dump(cache, fp)
        return result
    return memoized_func

#as getprobs is called a larger number of times, it will become faster as more input combinations
#and their probabilities will be saved to the json file

#to calculate probability of winning and tying, getprobs simulates 10,000 hands and checks
#the percentage where the player with "hand" wins and ties.
#table1 is a list with a number of cards 0, 3, 4, or 5. n is the number of opponents.
@memoize_probs
def getprobs(hand,table1,n):
    nwin = 0
    ntie = 0
    ntrials = 0
    if table1 == []:
        for j in range(0,10000):
            tablespecial = table1[:]
            currentdeck = deck[:]
            currentdeck.remove(hand[0])
            currentdeck.remove(hand[1])
            np.random.shuffle(currentdeck)
            tablespecial.append(currentdeck[0])
            currentdeck.remove(currentdeck[0])
            tablespecial.append(currentdeck[1])
            currentdeck.remove(currentdeck[1])
            tablespecial.append(currentdeck[0])
            currentdeck.remove(currentdeck[0])
            tablespecial.append(currentdeck[1])
            currentdeck.remove(currentdeck[1])
            tablespecial.append(currentdeck[1])
            currentdeck.remove(currentdeck[1])
            opponents = []
            for q in range(0,(2*n)):
                opponents.append(currentdeck[0])
                currentdeck.remove(currentdeck[0])
            types = np.zeros((n+1))
            for q in range(0,n):
                ohand = []
                ohand.append(opponents[(q*2)])
                ohand.append(opponents[(q*2+1)])
                types[(q+1)] = bvalue(ohand,tablespecial)
            types[0] = bvalue(hand,tablespecial)
            if np.amax(types) != np.partition(types.flatten(), -2)[-2]:
                #if there are no ties
                if np.argmax(types) == 0:
                    nwin = nwin + 1
            else:
                if np.amax(types) == types[0]:
                    y = np.argsort(types)
                    opn=y[-2]
                    hand2 = []
                    hand2.append(opponents[2*(opn-1)])
                    hand2.append(opponents[2*opn-1])
                    winner = 0
                    if winner == 1:
                        nwin = nwin + 1
                    elif winner == 0:
                        ntie = ntie + 1
            ntrials +=  1
            if j == 9999:
                probwin = float(nwin)/float(ntrials)
                probtie = float(ntie)/float(ntrials)
    elif len(table1) == 3:
        for j in range(0,10000):
            tablespecial = table1[:]
            currentdeck = deck[:]
            currentdeck.remove(hand[0])
            currentdeck.remove(hand[1])
            np.random.shuffle(currentdeck)
            tablespecial.append(currentdeck[0])
            currentdeck.remove(currentdeck[0])
            tablespecial.append(currentdeck[1])
            currentdeck.remove(currentdeck[1])
            opponents = []
            for q in range(0,(2*n)):
                opponents.append(currentdeck[0])
                currentdeck.remove(currentdeck[0])
            types = np.zeros((n+1))
            for q in range(0,n):
                ohand = []
                ohand.append(opponents[(q*2)])
                ohand.append(opponents[(q*2+1)])
                types[(q+1)] = bvalue(ohand,tablespecial)
            types[0] = bvalue(hand,tablespecial)
            if np.amax(types) != np.partition(types.flatten(), -2)[-2]:
                #if there are no ties
                if np.argmax(types) == 0:
                    nwin = nwin + 1
            else:
                if np.amax(types) == types[0]:
                    y = np.argsort(types)
                    opn=y[-2]
                    hand2 = []
                    hand2.append(opponents[2*(opn-1)])
                    hand2.append(opponents[2*opn-1])
                    winner = 0
                    if winner == 1:
                        nwin = nwin + 1
                    elif winner == 0:
                        ntie = ntie + 1
            ntrials +=  1
            if j == 9999:
                probwin = float(nwin)/float(ntrials)
                probtie = float(ntie)/float(ntrials)
    elif len(table1) == 4:
        for j in range(0,10000):
            tablespecial = table1[:]
            currentdeck = deck[:]
            currentdeck.remove(hand[0])
            currentdeck.remove(hand[1])
            currentdeck.remove(table1[0])
            currentdeck.remove(table1[1])
            currentdeck.remove(table1[2])
            currentdeck.remove(table1[3])
            np.random.shuffle(currentdeck)
            tablespecial.append(currentdeck[0])
            currentdeck.remove(currentdeck[0])
            opponents = []
            for q in range(0,(2*n)):
                opponents.append(currentdeck[0])
                currentdeck.remove(currentdeck[0])
            types = np.zeros((n+1))
            for q in range(0,n):
                ohand = []
                ohand.append(opponents[(q*2)])
                ohand.append(opponents[(q*2+1)])
                types[(q+1)] = bvalue(ohand,tablespecial)
            types[0] = bvalue(hand,tablespecial)
            if np.amax(types) != np.partition(types.flatten(), -2)[-2]:
                #if there are no ties
                if np.argmax(types) == 0:
                    nwin = nwin + 1
            else:
                if np.amax(types) == types[0]:
                    y = np.argsort(types)
                    opn=y[-2]
                    hand2 = []
                    hand2.append(opponents[2*(opn-1)])
                    hand2.append(opponents[2*opn-1])
                    winner = 0
                    if winner == 1:
                        nwin = nwin + 1
                    elif winner == 0:
                        ntie = ntie + 1
            ntrials = ntrials + 1
            if j == 9999:
                probwin = float(nwin)/float(ntrials)
                probtie = float(ntie)/float(ntrials)
    elif len(table1) == 5:
        for j in range(0,10000):
            tablespecial = table1[:]
            currentdeck = deck[:]
            currentdeck.remove(hand[0])
            currentdeck.remove(hand[1])
            currentdeck.remove(table1[0])
            currentdeck.remove(table1[1])
            currentdeck.remove(table1[2])
            currentdeck.remove(table1[3])
            currentdeck.remove(table1[4])
            np.random.shuffle(currentdeck)
            opponents = []
            for q in range(0,(2*n)):
                opponents.append(currentdeck[0])
                currentdeck.remove(currentdeck[0])
            types = np.zeros((n+1))
            for q in range(0,n):
                ohand = []
                ohand.append(opponents[(q*2)])
                ohand.append(opponents[(q*2+1)])
                types[(q+1)] = bvalue(ohand,tablespecial)
            types[0] = bvalue(hand,tablespecial)
            if np.amax(types) != np.partition(types.flatten(), -2)[-2]:
                #if there are no ties
                if np.argmax(types) == 0:
                    nwin = nwin + 1
            else:
                if np.amax(types) == types[0]:
                    y = np.argsort(types)
                    opn=y[-2]
                    hand2 = []
                    hand2.append(opponents[2*(opn-1)])
                    hand2.append(opponents[2*opn-1])
                    winner = 0
                    if winner == 1:
                        nwin = nwin + 1
                    elif winner == 0:
                        ntie = ntie + 1
            ntrials = ntrials + 1
            if j == 9999:
                probwin = float(nwin)/float(ntrials)
                probtie = float(ntie)/float(ntrials)
    return (probwin,probtie)

#val_dist gives the distribution of values for a hand given a table
def memoize_val_dist(func):
    with open('val_dist_data.json') as json_file:
        cache = json.load(json_file)
    def memoized_func(table1,n):
        inputs = [table1,n]
        key = str(inputs)
        if key in cache:
            return cache[key]
        result = func(table1,n)
        cache[str(inputs)] = result
        with open('val_dist_data.json', 'w') as fp:
            json.dump(cache, fp)
        return result
    return memoized_func

@memoize_val_dist
def val_dist(table1,n):
    scoredist = np.zeros(11)
    if table1==[]:
        for i in range(0,10000):
            deck2 = deck[:]
            hand = []
            np.random.shuffle(deck2)
            hand.append(deck2[0])
            deck2.remove(deck2[0])
            hand.append(deck2[2])
            deck2.remove(deck2[2])
            currentdeck = deck2[:]
            np.random.shuffle(currentdeck)
            table = []
            table.append(currentdeck[1])
            currentdeck.remove(currentdeck[1])
            table.append(currentdeck[1])
            currentdeck.remove(currentdeck[1])
            table.append(currentdeck[0])
            currentdeck.remove(currentdeck[0])
            table.append(currentdeck[1])
            currentdeck.remove(currentdeck[1])
            table.append(currentdeck[1])
            currentdeck.remove(currentdeck[1])
            value = bvalue(hand,table)
            #value is between 2 and more than 100000
            ind = int(float(value) / 10000)
            for j in range(0,(ind+1)):
                scoredist[ind]+=1
        scoredist / 10000
    elif len(table1) == 3:
        for i in range(0,10000):
            deck2 = deck[:]
            hand = []
            np.random.shuffle(deck2)
            hand.append(deck2[0])
            deck2.remove(deck2[0])
            hand.append(deck2[2])
            deck2.remove(deck2[2])
            currentdeck = deck2[:]
            np.random.shuffle(currentdeck)
            table = table1
            table.append(currentdeck[0])
            currentdeck.remove(currentdeck[0])
            table.append(currentdeck[1])
            currentdeck.remove(currentdeck[1])
            value = bvalue(hand,table)
            #value is between 2 and more than 100000
            ind = int(float(value) / 10000)
            for j in range(0,(ind+1)):
                scoredist[ind]+=1
        scoredist / 10000
    elif len(table1) == 4:
        for i in range(0,10000):
            hand = []
            deck2 = deck[:]
            np.random.shuffle(deck2)
            hand.append(deck2[0])
            deck2.remove(deck2[0])
            hand.append(deck2[2])
            deck2.remove(deck2[2])
            currentdeck = deck2[:]
            np.random.shuffle(currentdeck)
            table = table1
            table.append(currentdeck[0])
            currentdeck.remove(currentdeck[0])
            value = bvalue(hand,table)
            #value is between 2 and more than 100000
            ind = int(float(value) / 10000)
            for j in range(0,(ind+1)):
                scoredist[ind]+=1
        scoredist / 10000
    elif len(table1) == 5:
        for i in range(0,10000):
            hand = []
            deck2 = deck[:]
            np.random.shuffle(deck2)
            hand.append(deck2[0])
            deck2.remove(deck2[0])
            hand.append(deck2[2])
            deck2.remove(deck2[2])
            currentdeck = deck2[:]
            np.random.shuffle(currentdeck)
            table = table1
            value = bvalue(hand,table)
            #value is between 2 and more than 100000
            ind = int(float(value) / 10000)
            for j in range(0,(ind+1)):
                scoredist[ind]+=1
        scoredist / 10000
        #scoredist[ind] gives probability that value of hand have value > ind*10000
        #this scoredist is for a single opponent hand
    score_list = []
    for i in range(0,11):
        score_list.append(scoredist[i])
    return score_list
