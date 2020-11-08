#
# FastDev - Analyzing sales Data
#

# import packages
import pandas as pd
import numpy as np
import plotly.express as px
import os

########## Merge all 12 months of sales

files = [file for file in os.listdir("/") if "2019"in file ]

all_months_data = pd.DataFrame()
for file in files : 
  df = pd.read_csv("/"+file)
  all_months_data = pd.concat([all_months_data,df])
  
all_months_data.to_csv("all_month_data.csv" , index = False)

# duplicate header rows have been added to the DataFrame from the merging


######## Cleaning the data

# Make a dataFrame of rows that contain NaN value
nan_data = all_months_data[all_months_data.isna().any(axis=1)]

# Drop this rows from the DataFrame
df.dropna(how = "all")

# removing duplicate lines
all_months_data = all_months_data[all_months_data["Price Each"] != "Price Each"]


#### Question 1 : What was the best month of sales ? How much was earned that month ?

# add month column 
all_months_data["Month"] = all_months_data["Order Date"].str[0:2]

# adding a total column to get the total for each item ordered
all_months_data["total"] = all_months_data["Price Each"].astype("float") * all_months_data["Quantity Ordered"].astype(float)


# Convert the type of month from String to int
all_months_data['Month'] = all_months_data['Month'].astype('float')

# total Sales
total_sales = []
for m in range(1,13):
  total_sales.append(all_months_data.total[all_months_data["Month"] == m].sum())

######## Visualizing the data with plotly
total_sales = []
for m in range(1,13): # shorter version  df = all_months_data.groupby("Month").sum() 
  total_sales.append(all_months_data.total[all_months_data["Month"] == m].sum()) 



Month = ["January", "February" , "March" , "April" , "May" , "June" , "July" , "August" , "September" , "October" , "November" ,"December" ]

df = pd.DataFrame(list(zip(Month , somme)) , columns = ["Month" , "Total Sales"])


fig = px.bar(df , x ="Month" , y = "Total Sales" , title = "Total sales per month")

fig.show() # the best month for sales is Decemeber

#### Question 2 : What city had the highest number of sales ?

# Augmenting the data Set and adding a new column with the city of each order
###Cleaning the Data
number_of_missing_values_purchase_addresse = all_months_data['Purchase Address'].isnull().values.any().sum() #1

# drop the rows with NaN value for Purchase addresse

all_months_data.dropna(subset=['Purchase Address'] , inplace = True)
number_of_missing_values_purchase_addresse = all_months_data['Purchase Address'].isnull().values.any().sum()

# Augement the dataSet by adding a city column 
all_months_data['City'] = [ str(c).split(",")[1] for c in all_months_data['Purchase Address']]

# Group the sales by city
sales_by_city = all_months_data.groupby("City").sum())

######## Visualizing the data with plotly
#fig2 = px.bar()
