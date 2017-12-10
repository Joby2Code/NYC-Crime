#This module filters the crime per precinct in a bourough
import sys
import re
from pyspark import SparkContext
from csv import reader

def check_precinct(x):
    if x is None or x == '':
        return 'NULL'
    try:
        p = int(x)
    except Exception as e:
        return 'NULL'
    if p in range(1, 124):
        return p
    else:
        return 'NULL'


sc=SparkContext();
csvfile = sc.textFile(sys.argv[1], 1);
#csvfile = sc.textFile("NYPD_Complaint_Data_Historic.csv");

#Create output partitions
crimedata = csvfile.mapPartitions(lambda x:reader(x));

borough=['MANHATTAN', 'BRONX', 'BROOKLYN', 'QUEENS', 'STATEN ISLAND']

for i in range(0,len(borough)):
    crimedata.map(lambda x:(x[13],check_precinct(x[14]),x[11])).filter(lambda x:x[0]== borough[i] and x[1] != 'NULL').map(lambda x: ((x[1],x[2]),1)).reduceByKey(lambda x,y:x+y).map(lambda x:(x[0][0],x[0][1],x[1])).saveAsTextFile(borough[i]+"_precinct.out")
