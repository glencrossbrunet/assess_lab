import numpy as np
import pandas as pd
import random
from simulatorlab.laboratory import *

class HoodModel:

  def __init__(self, initial_data):
    self.model = initial_data['model']
    self.max_sash_height = initial_data['max_sash_height']
    self.sash_width = initial_data['sash_width']
    self.face_vel_occupied = initial_data['face_vel_occupied']
    self.face_vel_unoccupied = initial_data['face_vel_unoccupied']
    self.min_cfm = initial_data['min_cfm']
    self.max_cfm = initial_data['max_cfm']

  def __str__(self):
    return self.model

class Fumehood:

  def __init__(self, initial_data, laboratories, hoodmodels):
    self.hood_id = initial_data['hood_id']
    self.bac = initial_data['bac']
    self.mcgill_tag = initial_data['mcgill_tag']
    self.hood_num = initial_data['hood_num']
    self.workshop = initial_data['workshop']
    self.laboratory = get_laboratory_for_id(initial_data['laboratory'], laboratories)
    if(self.laboratory is not None):
      self.laboratory.fumehoods.append(self)
    self.hood_model = get_hoodmodel_for_id(initial_data['hood_model'], hoodmodels)
    self.install_time = initial_data['install_time']
    self.follow_up_date = initial_data['follow_up_date']
    self.mac_address = initial_data['mac_address']
    self.gateway_id = initial_data['gateway_id']
    self.user_type = initial_data['user_type']
    self.flag_data = initial_data['flag_data']
    self.description_notes = initial_data['description_notes']
    self.installation_notes = initial_data['installation_notes']
    self.prompt_type = initial_data['prompt_type']
    self.data = None
    self.unadjusted_data = None
    self.occupancy_data = None

  def __str__(self):
    if self.hood_model.model is None or self.laboratory is None:
      return self.hood_id + "__incomplete-metadata"
    return self.hood_id + '__' + self.hood_model.model + '__' + self.laboratory.laboratory_name

  def reset(self):
    if(self.unadjusted_data is not None):
      self.data = self.unadjusted_data.copy()

  def facevelocity(self, occupied):
    if occupied:
      return self.hood_model.face_vel_occupied
    else:
      return self.hood_model.face_vel_unoccupied

  def faceintakecfm(self, sash_height, occupied):
    return self.facevelocity(occupied) * sash_height * self.hood_model.sash_width / 144

  def finalcfm(self, sash_height, occupied):
    sash_height = sash_height * self.hood_model.max_sash_height * 0.01
    return np.min([self.hood_model.max_cfm, 
                   np.max([self.hood_model.min_cfm, self.faceintakecfm(sash_height, occupied)])])

def get_fumehood_for_bac(bac, fumehoods):
  for fumehood in fumehoods:
    if fumehood.bac == bac:
      return fumehood
  return None

def get_hoodmodel_for_id(id, hoodmodels):
  for hoodmodel in hoodmodels:
    if hoodmodel.model == id:
      return hoodmodel
  return None

def add_unadjusted_fumehood_data_to_fumehoods(df, fumehoods):
  df = df.groupby('fumehood')
  for k, v in df:
    v = v.drop('fumehood', 1)
    v = v.drop('flow', 1)
    v.columns = [k]
    k.unadjusted_data = v

def test_flow_vs_open(fumehood):
  pass

def link_missing_sample_data_for_random_fumehoods(fumehoods):
  for fumehood in fumehoods:
    if fumehood.unadjusted_data is None:
      for fumehood_prime in fumehoods:
        if fumehood_prime.unadjusted_data is not None and fumehood_prime.bac == fumehood.bac:
          fumehood.unadjusted_data = fumehood_prime.unadjusted_data

def populate_fumehood_occupancy_data(fumehood):
  index = fumehood.data.index
  result = []
  for each in index:
    if each.hour >= fumehood.laboratory.day_start.hour and each.hour <= fumehood.laboratory.night_start.hour and np.random.rand(1)[0] < fumehood.laboratory.occupancy_percent:
      result.append(True)
    else:
      result.append(False)
  fumehood.occupancy_data = pd.Series(result, index=index)

def adjust_cfm_by_occupancy(fumehood):
  for sample in fumehood.data.index:
    percent_open = fumehood.data.loc[sample]
    occ = fumehood.occupancy_data.loc[sample]
    fumehood.data.loc[sample] = fumehood.finalcfm(percent_open, occ)

def get_random_working_bac(fumehoods, bac):
  if bac == -1:
    return get_random_working_bac(fumehoods, fumehoods[random.randint(0,len(fumehoods) -1)].bac)
  else:
    return bac