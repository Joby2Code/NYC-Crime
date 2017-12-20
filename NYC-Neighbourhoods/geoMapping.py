import geopandas
from shapely.geometry import Point
import numpy as np
import pandas as pd
import re


neighborhoods = geopandas.read_file('nynta_17d/nynta.shp')
dataset = pd.read_csv("/Users/pravarsingh/Desktop/Study Material/sem 3/Big Data Analytics/project/NYPD_Complaint_Data_Historic_Cleaned.csv", engine='python',index_col=None, header=None,error_bad_lines=False)
dataset[23] = None

#For handling invalid values
latlong_regex = re.compile(r'(\([^\(\)]+\))')


# Map crimes to neighborhoods
def find_neighborhood(x_coord, y_coord):
    '''
    Takes a pair of X and Y coordinates (using the NAD_1983_StatePlane_New_York_Long_Island coordinate system)
    and returns the corresponding New York City neighborhood.
    '''

    x_coord = re.sub(latlong_regex, r'\1', x_coord)
    y_coord = re.sub(latlong_regex, r'\1', y_coord)
    if np.isnan(x_coord) or np.isnan(y_coord):
        return np.nan

    matches = neighborhoods.geometry.contains(Point(x_coord, y_coord))

    if any(matches):
        return neighborhoods.loc[matches, 'NTAName'].values[0]

    return np.nan

years = range(2006, 2016)

for crime_type in ['felony', 'misdemeanor', 'violation']:
    for year in years:
        # Define filename
        folder = dataloc + '/bk_slice_' + crime_type + '/'
        filename = folder + crime_type + '_{}_desc_year_borough'.format(year)

         # Drop any rows that are missing x or y coordinates
        dataset = dataset[~pd.isnull(dataset[19])]
        dataset = dataset[~pd.isnull(dataset[20])]

        for index, row in dataset.iterrows():
            dataset[23][index] = find_neighborhood(row[19],row[20])
            print(dataset[23][index])

        dataset.to_csv(filename + "_with_hood.out", index=False)

#Usage:
#print(find_neighborhood(1004528,195225))