import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

def calcDisRate(name: str):
  # use "Date" column as index
  df = pd.read_csv(name, index_col="Date")
  print(f"par rates:\n{df}")
  periods = df.columns.to_numpy()
  # for info: print monthly and annual periods
  monthlyTimePeriods = []
  annualTimePeriods = []
  for period in periods:
    if "Mo" in period:
      monthlyTimePeriods.append(float(period.split()[0]))
    elif "Yr" in period:
      annualTimePeriods.append(float(period.split()[0]))
  
  print(f"months: {monthlyTimePeriods}\nyears: {annualTimePeriods}")
  disFactDF = pd.DataFrame(index=df.index, columns=df.columns, dtype=float)

  # find the index of the 6 month (we need this later)
  i6m = df.columns.get_loc("6 Mo")
  # iterate for each date and each column (maturity)
  for d, date in enumerate(df.index):
    for i, period in enumerate(periods):
      # short end construction
      if "Mo" in period:
        r = df.loc[date, period] / 100
        disFactDF.loc[date, period] = 1 / (1 + 0.5 * r)
      # long end construction
      elif "Yr" in period:
        # rate for this period
        r = df.loc[date, period] / 100
        # previous maturities' rates
        prev_rates = df.iloc[d, i6m:i].values / 100
        # sum of discounted previous maturities' rates w/ compounding factor
        rsum = (0.5 * prev_rates * disFactDF.iloc[d, i6m:i].values).sum()
        # compute discount factor by subtracting the previous discounted rates
        disFactDF.loc[date, period] = (1 - rsum) / (1 + 0.5 * r)
  #print(disFactDF)
  return disFactDF


def to_yf(s: str) -> float:
  """Converts "x Mo" and "y Yr" strings to year fractions."""
  # months/years + "Mo" or "Yr"
  time, period = s.split()
  return float(time) / 12 if period == "Mo" else float(time)

 
def graph(pd):
  # convert weeks/months columns to year fractions
  times = [to_yf(s) for s in pd.columns]
  for date in pd.index:
    plt.plot(times, pd.loc[date], marker='o', label=date)

  plt.xlabel('Maturity (Years)')
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
