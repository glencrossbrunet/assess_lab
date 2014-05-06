class Laboratory:

  def __init__(self, initial_data):
    self.laboratory_name = initial_data['laboratory_name']
    self.building_name = initial_data['building_name']
    self.additional_evac = initial_data['additional_evac']
    self.building_num = initial_data['building_num']
    self.room = initial_data['room']
    self.department = initial_data['department']
    self.principle_investigator = initial_data['principle_investigator']
    self.other_contact = initial_data['other_contact']
    self.height = initial_data['height']
    self.surface_area = initial_data['surface_area']
    self.ach_unoccupied_day = initial_data['ach_unoccupied_day']
    self.ach_occupied_day = initial_data['ach_occupied_day']
    self.ach_unoccupied_night = initial_data['ach_unoccupied_night']
    self.ach_occupied_night = initial_data['ach_occupied_night']
    self.additional_evac = initial_data['additional_evac']
    self.total_hoods = initial_data['total_hoods']
    self.min_evac_unoccupied_day = generate_min_evac_cfm(self.height, self.surface_area, 
                                  self.ach_unoccupied_day, self.additional_evac)
    self.min_evac_occupied_day = generate_min_evac_cfm(self.height, self.surface_area, 
                                  self.ach_occupied_day, self.additional_evac)
    self.min_evac_unoccupied_night = generate_min_evac_cfm(self.height, self.surface_area, 
                                  self.ach_unoccupied_day, self.additional_evac)
    self.min_evac_occupied_night = generate_min_evac_cfm(self.height, self.surface_area, 
                                              self.ach_occupied_day, self.additional_evac)
    self.day_start = initial_data['day_start']
    self.night_start = initial_data['night_start']

  def __str__(self):
    return self.laboratory_name

def generate_min_evac_cfm(height, surface_area, ach, additional_evac):
  result = (height * surface_area * ach)/60 + additional_evac
  return result


def get_laboratory_for_id(id, laboratories):
  for laboratory in laboratories:
    if laboratory.laboratory_name == id:
      return laboratory
  return None