import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
from discountFactorParYield import calcDisFact

def calcYields(name: str):
  finalDisFacts = calcDisFact(name)
  contCompYields = pd.DataFrame(index = finalDisFacts.index, columns = finalDisFacts.columns, dtype = float)

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
  yieldsDF = calcYields('../csvs/daily-treasury-par-yield-curve-rates.csv')
  print(yieldsDF)
  graph(yieldsDF)

if __name__ == "__main__":
  main()
