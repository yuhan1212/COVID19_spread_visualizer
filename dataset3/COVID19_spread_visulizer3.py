import pandas as pd
import folium
from flask import Flask, render_template

"""Get Data"""

# Put the data resource doc here
data_resource = "covid-19-dataset-3.csv"

# Put how many tops you want to see in the data visulizer
numbers_of_top_province = 15

# Panda will read the csv type data resource
covid_data = pd.read_csv(data_resource)


"""Deal with Data of Numbers"""
# Group data by province and only shows the column for Confirmed, Deaths, Recovered and Active
covid_data＿by_province = covid_data.groupby("Province_State").sum()[
    ["Confirmed", "Deaths", "Recovered", "Active"]
]

# Sort only the top Confirmed countries
covid_data＿by_province = covid_data＿by_province.nlargest(
    numbers_of_top_province, "Confirmed"
)[["Confirmed"]]


"""Deal with Data of Graph"""
# Keep only location and confirmed numbers
covid_data = covid_data[["Lat", "Long_", "Confirmed"]]

# Drop those incomplete data (a.k.a. NA data)
covid_data = covid_data.dropna()

# Map first show location
map_of_covid = folium.Map(
    location=[34.223334, -82.461707], tiles="Stamen toner", zoom_start=4
)

# Circle on map
def circle_maker(x):

    folium.Circle(
        location=[x[0], x[1]],
        radius=float(x[2]),
        color="red",
        popup="confirmed cases:{}".format(x[2]),
    ).add_to(map_of_covid)

# Apply circle to map
covid_data.apply(lambda x: circle_maker(x), axis=1)
html_map = map_of_covid._repr_html_()
pairs = [
    (country, confirmed)
    for country, confirmed in zip(
        covid_data＿by_province.index, covid_data＿by_province["Confirmed"]
    )
]

"""Implement on app"""
app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "home.html", table=covid_data＿by_province, cmap=html_map, pairs=pairs
    )

"""Run app"""
if __name__ == "__main__":
    app.run(debug=True)
