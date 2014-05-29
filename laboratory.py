import pandas as pd
import numpy as np
from baseformulae import *
from laboratorylogic import *

"""
Key for Metrics:
    occupancy = a series of the occupancy of the lab, given as the sum of fumehoods occupied at the given time
    min_lab_evacuation = None 
    min_hood_evacuation = None
    min_hood_additional_evacuation = None
    real_fumehood_evacuation = None
    excess_fumehood_evacuation = None
    real_total_evacuation = None
"""

class Laboratory:

  def __init__(self, *initial_data, **kwargs):
    self.initial_data = initial_data
    for dictionary in initial_data:
      for key in dictionary:
        setattr(self, key, dictionary[key])
    for key in kwargs:
      setattr(self, key, kwargs[key])
    self.ach_day_start = pd.to_datetime(self.ach_day_start)
    self.ach_night_start = pd.to_datetime(self.ach_night_start)

    self.sash_height_multiplier = 1
    self.fumehoods = []


  def reset_and_calculate_mins(self, *new_data, **kwargs):
    for dictionary in self.initial_data:
      for key in dictionary:
        setattr(self, key, dictionary[key])

    self.dataframe = pd.DataFrame()
    for dictionary in new_data:
      for key in dictionary:
        setattr(self, key, dictionary[key])
    for key in kwargs:
      setattr(self, key, kwargs[key])

    self.ach_day_start = pd.to_datetime(self.ach_day_start)
    self.ach_night_start = pd.to_datetime(self.ach_night_start)
    self.min_evac_unoccupied_day = calculate_min_laboratory_evac_cfm(self.ceil_height, self.surface_area, self.day_unoccupied_ach, self.additional_evac)
    self.min_evac_unoccupied_night = calculate_min_laboratory_evac_cfm(self.ceil_height, self.surface_area, self.night_unoccupied_ach, self.additional_evac)
    self.min_evac_occupied_day = calculate_min_laboratory_evac_cfm(self.ceil_height, self.surface_area, self.day_occupied_ach, self.additional_evac)
    self.min_evac_occupied_night = calculate_min_laboratory_evac_cfm(self.ceil_height, self.surface_area, self.night_occupied_ach, self.additional_evac)

    print "Operating on lab with settings := " + str(self)

  def __str__(self):
    return self.laboratory_name + '==' + str(';'.join(map(lambda x : str(x).replace(".",","), [self.day_unoccupied_ach, self.day_occupied_ach, self.night_unoccupied_ach, self.night_occupied_ach, self.fumehood_occupancy_rate, self.sash_height_multiplier])))


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


'''
Key for Fumehood Dataframe:
  percent_open = percentage fumehood is open estimated by the datastream
  datastream_flow = flow estimated by the datastream 
  occupancy = true of false representing occupation
  evacuation_cfm = evacuation of the fumehood over time
'''

class Fumehood:

  def __init__(self, initial_data, laboratories, hoodmodels):
    self.hood_id = initial_data['hood_id']
    self.bac = initial_data['bac']
    self.laboratory = get_laboratory_for_id(initial_data['laboratory'], laboratories)
    if(self.laboratory is not None):
      self.laboratory.fumehoods.append(self)
    self.model = get_hoodmodel_for_id(initial_data['hood_model'], hoodmodels)

    self.dataframe = pd.DataFrame()


  def __str__(self):
    if self.model.model is None or self.laboratory is None:
      return self.hood_id + "__incomplete-metadata"
    return self.hood_id + '__' + self.model.model

