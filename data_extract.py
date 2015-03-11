# ================================================
# Methods to convert STEM data in Panda to geojson
# ================================================

import pandas as pd

__author__ = 'jeromethai'

begin = 'var geojson_features = [{\n'

def begin_feature(type):
    string = '    "type": "Feature",\n    "geometry": {\n'
    begin_coord = '        "coordinates": [\n'
    return string + '        "type": "{}",\n'.format(type) + begin_coord

def coord(lat,lon,type):
    if type == "LineString": return '            [{}, {}],\n'.format(lon,lat)
    if type == "Point": return '            [{}, {}]'.format(lon,lat)

begin_prop = '            ]},\n    "properties": {\n'

def end_prop(next):
    if next: return '    }},{\n'
    return '    }}];\n'

def prop(name, value):
    return '        "{}": "{}",\n'.format(name, value)


def extract_all_trajectories(df):
    """create geojson LineString features from trajectories pandas dataframe
    generated in data_import.py"""
    out = ''
    out += begin
    for user_id in df.index.levels[0][:-1]:
    	out += extract_one_trajectory(df, user_id, True) 
    	out += end_prop(True)
    out += extract_one_trajectory(df, df.index.levels[0][-1], True)
    out += end_prop(False)
    return out


def extract_one_trajectory(df, user_id, called_by_extract_all_trajectories=False):
    """create geojson LineString features from trajectories pandas dataframe
    generated in data_import.py"""
    print 'convert trajectory for user {} to geoJson'.format(user_id)
    out = ''
    if not called_by_extract_all_trajectories: out += begin
    out += begin_feature("LineString")
    length, duration = 0., 0.
    for i in range(len(df.loc[user_id])):
    	row = df.loc[user_id].loc[i]
        if i > 0:
        	length += row['dist_to_prev']
        	duration += row['time_to_prev'] 
    	out += coord(row['lat'], row['lon'], "LineString")
    out += begin_prop
    out += prop('distance', length)
    out += prop('duration', duration)
    out += prop('user_id', user_id)
    out += prop('number_points', len(df.loc[user_id]))
    if not called_by_extract_all_trajectories: out += end_prop(False)
    return out


def to_geoJson_traj():
    df = pd.load('data/filtered_stem_LA_sample_users_all_type_6_0902.pkl')
    out = extract_all_trajectories(df)
    out += '\n'
    out += 'var lat_center_map = 33.982075\n'
    out += 'var lon_center_map = -118.28104\n'
    with open('visualization_data/all_trajectories.js', 'w') as f:
        f.write(out)


def to_geoJson_link():
    df = pd.load('data/OSM_LA.pkl')
    type = 'LineString'
    out = begin
    for i in range(len(df)):
        out += begin_feature(type)
        out += coord(df.loc[i]['lat1'], df.loc[i]['lon1'], type)
        out += coord(df.loc[i]['lat2'], df.loc[i]['lon2'], type)
        out += begin_prop
        out += prop('flow_over_capacity', df.loc[i]['flow/capacity'])
        out += prop('tt_over_fftt', df.loc[i]['travel_time/fftt'])
        out += prop('capacity', df.loc[i]['capacity'])
        out += prop('freespeed', df.loc[i]['freespeed'])
        out += prop('length', df.loc[i]['length'])
        out += prop('fftt', df.loc[i]['fftt'])
        if i < len(df)-1:
            out += end_prop(next = True)
        else:
            out += end_prop(next = False)
    out += '\n'
    out += 'var lat_center_map = 33.982075\n'
    out += 'var lon_center_map = -118.28104\n'
    with open('visualization_data/OSM_LA.js', 'w') as f:
        f.write(out)




def example():
    type = 'LineString'
    with open('visualization_data/dummy.js', 'w') as f:
        f.write(begin + begin_feature(type))
        f.write(coord(33.974394, -118.308914, type))
        f.write(coord(33.974465, -118.300266, type))
        f.write(coord(33.974465, -118.291554, type))
        f.write(begin_prop)
        f.write(prop('name1', 'value1'))
        f.write(prop('name2', 'value2'))
        f.write(end_prop(next = True))
        f.write(begin_feature(type))
        f.write(coord(33.974394, -118.308914, type))
        f.write(coord(33.974465, -118.300266, type))
        f.write(coord(33.974465, -118.291554, type))
        f.write(begin_prop)
        f.write(prop('name1', 'value1'))
        f.write(prop('name2', 'value2'))
        f.write(end_prop(next = False))



def main():
    #to_geoJson_traj()
    to_geoJson_link()



if __name__ == "__main__":
    main()