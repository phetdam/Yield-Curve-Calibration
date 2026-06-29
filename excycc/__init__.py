import sys
sys.path.insert(0, "../")
from discountFactorParYield import calcDisFact
from discountFactorParYield import graph as graphDF
from contCompYields import calcYields
from contCompYields import graph as graphCC
from forwardCurve import forwardCurve
from forwardCurve import graph as graphFC

def main():
  periodDF = calcDisFact('../daily-treasury-par-yield-curve-rates.csv')
  print(periodDF)
  graphDF(periodDF)
  yieldsDF = calcYields('../daily-treasury-par-yield-curve-rates.csv')
  print(yieldsDF)
  graphCC(yieldsDF)
  forwardCurveDF = forwardCurve('../daily-treasury-par-yield-curve-rates.csv')
  print(forwardCurveDF)
  graphFC(forwardCurveDF)
  pass

if __name__ == "__main__":
  main()
