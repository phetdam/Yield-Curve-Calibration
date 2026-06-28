import sys
sys.path.insert(0, "../")
from discountFactorParYield import *

def main():
  periodDF = calcDisFact('../daily-treasury-par-yield-curve-rates.csv')
  print(periodDF)
  graph(periodDF)
  pass

if __name__ == "__main__":
  main()
