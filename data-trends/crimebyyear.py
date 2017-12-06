#This module filters the crime committed by year
import sys
import re
from pyspark import SparkContext
from csv import reader

#function definition
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


def getYear(x):
    if x != 'Null':
        return x.split('/')[2];


sc=SparkContext();
csvfile = sc.textFile(sys.argv[1], 1);
#csvfile = sc.textFile("NYPD_Complaint_Data_Historic.csv");

#Create output partitions
crimedata = csvfile.mapPartitions(lambda x:reader(x));

#Code to automate data collection with respect to year

for i in range (2005,2017):
    crimedata.map(lambda x:dateChecker(x[1],x[3],x[5])).filter(lambda x:getYear(x) == str(i)).map(lambda x: (x,1)).reduceByKey(lambda x,y:x+y).saveAsTextFile(str(i)+"_data.out");
