import pandas as pd

__author__ = 'jeromethai'

def add_raw_traj(line):
    """append trajctory of user in line at the end of traj_data"""    
    p = line.find('[')
    user_id = line[:p-1]
    rows = [] 
    for j, e in enumerate(line[p+1:].split(', ')):
        if j%3 == 0: lat = float(e.strip('['))
        if j%3 == 1: lon = float(e.strip(']'))
        if j%3 == 2: rows.append([lat, lon, e.strip('\n').strip(']').strip("'")])
    multi_index = pd.MultiIndex.from_tuples(zip([user_id]*len(rows), range(len(rows))))
    df = pd.DataFrame(rows, index = multi_index, columns = ['lat', 'lon', 'timeStamp'])
    return df


def csv_to_panda(filepath, add_traj):
    """add trajectories in csv to traj_data and user_data
    
    traj_data contains all the points from all ids
    columns of traj_data: [lat, lon, timeStamp]

    user_data enables to retrieve the sequence of points associated to a user_id
    user_id: from the csv
    start_index: index of the first point in the sequence in traj_data
    end_index: infdex of the last point in the sequence in traj_data
    """
    list_df = []
    with open(filepath) as f:
        for i, line in enumerate(f): list_df.append(add_traj(line))
    return pd.concat(list_df)


def main():
    filepath = 'data/stem_LA_sample_users_all_type_6_0902.csv'
    traj_data = csv_to_panda(filepath, add_raw_traj)
    print traj_data.ix['196632997806448']
    #print len(traj_data)
    print 'import complete'


if __name__ == "__main__":
    main()

