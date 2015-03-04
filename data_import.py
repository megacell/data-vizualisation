import pandas as pd
from utils import delta_time, distance_on_unit_sphere

__author__ = 'jeromethai'

def add_raw_traj(line):
    p = line.find('[')
    user_id = line[:p-1]
    rows = [] 
    for j, e in enumerate(line[p+1:].split(', ')):

        if j%3 == 0: lat = float(e.strip('['))
        if j%3 == 1: lon = float(e.strip(']'))
        if j%3 == 2:
            time = e.strip('\n').strip(']').strip("'")
            if j/3 >= 1:
                # distance in km
                dist = 6373 * distance_on_unit_sphere(lat, lon, old_lat, old_lon)
                # time in sec
                deltatime = delta_time(old_time, time)
            else: 
                dist = None
                deltatime = None
            rows.append([lat, lon, time, dist, deltatime])
            old_lat, old_lon, old_time = lat, lon, time

    multi_index = pd.MultiIndex.from_tuples(zip([user_id]*len(rows), range(len(rows))))
    columns = ['lat', 'lon', 'timeStamp', 'dist_to_prev', 'time_to_prev']
    df = pd.DataFrame(rows, index = multi_index, columns = columns)
    return df


def csv_to_panda(filepath, add_traj):
    list_df = []
    with open(filepath) as f:
        for i, line in enumerate(f): list_df.append(add_traj(line))
    return pd.concat(list_df)


def main():
    filepath = 'data/stem_LA_sample_users_all_type_6_0902.csv'
    traj_data = csv_to_panda(filepath, add_raw_traj)
    print traj_data
    print traj_data.ix['196632997806448']
    print 'import complete'


if __name__ == "__main__":
    main()

"""
from datetime import datetime
datetime.strptime(end[11:19], '%H:%M:%S')
"""