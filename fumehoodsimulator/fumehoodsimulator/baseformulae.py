import pandas as pd
import numpy as np
import numpy as np
import copy

'''
LAB LEVEL
'''

def calculate_min_laboratory_evac_cfm(height, surface_area, ach, additional_evac):
  result = (height * surface_area * ach)/60 + abs(additional_evac)
  return result


def get_min_laboratory_evac_cfm_at_time(laboratory, time, occupied):
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


def copy_laboratory(laboratory):
  new_fumehoods = []
  for hood in laboratory.fumehoods:
    new_fumehoods.append(copy.deepcopy(hood))
  new_laboratory = copy.deepcopy(laboratory)
  new_laboratory.fumehoods = new_fumehoods
  return new_laboratory


'''
HOOD LEVEL
'''

def get_hood_face_velocity(hood, occupied):
  return hood.model.face_vel_occupied if occupied else hood.model.face_vel_unoccupied


def calculate_face_intake_cfm(hood, sash, occupied):
  return get_hood_face_velocity(hood, occupied) * sash * hood.model.sash_width / 144


def calculate_bounded_hood_cfm(hood, sash_percent, occupied, fumehood_multiplier):
  sash = sash_percent * hood.model.max_sash_height * 0.01
  return np.min([hood.model.max_cfm, np.max([hood.model.min_cfm, fumehood_multiplier * np.random.randint(95,105) * 0.01 * calculate_face_intake_cfm(hood, sash, occupied)])])

