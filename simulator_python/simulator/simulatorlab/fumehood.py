import numpy as np
import pandas as pd

class Fumehood:
    bac
    kind
    height
    width
    minflowrate
    maxflowrate
    facevelocityoccupied
    facevelocityunoccupied
    maxsash
    maxcfm
    mincfm
    occupied
    metadata

    def __init__(self, kind, height, width, minflowrate, maxflowrate, facevelocityoccupied, facevelocityunoccupied, maxsash, maxcfm, mincfm):
      self.kind = kind
      self.height = height
      self.width = width
      self.minflowrate = minflowrate
      self.maxflowrate = maxflowrate
      self.facevelocityoccupied = facevelocityoccupied
      self.facevelocityunoccupied = facevelocityunoccupied
      self.maxsash = maxsash
      self.maxcfm = maxcfm
      self.mincfm = mincfm

    def facevelocity(self):
      if self.occupied:
        return self.facevelocityoccupied
      else:
        return self.facevelocityunoccupied

    def faceintakecfm(self):
      return self.facevelocity * self.maxsash * self.height * self.width / 144

    def fumehoodcfm(self):
      return np.min([self.maxcfm, np.max([self.mincfm, self.faceintakecfm])])

def load_fumehood_metadata(f):
  metadata = pd.read_csv(f)