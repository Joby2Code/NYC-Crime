from pyspark import SparkContext
from csv import reader
from datetime import datetime


#Function Defintions
def checkFromDate(x):
    date = x.split('/')
    if len(date) != 3 :
        return 'NULL'
    try:
        m=int(date[0])
        d=int(date[1])
        y=int(date[2])
    except Exception as e:
        return 'NULL'
    if m not in range(1,13) or d not in range(1,32) or y not in range(2010,2017):
        return 'INVALID'
    else:
        return 'VALID'


sc = SparkContext();
csvData = sc .textFile("NYPD_Complaint_Data_Historic.csv");

#Create output partitions
crimeData = csvData.mapPartitions(lambda x:reader(x));

#Data Cleaning for valid time stamp: from_date
#Code snippet just takes the main RDD and creates a new RDD with the Valid date checker return output
fromDate = crimeData.map(lambda x: (x[0], (x[1], "DATE", "Complaint from date","date",checkFromDate(x[1]))))
fromDate.take(5);
#Save to file
fromDate.map(lambda x:x[1]).saveAsTextFile("fromdate.out")



#Stoppping Spark SparkContext
sc.stop()
