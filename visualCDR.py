import json
import pandas as pd
import random

#Read a CSV file of 100 users on 04/16
fnameCDR = 'data/sample_users_all_type_0416_smaller.csv'
fnameSTEM = 'data/stem_sample_users_09_02_smaller.csv'
with open(fnameCDR) as f:
    content = f.readlines()
print content[0]

fnameJsCDR = 'data/visualDataCDR.js'
#Choose the user_number we want : 22,34
with open(fnameJsCDR, 'wb') as javaScriptFile:
    dictResults = {}
    dictLatLngArrays = {}
    for n in range(98):
        #Get one user with all the tracks
        user = content[n]
        print "Collecting data from user " + str(n)
        #Find the user id
        user_id = user[:user.find('[')]

        #Generate a pandas dataFrame
        d = {'lat':[],'lon':[],'timeStamp':[],'trackType':[]}
        df = pd.DataFrame(d)


        index = 1
        count = 0
        #Go through the csv file to complete the pandas dataFrame
        while index > 0:
                index = user.find('(')
                user = user[index+1:]
                if index >= 0:
                    #print 'we are in the loop'
                    track = user[:user.find(')')]
                    #print "track ## ",track
                    lat = float(track[3:track.find(',')-1]) + ((random.random()-0.5)/500)
                    track = track[track.find(',')+1:]
                    lon = float(track[3:track.find(',')-2]) + ((random.random()-0.5)/500)
                    track = track[track.find(',')+1:]
                    timeStamp = track[:track.find(',')]
                    trackType = track[track.find(',')+1:]
                    df.loc[count] = [lat, lon, timeStamp, trackType]
                    count += 1
                    #Sort the dataFrame considering the timeStamp
        print "Number of points : ", count
        df = df.sort(['timeStamp'])
                    #print df
        LatLngArray = []
        #Fill an LatLng Array (usefull for Leaflet)
        for i in range(len(df) - 1):
            tmp = []
            tmp.append(df.loc[i].lat)
            tmp.append(df.loc[i].lon)
            LatLngArray.append(tmp)

        #Write the variables on a file
        javaScriptFile.write('var LatLngArray_' + str(n) + ' = ')
        dictLatLngArrays['LatLngArray_' + str(n)] = LatLngArray
        javaScriptFile.write(str(LatLngArray))
        javaScriptFile.write('\n')
        dictionary = {}
        geo_data = {
            'type': 'FeatureCollection',
            'features': []
            }
        #Add the points to a geojson (usefull for Leaflet)
        for i in range(len(df)):
            feature = {
                'type': 'Feature',
                'geometry': {
                'type': 'Point',
                'coordinates': [df.loc[i].lon, df.loc[i].lat]
                },
                'properties': {
                'trackType': 'trackType: ' + str(df.loc[i].trackType),
                'timeStamp': 'timeStamp: ' + str(df.loc[i].timeStamp)
                }
                }
            geo_data['features'].append(feature)
        varname = 'user_' + str(n)
        dictResults[varname] = geo_data
        javaScriptFile.write('var ' + varname + ' = ')
        json.dump(geo_data, javaScriptFile, indent=2)
        javaScriptFile.write('\n')
    javaScriptFile.write('var ' + 'dictResults' + ' = ' + str(dictResults) + '\n')
    javaScriptFile.write('var ' + 'dictLatLngArrays' + ' = ' + str(dictLatLngArrays) + '\n')
