import pandas as pd
from utils import delta_time, distance_on_unit_sphere

TOL = 1e-6

__author__ = 'jeromethai'


# ============================
# Methods to extract STEM data
# ============================


def add_raw_traj(line):
    """create panda dataframe with trajectory of one user
    from the STEM dataset
    """
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
            else: dist, deltatime = 0., 0.
            rows.append([lat, lon, time, dist, deltatime])
            old_lat, old_lon, old_time = lat, lon, time

    multi_index = pd.MultiIndex.from_tuples(zip([user_id]*len(rows), range(len(rows))))
    columns = ['lat', 'lon', 'timeStamp', 'dist_to_prev', 'time_to_prev']
    df = pd.DataFrame(rows, index = multi_index, columns = columns)
    return df


def csv_to_panda_traj(filepath, method):
    """Import the whole csv into panda using method that matches the csv format
    """
    list_df = []
    with open(filepath) as f:
        for i, line in enumerate(f): list_df.append(method(line))
    return pd.concat(list_df)



def remove_static_points(df, deltatime):
    """Remove consecutive points with same position within deltatime seconds
    for one trajectory"""
    if len(df) <= 2: return df
    rows, p1, p2 = [], 0, 1
    while p1 < len(df):
        rows.append(df.loc[p1].tolist())
        time = 0
        while p2 < len(df) and df.loc[p2]['dist_to_prev'] < TOL and df.loc[p2]['time_to_prev'] < deltatime:
            time += df.loc[p2]['time_to_prev']
            p2 += 1
        if p1 < p2-1: rows.append(df.loc[p2-1].tolist()[:-1] + [time])
        p1 = p2
        p2 = p2+1
    return pd.DataFrame(rows, columns = df.columns)


def filter_data(df):
    """Remove consecutive points with same position within deltatime seconds
    and static trajectories"""
    temp = []
    for user_id in df.index.levels[0]:
        print 'filter traj for', user_id
        if df.loc[user_id]['dist_to_prev'].sum() < 1.0: continue
        filtered_traj = remove_static_points(df.loc[user_id], 300)
        filtered_traj['user_id'] = user_id
        filtered_traj.set_index('user_id', append=True, inplace=True)
        temp.append(filtered_traj.reorder_levels(['user_id', None]))
    return pd.concat(temp)


def save_filtered_data():
    filepath = 'data/stem_LA_sample_users_all_type_6_0902.csv'
    traj_data = csv_to_panda_traj(filepath, add_raw_traj)
    print 'import complete, filter data'
    filtered_data = filter_data(traj_data)
    filtered_data.save('data/filtered_stem_LA_sample_users_all_type_6_0902.pkl')



# ===================================
# Methods to extract data from OSM_LA
# ===================================

def read_link(line):
    """read link 
    """
    return [float(e) for e in line.split(';')]


def csv_to_panda_link(filepath, savepath, method, columns, skip = False):
    """Import and save the whole csv into panda using method that matches the csv format
    """
    links = []
    with open(filepath) as f:
        for i, line in enumerate(f):
            if i == 0 and skip: continue
            links.append(method(line))
    df = pd.DataFrame(links, columns = columns)
    df.save(savepath)


def save_link_LA_OSM():
    filepath = 'data/OSM_LA.csv'
    savepath = 'data/OSM_LA.pkl'
    skip = True
    columns = ['lon1', 'lat1', 'lon2', 'lat2', 'flow/capacity',
            'travel_time/fftt', 'capacity', 'freespeed', 'length', 'fftt']
    csv_to_panda_link(filepath, savepath, read_link, columns, skip)



def main():
    #save_filtered_data()
    #df = pd.load('data/filtered_stem_LA_sample_users_all_type_6_0902.pkl')
    #for user_id in df.index.levels[0]:
    #    print df.loc[user_id]['dist_to_prev'].sum()
    #save_link_LA_OSM()
    df = pd.load('data/OSM_LA.pkl')
    print df
    

if __name__ == "__main__":
    main()

