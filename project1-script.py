import pandas as pd
import os
import matplotlib.pyplot as plt

all_months_data = pd.DataFrame()

# list all the files in the Sales_Data directory 
files = [file for file in os.listdir('SalesAnalysis/Sales_Data/')]

# merge all the csv files into one csv
for file in files:
    df = pd.read_csv('SalesAnalysis/Sales_Data/' + file)
    all_months_data = pd.concat([all_months_data , df])

# create the new csv file that consists of all the data
all_months_data = all_months_data.dropna()
all_months_data = all_months_data.reset_index(drop=True)
all_months_data.to_csv('all_months_data_script.csv', index=False)

# Read data in updated dataframe 
all_data = pd.read_csv('all_months_data_script.csv')

# Task 2: Add month column
order_date = all_data['Order Date']

# this returns the first 2 characters in the 'Order Date' column -> indicates the month
month = order_date[0][:2] # 04 -> represents the month April
# print(type(month)) # <class 'str'>

# the data in the "Month" column are strings so we need to convert to numeric value
    # figure out error => ValueError: invalid literal for int() with base 10: 'Or'
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
# print(all_data['Month'].head(25))

# Task 3: need to add a sales column that represents the total purchase amount
    # realize that the 'Price Each' is also a <str> so need to convert to numeric vales
    # which will allow us to caluclate how much was earned each month etc. 

all_data = all_data[all_data['Quantity Ordered'] != 'Quantity Ordered']

all_data['Price Each'] = all_data['Price Each'].astype(float)
all_data['Quantity Ordered'] = all_data['Quantity Ordered'].astype('int32')
all_data['Total Sales'] = all_data['Price Each'] * all_data['Quantity Ordered']

# Question 1: What was the best month for sales? How much was earned that month?
    # need to figure out how much was made for each month
    # find which month made the most sales

results_month = all_data.groupby(['Month']).sum()
# print(total_sale_per_month['Total Sales']) # December had the best sales


# plot data to get a better representation 
months = range(1,13)
plt.figure(1)
plt.bar(months, results_month['Total Sales'])
plt.xticks(months)
plt.xlabel('Months')
plt.ylabel('Sales (USD)')
# plt.show()

# Question 2: What city had highest number of sales?

# how to access just the city from the 'Purchase Address' Column 

all_data['Location'] = all_data['Purchase Address'].apply(
    lambda place: place.split(',')[1] + ", " + place.split()[-2]
)

# print(all_data['Location'].head())

result_city = all_data.groupby(['Location']).sum()

# print(result_city)
plt.close()
cities = [city for city, df in all_data.groupby('Location')]
plt.figure(2)
plt.bar(cities, result_city['Total Sales'])
plt.xticks(rotation='vertical', size=8)
plt.xlabel('Cities')
plt.ylabel('Total Sales (USD $)')
plt.title('Total Sales Made in Each City')
# plt.show()

plt.close()


# Question 3: What time should advertisements be put out to maximize likelihood of customer purchases?
    # determine what time frame were most purchases made (between each hour)

# change 'Order Date' column to a datetime object
from datetime import datetime 

# all_data['Order Date'] = all_data['Order Date'].apply(
#     lambda time: datetime.strptime(time, '%m/%d/%y %H:%M')
# )

# easier way to apply datetime:
all_data['Order Date'] = pd.to_datetime(all_data['Order Date']) # gives us this format YYYY/MM/D HH:MM:SS

# extract the hour
all_data['Hour'] = all_data['Order Date'].dt.hour

# print(all_data.head())

hour_purchase = all_data.groupby('Hour')['Total Sales'].sum().reset_index()
# print(hour_purchase)
# print(all_data.columns)

# print(hour_purchase[hour_purchase['Total Sales'] == hour_purchase['Total Sales'].max()])

# It seems that 7PM had the most sales and it the best time to put out advertisements







