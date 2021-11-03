import pandas as pd
import matplotlib.pyplot as pl

n = 100 #number of models generated
T = 191 #time intervals
total = 1 #total function interval
cf = []
cc = []

dg = pd.DataFrame() #all generated models dataframe
df = pd.read_excel('sheet.xlsx') #template sheet
dr = pd.read_excel('result.xlsx') #template sheet (results)
    
for k in range(n):
    
    dt = total/(T+1) #time interval 
    t = dt #current time
    for i in range(T):
        b = 168 *(t**5)*((1-t)**2)
        t += dt
        df.loc[i,'Beta(t)'] = b
 
    from scipy.stats import norm
    x = 0
    dev = 0.25
    w0 = 0
    for i in range(T+1):
        w = (x+norm.rvs(scale=dev**2))
        w0 += w
        df.loc[i,'W(t)'] = w0
    
    for i in range(T+1):
        if df.iloc[i,0] + df.iloc[i,1] > 0:
            df.loc[i,'D(t)'] = df.iloc[i,0] + df.iloc[i,1]
        else:
            df.loc[i,'D(t)'] = 0
        
    for i in range(T):
        dg.loc[i,k] = df.iloc[i,2]
        
ds = pd.read_csv('kandersteg2016.txt',sep = ';') #import of current season as CSV

N = int(0.5*T)

for i in range(N):
    cc.append(ds.iloc[i,2])

from scipy.stats import pearsonr #itterating the correlations
for i in range(n):
    for j in range(N):
        cf.append(dg.iloc[j,i])
    z = pearsonr(cc,cf)
    dr.loc[i,'Correlation'] = z[0]
    dr.loc[i,'Model Number'] = i
    cf.clear()
dr.sort_values(by=['Correlation'],inplace=True, ascending=False)

def percentage(x,y):
    return ((100*x)/y)-100

ooo = dr.iloc[0,0]
oooo = dr.iloc[1,0]
zero = (dg.iloc[N,ooo]+dg.iloc[N,oooo])/2
zeror = ds.iloc[N,2]

pred = []
for i in range(50):
    temp = ((dg.iloc[N+i,ooo]+dg.iloc[N+i,oooo])/2)
    pred.append(percentage(temp,zero))

real = []
for i in range(50):
    real.append(percentage(ds.iloc[N+i,2],zeror))

pl.plot(pred,label='Predicted')
pl.plot(real,label="Real")

pl.xlabel("Days")
pl.ylabel("Percentage Increase")
pl.legend()

