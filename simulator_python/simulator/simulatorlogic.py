def adjust_cfm_for_fumehood_state(series, fumehood):
  new_cfm = fumehood.finalcfm(series.ix['open'], True)
  series.ix['flow'] = new_cfm
  return series

def adjust_cfm_for_laboratory_parameters(cfm, laboratory):
  if cfm < laboratory.min_evac_cfm:
    return laboratory.min_evac_cfm
  if cfm > laboratory.max_evac_cfm:
    return laboratory.max_evac_cfm
  return cfm
