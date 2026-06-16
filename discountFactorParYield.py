import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

def calcDisRate(name: str):
  df = pd.read_csv(name)
  #print(df)
  periods = df.columns.to_numpy()
  periods = periods[1:]
  print(periods)
  monthlyTimePeriods = []
  annualTimePeriods = []
  for period in periods:
    if "Mo" in period:
      str = period.split()
      monthlyTimePeriods.append(float(str[0]))
    elif "Yr" in period:
      str = period.split()
      annualTimePeriods.append(int(str[0]))
  
  print(monthlyTimePeriods, "\n", annualTimePeriods)
  disFactDF = pd.DataFrame(index = df['Date'],  columns = df.columns[1:], dtype = float)
  #print(disFactDF)

  for row in range(len(df)):
    date = df.loc[row, 'Date']
    for i, period in enumerate(periods):
      if "Mo" in period:
        str = period.split()
        time = float(str[0]) * 30.42
        rate = df.loc[row, period] / 100.0
        disFactDF.loc[df.loc[row, 'Date'], period] = 1 * ((rate * time) / 365)
      elif "Yr" in period:
        str = period.split()
        time = float(str[0]) * 30.42
        rate = df.loc[row, period] / 100.0
        sixMonthPeriod = periods[np.where(periods == "6 Mo")][0]
        #print(sixMonthPeriod)
        splitStr = sixMonthPeriod.split()
        sixMonthTime = float(splitStr[0]) * 30.42
        if str[0].__eq__("1"):
          disFactDF.loc[df.loc[row, 'Date'], period] = 1 * ((rate * time) / 365) + (1 * ((rate * sixMonthTime) / 365))
        else:
          previousSum = disFactDF.loc[date, periods[:i]].sum()
          disFactDF.loc[df.loc[row, 'Date'], period] = 1 * ((rate * time) / 365) + previousSum + (1 * ((rate * sixMonthTime) / 365)) 
  
  #print(disFactDF)
  return disFactDF 
 
def graph(pd):
  weeks = pd.columns
  for date in pd.index:
    plt.plot(weeks, pd.loc[date], marker = 'o', label = date)

  plt.xlabel('Maturity (Weeks and Years)')
  plt.ylabel('Discount Factor')
  plt.title('Treasury Par Yield Curve Discount Factors')
  plt.legend()
  plt.grid(True)
  plt.show()

def main():
  periodDF = calcDisRate('daily-treasury-par-yield-curve-rates.csv')  
  print(periodDF)
  graph(periodDF)
  pass

if __name__ == "__main__":
  main()
