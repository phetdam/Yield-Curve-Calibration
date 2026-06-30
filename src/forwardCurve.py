import math
from pathlib import Path
import sys
from typing import Iterable

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import CubicSpline

# directory file is in
_cur_dir = Path(__file__).absolute().parent

# local import
sys.path.insert(0, str(_cur_dir))
from discountFactorParYield import calcDisFact


def par_yield_maturities(names: Iterable[str]) -> list[float]:
  """Convert Treasury par yield column names into year fractions.

  Months are converted into actual years by dividing by 12.
  """
  years = []
  # pre-emptively split "1 Mo" into number and unit
  for num, unit in (name.split() for name in names):
    if unit == "Mo":
      years.append(float(num) / 12)
    # assume years if not month
    else:
      years.append(float(num))
  return years


class InstForwardCurve:
  """Instantaneous forward rate curve for a given date.

  Parameters
  ----------
  tenors : Iterable[float]
    Year fractions for each input tenor
  discount_factors : Iterable[float]
    Discount factors for each tenor
  interpolator, default=scipy.interpolate.CubicSpline
    Interpolator type object. This must be one of the SciPy interpolators, e.g.
    Akima1DInterpolator, CubicSpline, or something with a similar API.
  """

  def __init__(
    self,
    tenors: Iterable[float],
    discount_factors: Iterable[float],
    interpolator=CubicSpline
  ):
    self._tenors = np.array(tenors, dtype=float)
    self._dfs = np.array(discount_factors)
    # interpolate -log() of discount factors + save the PPoly derivatives so we
    # can later invoke its __call__() method to get our instantaneous forwards
    self._interp = interpolator
    self._fwds = self._interp(self._tenors, -np.log(self._dfs)).derivative()
  
  def tenors(self) -> np.array:
    """Return the input tenors in units of fractional years."""
    return self._tenors

  def discount_factors(self) -> np.array:
    """Return the input discount factors for each tenor."""
    return self._dfs

  def interpolator(self):
    """Return the interpolator type object."""
    return self._interp

  def __call__(self, ts: Iterable[float]) -> np.array:
    """Return instantaneous forward rates for the requested tenors.

    The requested tenors must be within the range of the input tenors.
    """
    return self._fwds(ts)


def graph_forward_rates(df: pd.DataFrame, n_points: int = 500):
  """Display a graph of the instantaneous forwards from discount factors.

  Parameters
  ----------
  df : pandas.DataFrame
    DataFrame of Treasury discount factors for each listed maturity
  n_points : int, default=500
    Number of maturities evenly spaced within the Treasury tenors to report a
    forward rate for. Use a large number to accurately represent the shape of
    the curve on the graph as otherwise the default matplotlib interpolation
    will make all the forward rate points appear linearly interpolated.
  """
  tenors = par_yield_maturities(df.columns)
  # build instantaneous forward curve for each day + plot
  for date in df.index:
    curve = InstForwardCurve(tenors, df.loc[date, :].values)
    # plot the given number of points for an accurate shape on the graph
    dense_tenors = np.linspace(tenors[0], tenors[-1], num=n_points)
    fwds = curve(dense_tenors)
    plt.plot(dense_tenors, fwds, label=f"{date} ({curve.interpolator().__name__})")

  plt.xlabel('Maturity (Years)')
  plt.ylabel('Forward Rate')
  plt.title('Instantaneous Treasury Forward Rates')
  plt.legend()
  plt.grid(True)
  plt.show()


def main() -> int:
  dfs = calcDisFact(
    _cur_dir / ".." / "csvs" / "daily-treasury-par-yield-curve-rates.csv"
  )
  graph_forward_rates(dfs)
  return 0


if __name__ == "__main__":
  sys.exit(main())
