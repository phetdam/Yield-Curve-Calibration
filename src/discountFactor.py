import pandas as pd
import matplotlib.pyplot as plt

def calcDisFact(name: str):
  df = pd.read_csv(name);
  #print(df)
  #dates = df['Date']
  #print(dates)
  weeks = [4, 6, 8, 13, 17, 26, 52]
  periodDisFact = pd.DataFrame(index = df['Date'],  columns = weeks, dtype = float)
  #print(periodDisFact)
  for row in range(len(df)):
    for week in weeks:
      rateCol = f"{week} WEEKS BANK DISCOUNT"
      rate = df.loc[row, rateCol] / 100.0;
      t = week / 52.0
      periodDisFact.loc[df.loc[row, 'Date'], week] = (1 / (1 * (1 + rate) ** t))

  return periodDisFact

def graph(pd):
  weeks = pd.columns
  for date in pd.index:
    plt.plot(weeks, pd.loc[date], marker = 'o', label = date)

  plt.xlabel('Maturity (Weeks)')
  plt.ylabel('Discount Factor')
  plt.title('Treasury Bill Discount Factors')
  plt.legend()
  plt.grid(True)
  plt.show()

def main():
  periodDF = calcDisFact('../csvs/daily-treasury-bill-rates.csv')
  print(periodDF)
  graph(periodDF)

if __name__ == "__main__":
  main()
