import numpy as np
import datetime
from pyspark import SparkContext
import sys
from csv import reader

#Function definition

#Validates each date
def validateDate(x):
    try:
        date = x.split('/')
        if len(date) >= 1:
            m=int(date[0]);
            d=int(date[1]);
            y=int(date[2]);
            if(m in range (1,13) and d in range (1,32) and y in range(2005,2017)):
                return 'VALID';
            else:
                return 'INVALID'
        else:
            return 'INVALID';
    except Exception as e:
        return 'INVALID';

#filters for valid date entries
def dateChecker(x,y,z):
    status = validateDate(x);
    if status == 'VALID' :
        return x;
    else :
        status = validateDate(y)
        if status == 'VALID' :
            return y;
        else :
            if validateDate(z) == 'VALID' :
                return z
            else:
                return 'Null'


#Bourough Check
def checkBorough(x):
    if x is None:
        return 'NULL'
    elif x in ['MANHATTAN', 'BRONX', 'BROOKLYN', 'QUEENS', 'STATEN ISLAND']:
        return x
    else:
        return 'NULL'

def getYear(x):
    if x != 'Null':
        return x.split('/')[2];


sc=SparkContext();
#csvfile = sc.textFile(sys.argv[1], 1);
csvfile = sc.textFile("NYPD_Complaint_Data_Historic.csv");

#Create output partitions
crimedata = csvfile.mapPartitions(lambda x:reader(x));


crimedata.map(lambda x:(dateChecker(x[1],x[3],x[5]),checkBorough(x[13]))).filter(lambda x:x[1] != 'NULL').map(lambda x:((getYear(x[0]),x[1]),1)).reduceByKey(lambda x,y:x+y).map(lambda x:(x[0][0],x[0][1],x[1])).saveAsTextFile("crime-bourough-per-year.out")
