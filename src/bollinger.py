from collections import deque

def exponentialMovingAverage(closeList):

    #uses EMA
    #EMA(n)=(CLOSE - EMA(n-1)) * MULTIPLIER - EMA(n-1)
    current=0

    #amount of terms used to calculate moving average
    terms=9
    count=0
    multiplier=(2/(terms+1+1))
    toReturn=[]
    for i in closeList:
        #happens for the first 10 terms, to get the initial SMA
        if(count<terms):
            current+=i
            count+=1
            toReturn.append(float('nan'))
        #sum it up and divide it
        elif(count==terms):
            current+=i
            current/=10
            toReturn.append(current)
            count+=1
        #for every term after 10
        #EMA calculation starting now
        else:
            current=multiplier*(i-current)+current
            toReturn.append(current)

    return toReturn

def simpleMovingAverage(closeList):
    current=0
    terms=10
    count=0
    toRemove=deque([])
    toReturn=[]
    for i in closeList:
        if(count<terms):
            current+=i
            count+=1
            toReturn.append(float('nan'))
            toRemove.append(i)
        else:
            toReturn.append(current/10)
            current=current-toRemove.popleft()+i
            toRemove.append(i)

    return toReturn



def standardDeviation(mean, closeList):
    variance=0
    terms=10
    count=0
    toRemove=deque([])
    toReturn=[]

    for i,j in zip(mean, closeList):
        if(count<terms):
            toReturn.append(float('nan'))
            variance+=(j)**2
            toRemove.append((j)**2)
            count+=1
        else:
            toReturn.append((variance/count)**(0.5))
            variance=variance-toRemove.popleft()+((i-j)**2)
            toRemove.append((i-j)**2)

    for i in toReturn:
        print(i)
    return toReturn

def lowerBound(mean):
    toReturn=[]
    for i in mean:
        #weird, but effective way to check for nan
        if(i!=i):
            toReturn.append(float('nan'))
        else:
            toReturn.append(i)

def higherBound():
    a=1
