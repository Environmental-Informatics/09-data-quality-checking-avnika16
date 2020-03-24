#!/bin/env python
# Script to import a dataframe, remove NA values, check for gross errors and check individual data values. Version of program_09_template.py. 
# Author- Avnika Manaktala
import pandas as pd
import numpy as np

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    # add your code here
    nochg= DataDF.isna() #Changes
    totalnochg= nochg.sum() #Sum of changes
    
    DataDF= DataDF.where(DataDF> -990) #Replace NA values 
    #Counting NAs in dataframe per data type and saving to MissingValues
    ReplacedValuesDF.loc["1. No Data",:] = DataDF.isna().sum() - totalnochg

    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # add your code here
    nochg= DataDF.isna() #Changes
    totalnochg= nochg.sum() #Sum of changes
    
    #Checking gross- precipitation
    DataDF.Precip = DataDF.Precip.where( np.logical_and( DataDF.Precip >= 0., 
                                                        DataDF.Precip <= 25 ))

    #Checking for gross errors- temperature 
    tempDF = DataDF.loc[:,["Max Temp","Min Temp"]]
    tempDF = tempDF.where( np.logical_and( tempDF >= -25., tempDF <= 35.))
    DataDF.loc[:,["Max Temp","Min Temp"]] = tempDF
    
    #Checking for gross errors- wind
    DataDF.loc[:,"Wind Speed"] = DataDF.loc[:,"Wind Speed"].where(
            np.logical_and(DataDF.loc[:,"Wind Speed"] >= 0., 
            DataDF.loc[:,"Wind Speed"] <= 25))   
    
    #Counting NAs in dataframe per data type and saving to MissingValues
    ReplacedValuesDF.loc["2. Gross Error",:] = DataDF.isna().sum() - totalnochg

    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here
    # Changes
    count = 0
    ReplacedValuesDF.loc["3. Swapped",:] = count
    
    # check values for Tmax and Tmin (Tmax>Tmin)
    for x in DataDF.index:
        if ( DataDF.loc[x,"Min Temp"] > DataDF.loc[x,"Max Temp"] ):
            tmp = DataDF.loc[x,"Max Temp"]
            DataDF.loc[x,"Max Temp"] = DataDF.loc[x,"Min Temp"]
            DataDF.loc[x,"Min Temp"] = tmp
            count = count + 1
    
    # count number of Nans per data type, and save to MissingValues
    ReplacedValuesDF.loc["3. Swapped",["Max Temp","Min Temp"]] = count

    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # add your code here
    nochg= DataDF.isna() #Changes
    totalnochg= nochg.sum() #Sum of changes
    
    # Tmax and Tmin < 25 C
    rangec = 0
    for x in DataDF.index:
        if ( DataDF.loc[x,"Max Temp"] - DataDF.loc[x,"Min Temp"] > 25. ):
            DataDF.loc[x,"Max Temp"] = np.NaN
            DataDF.loc[x,"Min Temp"] = np.NaN
            rangec = rangec + 1
    
    # count number of Nans per data type, and save to MissingValues
    ReplacedValuesDF.loc["4. Range Fail",:] = DataDF.isna().sum() - totalnochg

    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    
    
## Creating plots
#    
#import matplotlib.pyplot as plt #importing packages
#
##Creating Variable for original data
#Open= ReadData('/Users/Avnika/Documents/GitHub/09-data-quality-checking-avnika16/DataQuality_tutorial/DataQualityChecking.txt')
#RawData = Open[0]
#
##Precipitation plot 
#
#plot1= plt.figure()
#ax1= plot1.add_subplot(111)
#ax1.scatter(x=DataDF.index.values, y=RawData['Precip'], marker='.', label="Raw Data")
#ax1.scatter(x=DataDF.index.values, y=DataDF['Precip'],  marker='.', label='Processed Data')
#plt.xlabel('Time')
#plt.ylabel('Precipitation (mm)')
#plt.title('Precipitation- Variable Correction')
#plt.legend(loc = 'lower left')
#plt.savefig('amanakta_precipitation.pdf')
#
##Max temp plot
#fig2 = plt.figure()
#ax2 = fig2.add_subplot(111)
#ax2.scatter(x=DataDF.index.values, y=RawData['Max Temp'], marker='.', label="Raw Data")
#ax2.scatter(x=DataDF.index.values, y=DataDF['Max Temp'],  marker='.', label='Processed Data')
#plt.xlabel('Date')
#plt.ylabel('Max Temperature (Celsius)')
#plt.title('Max Temperature- Variable Correction')
#plt.legend(loc = 'lower left')
#plt.savefig('amanakta_max_temp.pdf')
#
##Min temp plot
#
#fig2 = plt.figure()
#ax2 = fig2.add_subplot(111)
#ax2.scatter(x=DataDF.index.values, y=RawData['Min Temp'],  marker='.', label="Raw Data")
#ax2.scatter(x=DataDF.index.values, y=DataDF['Min Temp'],  marker='.', label='Processed Data')
#plt.xlabel('Date')
#plt.ylabel('Min Temperature (Celsius)')
#plt.title('Min Temperature- Variable Correction')
#plt.legend(loc = 'lower left')
#plt.savefig('amanakta_min_temp.pdf')
#
##Wind speed plot
#
#fig2 = plt.figure()
#ax2 = fig2.add_subplot(111)
#ax2.scatter(x=DataDF.index.values, y=RawData['Wind Speed'],  marker='.', label="Raw Data")
#ax2.scatter(x=DataDF.index.values, y=DataDF['Wind Speed'],  marker='.', label='Processed Data')
#plt.xlabel('Date')
#plt.ylabel('Wind Speed (m/s)')
#plt.title('Wind Speed- Variable Correction')
#plt.legend(loc = 'upper right')
#plt.savefig('amanakta_wind_speed.pdf')
#
##Saving tables to txt files
#
#DataDF.to_csv('Processeddata.txt', sep='\t', index=True) #writing the corrected data to a tab-delimited text file
#ReplacedValuesDF.to_csv('ReplacedValueInfo.txt', sep='\t', index=True) #writing the correctio info to a tab-delimited text file