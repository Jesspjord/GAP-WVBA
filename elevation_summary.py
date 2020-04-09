# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 15:37:40 2020

@author: nmtarr

Description: Code to retrieve elevation parameters from GAP data, both the 
models and the maps.  Results are saved in a csv file.  

The general workflow is to loop through species list (GAP WV birds) and 
retrieve the max and min elevation parameters from the model dictionaries/json.
Then, use the habitat map to determine the elevations of the highest (max) and
lowest (min) grid cells that were identified as habitat.

These processes generate several variables with integer format that can be 
written to a results dataframe and csv.

NOTES:
Since WVBBA only looked at breeding season, we are only concerned with summer
(and year-round) data from GAP.

This code is full of holes and will need to be added to considerably in order
to run it.
"""
from datetime import datetime
import pandas as pd
import json
import sciencebasepy as sb

# Set paths to data
projDir = "P:/Proj6/GAP-WVBA/"
dataDir = projDir + "Data/"
habitatDir = projDir + "Data/habmaps/"
listDir = dataDir + 'Specieslists/WV_AtlasCodes.csv'
resultsCSV = projDir + "Results/elevation_summary.csv"
toDir = "T:/Temp/"


# Connect
sb = sb.SbSession()

# Create a function for retrieving the elevation parameter from sciencebase
def elev_from_model(gap_id, parameter, region):
    """
    Downloads GAP habitat model dictionary (json) and retrieves the elevation
    setting.
    
    Parameters:
    gap_id -- GAP species code
    parameter -- either "max" or "min"
    region -- number of region
    
    Example:
    elev = elev_from_model('bAMROx', 'max', '6')
    """
    ######## FILL OUT BY FOLLOWING example_read_json.py
    # Get a python list of species codes to loop through.
    species_list = pd.read_csv(listDir, dtype={'strUC': 'string'}) 
    #i = "bWOTHx"  
    for gap_id in species_list['strUC'] : 
        try:
            gap_id = gap_id[:1] + gap_id[1:5].upper() + gap_id[-1:]
            print(str("Retreiving data for") + gap_id)  
    
    # Search for gap model item in ScienceBase
            gap_id = gap_id[0] + gap_id[1:5].upper() + gap_id[5]
            item_search = '{0}_CONUS_HabModel_2001v1.json'.format(gap_id)
            items = sb.find_items_by_any_text(item_search)

    # Get a public item.  No need to log in.
            mod =  items['items'][0]['id']
            item_json = sb.get_item(mod)
            sb.get_item_files(item_json, toDir)

    # Read in the json of the model
            with open(toDir + gap_id + "_CONUS_HabModel_2001v1.json", 
                      "r") as inJSON:
                model_json = json.load(inJSON)

    # Drill down to the species models
            mods = model_json["models"]
            NE_summer_primary = [x[1] for x in mods[gap_id +  str('-s3')]
                                 ['PrimEcoSys']]
            SE_summer_primary = [x[1] for x in mods[gap_id +  str('-s6')]
                                 ['PrimEcoSys']]   
    
        except Exception as e: 
            print((str("Retreiving data for")) + gap_id + (str("failed.")) + e)
    # Return elevation
    return elevation

"""
# Create a function for retrieving the elevation min or max from hab map
def elev_from_map(gap_id, parameter):
    """
    Assessess GAP habitat map against elevation raster to determine the max
    or min elevation of suitable habitat grid cells (summer).
    
    Parameters:
    gap_id -- GAP species code
    parameter -- either "max" or "min"
    
    Example:
    elev = elev_from_map('bAMROx', 'max')
    """
    ######## Not sure yet the best way to do this. arcpy? 
    # Return elevation
     return elevation
"""

# Read in elevation.csv as a dataframe and save a copy in the archive
inDF = pd.read_csv(resultsCSV)
timestamp = str(datetime.now(tz=None).strftime("%d%B%Y_%I%M%p"))
archiveCSV = projDir + "/Results/Archive/elevation_" + timestamp + ".csv"
newDF = inDF.copy()
newDF.to_csv(archiveCSV)
workDF = pd.read_csv(archiveCSV)
species_list = pd.read_csv(listDir, dtype={'strUC': 'string'}, index_col=0) 
for i in species_list['strUC'] :
    workDF = pd.concat(workDF, 0, 'outer', '', (['strUC'], 'GAP_code')) 
workDF.to_csv(archiveCSV)

# Get a python list of species codes to loop through.
species_list = pd.read_csv(listDir, dtype={'strUC': 'string'}) 
#i = "bWOTHx"  
for i in df['strUC'] : 
    try:
        i = i[:1] + i[1:5].upper() + i[-1:]
        print(i) 
        dataset = rangDir + i + '_CONUS_01S_2001v1.tif'  

# For each species, determine the model parameters, and record in the results
# dataframe
#for sp in species_list:
#    print(sp)
    # Here's a start for how you'd use the function to get data from the hab model
    max_s6 = elev_from_model(sp, 'max', '6')
    newDF.loc[sp, 'GAP_max_SE'] = max_s6
    # Get the max elevation from the habitat map
    max_map = elev_from_map(sp, 'max')
    newDF.loc[sp, 'GAP_max_map'] = max_map
    
# newDF.to_csv(resultsCSV)

