import matplotlib.pyplot as plt
import pandas_datareader as pdr
import pandas as pd
import datetime as dt

#definition
#paradox: days where vix and spy move the same direction

#goal:
#      find all occurneces of up/down days following a paradox,looking for high probabilities

#first get pct_change of vix and spy to determine direction ez
start = dt.datetime(1990,1,2)
end = dt.datetime(2022,9,15)
df = pdr.DataReader('SPY','yahoo',start,end)
df['pct'] =  df.Close.pct_change()
print(df)
df.drop(df.tail(1).index,inplace=True)
print(df)
df2 = pd.read_csv('VIX_History.csv')
print(df2)
df2 = df2.CLOSE.pct_change()
df2.drop(df2.head(1).index,inplace=True)
print(df2)
df3 = df2.tolist()
df.reset_index(inplace=True)
df['pct2'] = df3
print(df)

#checks for paradoxes in both directions
def getP(col1,col2):
    if (col2 > 0) & (col1 > 0):

        return 1
    elif (col2 < 0) & (col1 <0):
        return 2
    else:
        return 0

#applying paradox checker on df
df['anon'] = df.apply(lambda x: getP(x.pct,x.pct2),axis=1)
#shifting close by 1 day to find frequency of down/up days following a paradox
df['close2'] =  df.pct.shift(-1)
#determine frequency of up and down days following both paradoxes
def getG(col1,col2):
        if (col1==1) & (col2 < 0):
            return 1
        elif (col1==2) & (col2 > 0):
            return 2
        else:
            return 0
#applying frequency function
df['parod'] = df.apply(lambda x: getG(x.anon,x.close2),axis=1)
#pulling dates of where upwards paradox is followed with red days for plot
#change to ==2 for finding downward paradoxes
indexes =[]
for index,val in df.iterrows():
    if val['parod']==1:
        indexes.append(index)

print(indexes)
#count upwards paradoxes
vixUp =  df.anon.value_counts()[1]
#count downwards paradoxes
vixDown = df.anon.value_counts()[2]
#count upwards paradoxes followed by red days
downParod = df.parod.value_counts()[1]
#count downwards paradoxes followed by green days
upParod = df.parod.value_counts()[2]
#occurnece of down days to up paradox
downF = downParod / vixUp
#occurence of up days to down paradox
upF = upParod / vixDown

print(df)
print(" chance of red day after up paradox:", downF )
print(" chance  of green day after down paradox:", upF)
print("how often is there a down paradox",vixDown/len(df))

#plot vlines for  all up paradoxes
plt.plot(df.Close)
for loc in indexes:
    plt.axvline(x=loc)


plt.show()
