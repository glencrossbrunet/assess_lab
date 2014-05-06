import pandas as pd
import numpy as np

def generate_semi_random_occupancy_dataframe(start_date, end_date, freq, day_start, night_start, occupancy_percent):
  index = pd.date_range(start_date, end_date, freq=freq)
  result = []
  for each in index:
    if each.hour >= day_start and each.hour <= night_start and np.random.rand(1)[0] > occupancy_percent:
      result.append(True)
    else:
      result.append(False)
  return pd.Series(result, index=index)