import pandas as pd
import numpy as np

class Laboratory:

  def __init__(self, initial_data):
    self.laboratory_name = initial_data['laboratory_name']
    self.additional_evac = initial_data['additional_evac']
#    self.room = initial_data['room']
#    self.department = initial_data['department']
#    self.principle_investigator = initial_data['principle_investigator']
#    self.other_contact = initial_data['other_contact']
    self.height = initial_data['height']
    self.surface_area = initial_data['surface_area']
    self.ach_unoccupied_day = initial_data['ach_unoccupied_day']
    self.ach_occupied_day = initial_data['ach_occupied_day']
    self.ach_unoccupied_night = initial_data['ach_unoccupied_night']
    self.ach_occupied_night = initial_data['ach_occupied_night']
    self.additional_evac = initial_data['additional_evac']
    self.total_hoods = initial_data['total_hoods']
    min_evac_unoccupied_day = generate_min_evac_cfm(self.height, self.surface_area, self.ach_unoccupied_day, self.additional_evac)
    self.min_evac_unoccupied_day = min_evac_unoccupied_day
    min_evac_occupied_day = generate_min_evac_cfm(self.height, self.surface_area, self.ach_occupied_day, self.additional_evac)
    self.min_evac_occupied_day = min_evac_occupied_day
    min_evac_unoccupied_night = generate_min_evac_cfm(self.height, self.surface_area, self.ach_unoccupied_night, self.additional_evac)
    self.min_evac_unoccupied_night = min_evac_unoccupied_night
    min_evac_occupied_night = generate_min_evac_cfm(self.height, self.surface_area, self.ach_occupied_night, self.additional_evac)
    self.min_evac_occupied_night = min_evac_occupied_night
    self.day_start = pd.to_datetime(initial_data['day_start'])
    self.night_start = pd.to_datetime(initial_data['night_start'])
    self.occupancy_percent = initial_data['fumehood_occupancy_percent']
    self.fumehood_reduction_factor = 0
    self.fumehoods = []
    self.occupancy_data = None
    self.min_evac_series = None
    self.fumehoods_unadjusted_sum = None
    self.fumehoods_adjusted_sum = None
    self.summary = None
    self.fumehood_data = None

  def reset_parameters(self, new_ach_unoccupied_day, new_ach_occupied_day, new_ach_unoccupied_night, new_ach_occupied_night, new_occupancy_percent, new_fumehood_reduction_factor):
    self.occupancy_percent = new_occupancy_percent
    self.ach_unoccupied_day = new_ach_unoccupied_day
    self.ach_occupied_day = new_ach_occupied_day
    self.ach_unoccupied_night = new_ach_unoccupied_night
    self.ach_occupied_night = new_ach_occupied_night
    min_evac_unoccupied_day = generate_min_evac_cfm(self.height, self.surface_area, self.ach_unoccupied_day, self.additional_evac)
    self.min_evac_unoccupied_day = min_evac_unoccupied_day
    min_evac_occupied_day = generate_min_evac_cfm(self.height, self.surface_area, self.ach_occupied_day, self.additional_evac)
    self.min_evac_occupied_day = min_evac_occupied_day
    min_evac_unoccupied_night = generate_min_evac_cfm(self.height, self.surface_area, self.ach_unoccupied_night, self.additional_evac)
    self.min_evac_unoccupied_night = min_evac_unoccupied_night
    min_evac_occupied_night = generate_min_evac_cfm(self.height, self.surface_area, self.ach_occupied_night, self.additional_evac)
    self.fumehood_reduction_factor = new_fumehood_reduction_factor

  def reset(self):
    self.occupancy_data = None
    self.min_evac_series = None
    self.fumehoods_unadjusted_sum = None
    self.fumehoods_adjusted_sum = None
    self.summary = None  
    for fumehood in self.fumehoods:
      fumehood.reset()

  def __str__(self):
    print self.laboratory_name
    return self.laboratory_name + '==' + str(','.join(map(str, [self.ach_unoccupied_day, self.ach_occupied_day, self.ach_unoccupied_night, self.ach_occupied_night, self.occupancy_percent, self.fumehood_reduction_factor])))

def generate_min_evac_cfm(height, surface_area, ach, additional_evac):
  result = (height * surface_area * ach)/60 - additional_evac
  return result

def get_min_evac_cfm_for_time(time, occupied, laboratory):
  if time.hour >= laboratory.day_start.hour and time.hour <= laboratory.night_start.hour:
    if occupied:
      return laboratory.min_evac_occupied_day
    else:
      return laboratory.min_evac_unoccupied_day
  else:
    if occupied:
      return laboratory.min_evac_occupied_night
    else:
      return laboratory.min_evac_unoccupied_night
  return None


def get_laboratory_for_id(id, laboratories):
  for laboratory in laboratories:
    if laboratory.laboratory_name == id:
      return laboratory
  return None

def get_all_fumehood_data_for_lab(laboratory):
  laboratory.fumehood_data = pd.concat([fumehood.data for fumehood in laboratory.fumehoods], join='outer', axis = 1)
  return laboratory.fumehood_data

def generate_laboratory_summary(laboratory):
  df = pd.concat([laboratory.min_evac_series, laboratory.fumehoods_unadjusted_sum, laboratory.fumehoods_adjusted_sum], join='outer', axis = 1)
  df.columns = ["minimum_evac", "hood_unadjusted_sum", "hood_adjusted_sum"]
  laboratory.summary = df
  return df