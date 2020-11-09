#
# FastDev - Analyzing sales Data - Electronic Store
#   08-11-2020

# import packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime


########## Merge all 12 months of sales

files = [file for file in os.listdir("/content/") if "2019"in file ]

all_months_data = pd.DataFrame()
for file in files : 
  df = pd.read_csv("/content/"+file)
  all_months_data = pd.concat([all_months_data,df])
  
all_months_data.to_csv("all_month_data.csv" , index = False)


# duplicate header rows have been added to the DataFrame from the merging


######## Cleaning the data

# Make a dataFrame of rows that contain NaN value
nan_data = all_months_data[all_months_data.isna().any(axis=1)]

# Drop this rows from the DataFrame
all_months_data.dropna(how = "all")

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


# Months of the year
Month = ["January", "February" , "March" , "April" , "May" , "June" , "July" , "August" , "September" , "October" , "November" ,"December" ]


df = pd.DataFrame(list(zip(Month , total_sales)) , columns = ["Month" , "Total Sales"])


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
  #all_months_data['City'] = [ str(c).split(",")[1] for c in all_months_data['Purchase Address']] # method 1 using a list 

# function to extract the city and state acronym from adress
def get_city_state(x):
   return x.split(",")[1] + " (" + x.split(",")[2].split(" ")[1] + ")"

all_months_data["City"] = all_months_data['Purchase Address'].apply(lambda x : get_city_state(x)) # method 2 using the apply method

# Group the sales by city 
sales_by_city = all_months_data.groupby("City").sum()
sales_by_city.drop(columns="Month" , inplace=True)

######## Visualizing the data with plotly
fig2 = px.bar(sales_by_city , x = sales_by_city.index , y ="total" , title ="Total sales by City" ,labels = dict(x= "Us cities" , total = "Total sales in USD") )
fig2.show() 

    # The city with the highest sales is San Fransisco (CA)

#### Question 3 :  How much products are there ? What's the Product that made the best sales ?

# Group the sales by products
sales_by_product = all_months_data.groupby("Product").sum()
sales_by_product.drop(columns="Month" , inplace=True)

fig3 = px.bar(sales_by_product , x = sales_by_product.index , y ="total" , title ="Total sales by Product" ,labels = dict(x= "Products" , total = "Total sales in USD") )
fig3.show() 

#### Question 4 : What time should we display advertisements to maximize likelihood of customer's buying product ?
 # defining the time with most sales
# Target column : Order date

all_months_data["Order Date"].dtype # dtype('O') O is for Object

# Parsing dates "Convert Order Date columns to datetime"
  # Example : 06/23/19 19:34 %m/%d/%y %M:%S
  # should be : 2019-06-23    %d-%m-%y 
  # default order datetime (year-month-day)

all_months_data["Order Date"] = pd.to_datetime(all_months_data["Order Date"])

# check days are between 1 and 31
  # numerically 
days = all_months_data["Order Date"].dt.day.nunique() # 31 which is the expected result 
   
# add hour column to dataset
all_months_data["Hours"]  = all_months_data["Order Date"].dt.hour

# add minute column to dataset
all_months_data["Minutes"]  = all_months_data["Order Date"].dt.minute

# grouping by hours returns tuples of datframes and the indice it was grouped by
hours = [h for h in all_months_data.groupby("Hours")]

# list that returns the total count fo rorders for each hour of the day
l = [hours[x][1]["Hours"].count() for x in range(24)]

# Visualizing 
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x =[i for i in range(24)] , y = l,mode='lines+markers'))
# Edit the layout
fig4.update_layout(title='Total count of orders for each hour of the day',
                   xaxis_title='hours of the day (0-23)',
                   yaxis_title='Total count of orders made')
fig4.show() # the figure has 2 maximas so 11am and 19pm would be great time to start advertizing as they correspond to the total max of orders made


#### Question 6 : What products are most often sold together ?


