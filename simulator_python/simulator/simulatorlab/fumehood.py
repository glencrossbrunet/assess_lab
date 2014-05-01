import numpy as np
import pandas as pd

class HoodModel:

  def __init__(self, initial_data):
    self.model = initial_data['model']
    self.max_sash_height = initial_data['max_sash_height']
    self.sash_width = initial_data['sash_width']
    self.face_vel_occupied = initial_data['face_vel_occupied']
    self.face_vel_unoccupied = initial_data['face_vel_unoccupied']
    self.min_cfm = initial_data['min_cfm']
    self.max_cfm = initial_data['max_cfm']
    self.prompt_type = initial_data['prompt_type']


class Fumehood:

  def __init__(self, initial_data, laboratory, hoodmodel):
    self.hood_id = initial_data['hood_id']
    self.bac = initial_data['bac']
    self.mcgill_tag = initial_data['mcgill_tag']
    self.additional_evac = initial_data['additional_evac']
    self.hood_num = initial_data['hood_num']
    self.workshop = initial_data['workshop']
    self.laboratory = initial_data['laboratory']
    self.hood_model = initial_data['hood_model']
    self.install_time = initial_data['install_time']
    self.follow_up_date = initial_data['follow_up_date']
    self.mac_address = initial_data['mac_address']
    self.gateway_id = initial_data['gateway_id']
    self.user_type = initial_data['user_type']
    self.flag_data = initial_data['flag_data']
    self.description_notes = initial_data['description_notes']
    self.installation_notes = initial_data['installation_notes']
    self.sash_height = 0
    self.occupied = True

  def facevelocity(self):
    if self.occupied:
      return self.hood_model.face_vel_occupied
    else:
      return self.hood_model.face_vel_unoccupied

  def faceintakecfm(self):
    return self.facevelocity * self.sash_height * self.hood_model.sash_width / 144

  def fumehoodcfm(self):
    return np.min([self.hood_model.max_cfm, 
                   np.max([self.hood_model.min_cfm, self.faceintakecfm])])
