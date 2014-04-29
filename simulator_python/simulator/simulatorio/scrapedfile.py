import numpy as np
import pandas as pd

def load_hoods_datastream(file):
    """Turn DataStream into two Pandas DataFrames - open & flow """
    open_dict_scraped = {}
    flow_dict_scraped = {}
    data_stream = pd.read_csv(file,
                              skiprows = 1,
                              index_col=0,
                              parse_dates=True,
                              date_parser = lambda x: np.datetime64(x*1000000),
                              squeeze = True)
    data_stream.tz_localize('UTC', copy=False).tz_convert('EST', copy=False)
    data_stream.columns = ['BAC','flow','open']
    
    # Create table for an id lookup
    bac_to_id = {}
    for i in range(len(hood_info)):
        bac_to_id[hood_info['bac'][i]] = hood_info.index[i]
    
    # Divide into groups
    grouped = data_stream.groupby('BAC')
    
    for name, group in grouped:
        hood_id = bac_to_id[name]
        # Ditch duplicates in index
        group['index'] = group.index
        group.drop_duplicates(cols='index', take_last = True, inplace=True)
        # Save what we need
        open_dict_scraped[hood_id] = group['open']
        flow_dict_scraped[hood_id] = group['flow']
    
    # conversion to dataframe
    open_scraped = pd.DataFrame(open_dict_scraped)
    flow_scraped = pd.DataFrame(flow_dict_scraped)
    
    # resampling
    flow_data = flow_data.resample('5min',how='mean',fill_method='ffill',
                                   closed='left',label='left').resample('1H',how='mean',fill_method='ffill',
                                                                        closed='left',label='left') 
    open_data = open_data.resample('5min',how='mean',fill_method='ffill',
                                   closed='left',label='left').resample('1H',how='mean',fill_method='ffill',
                                                                        closed='left',label='left')

    return open_scraped, flow_scraped