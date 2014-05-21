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
    for dictionary in initial_data:
      for key in dictionary:
        setattr(self, key, dictionary[key])
    for key in kwargs:
      setattr(self, key, kwargs[key])
    self.day_start = pd.to_datetime(self.day_start)
    self.night_start = pd.to_datetime(self.night_start)

    self.fumehood_reduction_factor = 0
    self.fumehoods = []

  def reset_and_calculate_mins(self, new_ach_unoccupied_day, new_ach_occupied_day, new_ach_unoccupied_night, new_ach_occupied_night, new_fumehood_reduction_factor):
   
    self.dataframe = pd.DataFrame()

    self.ach_unoccupied_day = new_ach_unoccupied_day
    self.ach_occupied_day = new_ach_occupied_day
    self.ach_unoccupied_night = new_ach_unoccupied_night
    self.ach_occupied_night = new_ach_occupied_night

    self.min_evac_unoccupied_day = calculate_min_laboratory_evac_cfm(self.height, self.surface_area, self.ach_unoccupied_day, self.additional_evac)
    self.min_evac_unoccupied_night = calculate_min_laboratory_evac_cfm(self.height, self.surface_area, self.ach_unoccupied_night, self.additional_evac)
    self.min_evac_occupied_day = calculate_min_laboratory_evac_cfm(self.height, self.surface_area, self.ach_occupied_day, self.additional_evac)
    self.min_evac_occupied_night = calculate_min_laboratory_evac_cfm(self.height, self.surface_area, self.ach_occupied_night, self.additional_evac)


    self.fumehood_reduction_factor = new_fumehood_reduction_factor


  def __str__(self):
    return self.laboratory_name + '==' + str(','.join(map(str, [self.ach_unoccupied_day, self.ach_occupied_day, self.ach_unoccupied_night, self.ach_occupied_night, self.fumehood_occupancy_percent, self.fumehood_reduction_factor])))


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
    self.mcgill_tag = initial_data['mcgill_tag']
    self.hood_num = initial_data['hood_num']
    self.workshop = initial_data['workshop']
    self.laboratory = get_laboratory_for_id(initial_data['laboratory'], laboratories)
    if(self.laboratory is not None):
      self.laboratory.fumehoods.append(self)
    self.model = get_hoodmodel_for_id(initial_data['hood_model'], hoodmodels)
    self.install_time = initial_data['install_time']
    self.follow_up_date = initial_data['follow_up_date']
    self.mac_address = initial_data['mac_address']
    self.gateway_id = initial_data['gateway_id']
    self.user_type = initial_data['user_type']
    self.flag_data = initial_data['flag_data']
    self.description_notes = initial_data['description_notes']
    self.installation_notes = initial_data['installation_notes']
    self.prompt_type = initial_data['prompt_type']

    self.dataframe = pd.DataFrame()


  def __str__(self):
    if self.model.model is None or self.laboratory is None:
      return self.hood_id + "__incomplete-metadata"
    return self.hood_id + '__' + self.model.model + '__' + self.laboratory.laboratory_name

