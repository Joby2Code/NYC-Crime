import pandas as pd
from scipy.stats import pearsonr

df = pd.read_csv("bedstuy_sales_with_felony_count.csv", sep=",", header = 0)

bedstuy_pearson_correlation = pearsonr(df['avg price'], df['count_felony'])

print("bedstuy pearson correlation: "+str(bedstuy_pearson_correlation))