import bollinger as CALC
import plotly
import numpy
import json
import plotly.graph_objs as go
import requests

def getData(highList, lowList, closeList, countList, index, frequency):
########BACKUP API TO PULL FROM
    #response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=152D6POCDHV6FCOL&datatype=json')
########

    response = requests.get('https://api.iextrading.com/1.0/stock/' + index +  '/chart/'+frequency )
    #data=response.json()
    data=json.loads(response.text)
    #print(data)
    count=0
    for i in data:
        if(i['high']>0 and i['low']>0) and i['close']>0:
            highList.append(i['high'])
            lowList.append(i['low'])
            closeList.append(i['close'])
            countList.append(count)
            count+=1

def plotData(highList, lowList, closeList, mean, countList):

    traceHigh=go.Scatter(
            x=countList,
            y=highList,
            fillcolor='rgba(255,0,0,0.2)',
            line=dict(color='rgba(255,0,0,0.2)'),
            name="High",
            showlegend=True
    )
    traceLow=go.Scatter(
            x=countList,
            y=lowList,
            fillcolor='rgba(0,255,0,0.2)',
            line=dict(color='rgba(0,0,255,0.2)'),
            name="Low",
            showlegend=True
    )
    traceMean=go.Scatter(
            x=countList,
            y=mean,
            name="Mean",
            showlegend=True
    )
    traceClose=go.Scatter(
            x=countList,
            y=closeList,
            name="Close",
            showlegend=True
    )

    data=[traceHigh, traceLow,traceMean,traceClose]
    plotly.offline.plot(data, auto_open=True)


if __name__=="__main__":
    highList=[]
    lowList=[]
    closeList=[]
    countList=[]
    index = str(input("What index would you like to look up?\n"))
    frequency = str(input("How frequent would you like te updates to be?\n1d, 1m, 3m, 6m, ytd, 1y, 2y, 5y\n"))
    getData(highList,lowList,closeList,countList, index, frequency)

    #gets the EMA based off of just the closing values
    #add feature later to base it off of the average of the high and low lists
    mean = CALC.exponentialMovingAverage(closeList)

    #gets SMA, depending on the trader, one or the other is preferred
    mean = CALC.simpleMovingAverage(closeList)

    #get the moving standard deviations
    standardDev=CALC.standardDeviation(mean,closeList)

    lowerBound=CALC.lowerBound(mean)



    #plot the data
    plotData(highList,lowList,closeList,mean, countList)
