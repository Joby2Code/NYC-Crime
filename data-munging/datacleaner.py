from pyspark import SparkContext

sc = SparkContext();
csv = sc .textFile("NYPD_Complaint_Data_Historic");
