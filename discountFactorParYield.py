import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def par_rates_to_dfs(name: str):
  # use "Date" column as index
  df = pd.read_csv(name, index_col="Date")
  print(f"par rates:\n{df}")
  periods = df.columns.to_numpy()
  # monthly and annual periods
  months = []
  years = []
  for period in periods:
    if "Mo" in period:
      months.append(float(period.split()[0]))
    elif "Yr" in period:
      years.append(float(period.split()[0]))

  # find longest year
  last_mat = int(df.columns[-1].split()[0])
  # for bootstrapping, we need a discount factor every half year, as the par
  # rates are half-year compounding. so the number of discount factors for 6m
  # to the final year (30y) is 60, i.e. 0.5y, 1y, 1.5y, ... 30y, so 60
  dfs = pd.DataFrame(
    index=df.index,
    columns=[f"{0.5 * (i + 1)}y" for i in range(2 * last_mat)],
    dtype=float
  )
  # bills are up through 6m, so do them separately first
  tb_df = pd.DataFrame(
    index=df.index,
    columns=[f"{float(m)}m" for m in months],
    dtype=float
  )
  for date in df.index:
    for i, m in enumerate(months):
      # annualized rate for this maturity
      r = df.loc[date, df.columns[i]] / 100
      # de-annualize to shorter compounding period
      tb_df.loc[date, f"{float(m)}m"] = 1 / (1 + float(m) * r / 12)
  # ensure 6m discount factor in dfs is set
  dfs["0.5y"] = tb_df["6.0m"]
  # find the index of the 6 month (we need this later)
  i6m = df.columns.get_loc("6 Mo")
  # interpolated 6m through 30y points at half-year intervals
  rdf = pd.DataFrame(index=dfs.index, columns=dfs.columns, dtype=float)
  for d, date in enumerate(rdf.index):
    rdf.loc[date, :] = np.interp(
      [0.5 * (i + 1) for i in range(len(dfs.columns))],
      [0.5] + years,
      df.iloc[d, i6m:]
    )
  # now construct notes + bonds, 0.5y through 30y, every 0.5 years
  for d, date in enumerate(dfs.index):
    for i, col in enumerate(dfs.columns):
      # rate for this period (cash flow as notional is unit)
      r = rdf.loc[date, col] / 100
      # sum of discounted cash flows w/ compounding factor
      rsum = (0.5 * r * dfs.iloc[d, 0:i].values).sum()
      # compute discount factor
      dfs.loc[date, col] = (1 - rsum) / (1 + 0.5 * r)
  # populate final discount factors corresponding 1-to-1 with df
  tdf = pd.DataFrame(index=df.index, columns=df.columns, dtype=float)
  # set <1y maturities
  tdf.iloc[:, 0:(i6m + 1)] = tb_df.values
  # set >=1y maturities
  for d, date in enumerate(tdf.index):
    tdf.iloc[d, i6m + 1:] = [dfs.loc[date, f"{y}y"] for y in years]
  return tdf


def to_yf(s: str) -> float:
  """Converts "x Mo" and "y Yr" strings to year fractions."""
  # months/years + "Mo" or "Yr"
  time, period = s.split()
  return float(time) / 12 if period == "Mo" else float(time)

 
def graph(pd):
  # convert weeks/months columns to year fractions
  times = [to_yf(s) for s in pd.columns]
  # note: can use -np.log(pd.loc[date]) / times instead for continuously
  # compounded yields to verify the discount factors are proportional
  for date in pd.index:
    plt.plot(times, pd.loc[date], marker='o', label=date)

  plt.xlabel('Maturity (Years)')
  plt.ylabel('Discount Factor')
  plt.title('Treasury Par Yield Curve Discount Factors')
  plt.legend()
  plt.grid(True)
  plt.show()


def main() -> int:
  dfs = par_rates_to_dfs('daily-treasury-par-yield-curve-rates.csv')
  print(dfs)
  graph(dfs)
  return 0


if __name__ == "__main__":
  sys.exit(main())
