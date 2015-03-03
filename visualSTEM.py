import json
import pandas as pd
import random

#Read a CSV file of 100 users on 04/16
fnameSTEM = 'data/stem_sample_users_09_02_smaller.csv'
fnameSTEM_LA = 'data/stem_LA_sample_users_all_type_6_0902.csv'
with open(fnameSTEM_LA) as f:
    content = f.readlines()
print content[0]

fnameJsSTEM = 'data/visualDataSTEM.js'
#Choose the user_number we want : 22,34
with open(fnameJsSTEM, 'wb') as javaScriptFile:
    dictResults = {}
    dictLatLngArrays = {}
    for n in range(98):
        #Get one user with all the tracks
        user = content[n]
        print "Collecting data from user " + str(n)
        #Find the user id
        user_id = user[:user.find('[')]
        user = user[user.find('[')+1:]
        #Generate a pandas dataFrame
        d = {'lat':[],'lon':[],'timeStamp':[]}
        df = pd.DataFrame(d)


        index = 1
        count = 0
        #Go through the csv file to complete the pandas dataFrame
        while index >= 0:
                index = user.find('[')
                user = user[index+1:]
                if index >= 0:
                    #print 'we are in the loop'
                    lat = float(user[1:user.find(',')]) + ((random.random()-0.5)/500)
                    user = user[user.find(',')+1:]
                    lon = float(user[:user.find(']')]) + ((random.random()-0.5)/500)
                    user = user[user.find(',')+1:]
                    timeStamp = user[:user.find(']')]
                    df.loc[count] = [lat, lon, timeStamp]
                    count += 1
                    #Sort the dataFrame considering the timeStamp
        print "Number of points : ", count
        df = df.sort(['timeStamp'])
                    #print df
        LatLngArray = []
        #Fill an LatLng Array (usefull for Leaflet)
        for i in range(len(df) - 1):
            tmp = []
            tmpLatLon = []
            tmpLatLon.append(df.loc[i].lat)
            tmpLatLon.append(df.loc[i].lon)
            tmp.append(tmpLatLon)
            tmp.append(df.loc[i].timeStamp)
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
