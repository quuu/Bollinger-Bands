import bollinger as CALC
import plotly
import numpy
import json
import plotly.graph_objs as go
import requests

def getData(index="AAPL", frequency="1y"):
    ########BACKUP API TO PULL FROM
    #response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=152D6POCDHV6FCOL&datatype=json')
########
    highList=[];lowList=[];closeList=[];dateList=[]
    response = requests.get('https://api.iextrading.com/1.0/stock/' + index +  '/chart/'+frequency )
    #data=response.json()
    data=json.loads(response.text)
    #print(data)
    for i in data:
        if(i['high']>0 and i['low']>0) and i['close']>0:
            highList.append(i['high'])
            lowList.append(i['low'])
            closeList.append(i['close'])
            dateList.append(i['date'])
    return highList,lowList,closeList,dateList

def plotData(closeList, mean, lowerBand, higherBand, dateList, highList=[], lowList=[]):

    traceClose=go.Scatter(
            x=dateList,
            y=closeList,
            line=dict(color='rgba(255,0,0,1)'),
            name="Close",
            showlegend=True
    )
    traceMean=go.Scatter(
            x=dateList,
            y=mean,
            line=dict(color='rgba(0,0,0,0.6'),
            name="Mean",
            showlegend=True
    )
    traceLowBand=go.Scatter(
            x=dateList,
            y=lowerBand,
            line=dict(color='rgba(0,0,0,0.4)'),
            name="Lower Band",
            showlegend=True
    )
    traceHighBand=go.Scatter(
            x=dateList,
            y=higherBand,
            line=dict(color='rgba(0,0,0,0.4)'),
            name="Higher Band",
            showlegend=True
    )

    layout=go.Layout(

        title="THSI IS A CHART",
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            autotick=True,
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=True,
            showline=True,
            showticklabels=True,
        ),

        showlegend=True,
    )
    if(len(highList)!=0 and len(lowList)!=0):
        traceHigh=go.Scatter(
                x=dateList,
                y=highList,
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(color='rgba(255,0,0,0.2)'),
                name="High",
                showlegend=True
        )

        traceLow=go.Scatter(
               x=dateList,
               y=lowList,
               fillcolor='rgba(0,255,0,0.2)',
               line=dict(color='rgba(0,0,255,0.2)'),
               name="Low",
               showlegend=True
        )
        data=[traceHigh, traceLow,traceMean,traceClose,traceLowBand, traceHighBand]
    else:
        data=[traceMean,traceClose,traceLowBand,traceHighBand]
    fig = go.Figure(data=data,layout=layout)
    plotly.offline.plot(fig,filename="graph.html", auto_open=True)


if __name__=="__main__":

    index = str(input("What index would you like to look up? (Default is AAPL)\n"))

    #setting default value
    if(index==""):  index="AAPL"

    frequency = str(input("How frequent would you like te updates to be?\n1d, 1m, 3m, 6m, ytd, 1y, 2y, 5y (Default is 1y)\n"))

    #setting default value
    if(frequency==""):  frequency="1y"

    #getting all the api parameters
    highList,lowList,closeList,dateList=getData(index, frequency)

    #choosing which calculation to perform
    algo = str(input("SMA or EMA? (Default is Simple)\n"))

    #gets the EMA/SMA based off of just the closing values
    #add feature later to base it off of the average of the high and low lists
    if(algo == "EMA"):  mean = CALC.exponentialMovingAverage(closeList)
    else:   mean = CALC.simpleMovingAverage(closeList)

    #get the moving standard deviations
    deviation=CALC.standardDeviation(mean,closeList)

    #ADD PROMPT ABOUT WHETHER TO DISPLAY HIGH AND LOW OR NOT
    #highLow = str(input("Do you want to display the highest and lowest of the days?(Default: No)"))

    #plot the data
    plotData(closeList,mean,CALC.lowerBound(mean,deviation),
            CALC.higherBound(mean,deviation), dateList, highList, lowList)
