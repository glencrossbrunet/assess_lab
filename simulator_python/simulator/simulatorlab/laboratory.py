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
    self.ach_unoccupied = initial_data['ach_unoccupied']
    self.ach_occupied = initial_data['ach_occupied']
    self.additional_evac = initial_data['additional_evac']
    self.total_hoods = initial_data['total_hoods']
    self.min_evac_cfm = generate_min_evac_cfm(self.height, self.surface_area, 
                                              self.ach_unoccupied, self.additional_evac)
    self.max_evac_cfm = generate_max_evac_cfm(self.height, self.surface_area, 
                                              self.ach_occupied, self.additional_evac)

  def __str__(self):
    return self.laboratory_name

def generate_min_evac_cfm(height, surface_area, ach_unoccupied, additional_evac):
  result = (height * surface_area + additional_evac) * ach_unoccupied
  return result / 10

def generate_max_evac_cfm(height, surface_area, ach_occupied, additional_evac):
  result = (height * surface_area + additional_evac) * ach_occupied
  return result / 10

def get_laboratory_for_id(id, laboratories):
  for laboratory in laboratories:
    if laboratory.laboratory_name == id:
      return laboratory
  return None