import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
import math

def processDF(name: str):
  #df = pd.read_csv(name)
  #print(df)
  df = pd.read_csv(name, index_col = "Date")
  periods = df.columns.to_numpy()
  #periods = periods[1:]
  print(periods)
  monthlyTimePeriods = []
  annualTimePeriods = []
  for period in periods:
    if "Mo" in period:
      str = period.split()
      monthlyTimePeriods.append(float(str[0]))
    elif "Yr" in period:
      str = period.split()
      annualTimePeriods.append(float(str[0]))

  print(monthlyTimePeriods, "\n", annualTimePeriods)
  #disFactDF = pd.DataFrame(index = df['Date'],  columns = df.columns[1:], dtype = float)
  #print(disFactDF)
  return df, monthlyTimePeriods, annualTimePeriods

def calcDisFact(name: str):
  df, monthlyTimePeriods, annualTimePeriods = processDF(name)
  lastMat = int(df.columns[-1].split()[0])

  biannualDisFacts = pd.DataFrame(index = df.index, columns = [f"{0.5 * (i + 1)}y" for i in range(2 * lastMat)], dtype = float)

  biannualBills = pd.DataFrame(index = df.index, columns = [f"{float(m)}m" for m in monthlyTimePeriods], dtype = float)

  for date in df.index:
    for i, m in enumerate(monthlyTimePeriods):
      rate = df.loc[date, df.columns[i]] / 100
      biannualBills.loc[date, f"{float(m)}m"] = 1 / (1 + float(m) * rate / 12)

  biannualDisFacts["0.5y"] = biannualBills["6.0m"]

  i6m = df.columns.get_loc("6 Mo")

  interpolationDF = pd.DataFrame(index = biannualDisFacts.index, columns = biannualDisFacts.columns, dtype = float)
  for d, date in enumerate(interpolationDF.index):
    interpolationDF.loc[date, :] = np.interp([0.5 * (i + 1) for i in range(len(biannualDisFacts.columns))],
      [0.5] + annualTimePeriods, df.iloc[d, i6m:])

  for d, date in enumerate(biannualDisFacts.index):
    for i, col in enumerate(biannualDisFacts.columns):
      rate = interpolationDF.loc[date, col] / 100
      rsum = (0.5 * rate * biannualDisFacts.iloc[d, 0:i].values).sum()
      biannualDisFacts.loc[date, col] = (1 - rsum) / (1 + 0.5 * rate)

  finalDisFacts = pd.DataFrame(index = df.index, columns = df.columns, dtype = float)
  finalDisFacts.iloc[:, 0:(i6m + 1)] = biannualBills.values

  for d, date in enumerate(finalDisFacts.index):
    finalDisFacts.iloc[d, i6m + 1:] = [biannualDisFacts.loc[date, f"{a}y"] for a in annualTimePeriods]

  contCompYields = pd.DataFrame(index = df.index, columns = df.columns, dtype = float)

  #print(contCompYields)

  for d, date in enumerate(contCompYields.index):
    #print(d, date)
    for i, col in enumerate(contCompYields.columns):
      #print(i, col)
      if "Mo" in col:
        str = col.split()
        year = float(str[0]) / 12
      elif "Yr" in col:
        str = col.split()
        year = float(str[0])
      #print(finalDisFacts.loc[date, col])
      contCompYields.loc[date, col] = -(1 / year) * math.log(finalDisFacts.loc[date, col])

  #print(contCompYields)

  #return finalDisFacts
  return contCompYields

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
  plt.ylabel('Yield')
  plt.title('Treasury Continuously Compounded Yield Curve')
  plt.legend()
  plt.grid(True)
  plt.show()

def main():
  #periodDF = calcDisRate('daily-treasury-par-yield-curve-rates.csv')
  periodDF = calcDisFact('daily-treasury-par-yield-curve-rates.csv')
  print(periodDF)
  graph(periodDF)
  pass

if __name__ == "__main__":
  main()
