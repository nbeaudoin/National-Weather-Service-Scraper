
# coding: utf-8

# The goal of this tutorial is to derive the weekly weather forecast for the 
# Washington, DC area from teh National Weather Service. This is based on the 
# tutorial by DataQuest but adjusted to reflect a new region. For the previous 
# tutorial from DataQuest, please visit 
# https://www.dataquest.io/blog/web-scraping-tutorial-python/


# import modules
import requests
from bs4 import BeautifulSoup


# get weather from National Weather Service for Reagan National Airport
page = requests.get("http://forecast.weather.gov/MapClick.php?lat=38.878655000000066&lon=-77.09737999999996#.WjWaybQ-fOQ")
page


# download html as python object
soup = BeautifulSoup(page.content, 'html.parser')
soup


# get "seven-day-forecast" tags
seven_day = soup.find(id="seven-day-forecast")
seven_day


# get items in the "tombstone-container" 
forecast_items = seven_day.find_all(class_="tombstone-container")
forecast_items



# display the first item in seven day forecast
tonight = forecast_items[0]
print(tonight.prettify())


# get information from "period-name"
period = tonight.find(class_='period-name').get_text()
period


# extract text for the weather description
short_desc = tonight.find(class_='short-desc').get_text()
short_desc


# extract the temperature
temp = tonight.find(class_='temp').get_text()
temp


# extract the title
img = tonight.find('img')
desc = img['title']
desc


# extract all the information from the page
period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
periods

# get the three other fields
short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

print(short_descs)
print(temps)
print(descs)


# Combining our data into a Pandas Dataframe
import pandas as pd
weather = pd.DataFrame({
        "period": periods, 
        "short_desc": short_descs, 
        "temp": temps, 
        "desc":descs
    })
weather



# pull numeric values
temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
temp_nums


# find the mean of all hgih and low temps
weather["temp_num"].mean()

# select the rows that happen at night
is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night
is_night
weather[is_night]

