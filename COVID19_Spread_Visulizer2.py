import pandas as pd
import folium
from flask import Flask, render_template

"""Put the data resource doc here"""
data_resource = "covid-19-dataset-2.csv"

"""Put how many countries you want to see in the data visulizer"""
numbers_of_top_countries = 15

"""Panda will read the csv type data resource"""
covid_data = pd.read_csv(data_resource)
# print(corona_data)

"""Group data by country and only shows the column for Confirmed, Deaths, Recovered and Active"""
covid_data＿by_country = covid_data.groupby("Country_Region").sum()[
    ["Confirmed", "Deaths", "Recovered", "Active"]
]
# print(covid_data＿by_country)

""""Sort only the top Confirmed countries"""
covid_top＿confirmed_country = covid_data＿by_country.nlargest(numbers_of_top_countries, "Confirmed")[
    ["Confirmed"]
]
# print(covid_top＿confirmed_country)

""""Drop those incomplete data (a.k.a. NA data)"""
covid_data = covid_data.dropna()
# print(covid_data)

map_of_covid = folium.Map(
    location=[34.223334, -82.461707], tiles="Stamen toner", zoom_start=8
)


def circle_maker(x):

    folium.Circle(
        location=[x[0], x[1]],
        radius=float(x[2]),
        color="red",
        popup="confirmed cases:{}".format(x[2])).add_to(map_of_covid)


covid_data[["Lat", "Long_", "Confirmed"]].apply(lambda x: circle_maker(x), axis=1)
html_map = map_of_covid._repr_html_()
pairs=[(country, confirmed) for country, confirmed in zip(covid_top＿confirmed_country.index, covid_top＿confirmed_country['Confirmed'])]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html", table=covid_top＿confirmed_country, cmap=html_map, pairs=pairs)

if __name__=="__main__":
    app.run(debug=True)