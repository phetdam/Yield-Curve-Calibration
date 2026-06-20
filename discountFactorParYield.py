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

  i6m = df.columns.get_loc("6 Mo")

  for row in range(len(df)):
    date = df.loc[row, 'Date']
    for i, period in enumerate(periods):
      if "Mo" in period:
        rate = df.loc[row, period] / 100.0
        disFactDF.loc[df.loc[row, 'Date'], period] = 1 / (1 + 0.5 * rate)
      elif "Yr" in period:
        rate = df.loc[row, period] / 100.0
        prevRates = df.iloc[row, i6m:i].values / 100
        rsum = (0.5 * prevRates * disFactDF.iloc[row, i6m:i].values).sum()
        disFactDF.loc[df.loc[row, 'Date'], period] = (1 - rsum) / (1 + 0.5 * rate)

  #print(disFactDF)
  return disFactDF

def graph(pd):
  weeks = pd.columns
  weeksNumeric = []
  for week in weeks:
    if "Mo" in week:
      str = week.split()
      week = round(float(str[0]) / 12, 3)
      weeksNumeric.append(week)
    else:
      str = week.split()
      week = float(str[0])
      weeksNumeric.append(week)
  #print(weeks)
  #print(weeksNumeric)

  for date in pd.index:
    #plt.plot(weeks, pd.loc[date], marker = 'o', label = date)
    plt.plot(weeksNumeric, pd.loc[date], marker = 'o', label = date)

  #plt.xlabel('Maturity (Weeks and Years)')
  plt.xlabel('Maturity (Converted to Years for Uniformity)')
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
