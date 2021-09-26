# -*- coding: utf-8 -*-
# Copyright 2018-2019 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example of showing geographic data."""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

st.markdown("""
<style>
.big-font {
    font-size:100px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Origins and Destinations of Travelling Data for Areas near Bangkok</p>', unsafe_allow_html=True)

st.title("By Siraphop Thanyapisetsak 6130828021")

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns(2)

with row1_1:
    date_select = st.selectbox("Date Selection",("Jan. 1, 2019", "Jan. 2, 2019","Jan. 3, 2019","Jan. 4, 2019","Jan. 5, 2019"))
    hour_selected = st.slider("Select hour of travelling", 0, 23)

with row1_2:
    st.write(
    """
    ##
    Examining the number of travelling started and destinations reached for areas near Bankok.
    By sliding the slider on the left and selecting date you can view different slices of date and time and explore different transportation trends.

    This website was made by Siraphop Thanyapisetsak Student NO. 6130828021
    """)

timedisplay = "Date Displayed : " + date_select
st.title(timedisplay)

# LOADING DATA
DATE_TIME = "date/time"

# ALL DATA URL
DATA20190101 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv")
DATA20190102 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190102.csv")
DATA20190103 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190103.csv")
DATA20190104 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190104.csv")
DATA20190105 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190105.csv")

#SELECT DATA ACCORDING TO date_select
if date_select == "Jan. 1, 2019" :
  DATA_URL = DATA20190101
elif date_select == "Jan. 2, 2019" :
  DATA_URL = DATA20190102
elif date_select == "Jan. 3, 2019" :
  DATA_URL = DATA20190103
elif date_select == "Jan. 4, 2019" :
  DATA_URL = DATA20190104
elif date_select == "Jan. 5, 2019" :
  DATA_URL = DATA20190105

@st.cache(persist=True)
def load_data_origin(nrows):
    datastart = pd.read_csv(DATA_URL, nrows=nrows)
    datastart = datastart[['timestart','latstartl','lonstartl']].copy()
    datastart = datastart.rename(columns = {'timestart': 'Date/Time', 'latstartl': 'Lat', 'lonstartl': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    datastart.rename(lowercase, axis="columns", inplace=True)
    datastart[DATE_TIME] = pd.to_datetime(datastart[DATE_TIME])
    return datastart

def load_data_destination(nrows):
    datastop = pd.read_csv(DATA_URL, nrows=nrows)
    datastop = datastop[['timestop','latstop','lonstop']].copy()
    datastop = datastop.rename(columns = {'timestop': 'Date/Time', 'latstop': 'Lat', 'lonstop': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    datastop.rename(lowercase, axis="columns", inplace=True)
    datastop[DATE_TIME] = pd.to_datetime(datastop[DATE_TIME])
    return datastop

data1 = load_data_origin(100000)

data2 = load_data_destination(100000)

# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

# FILTERING DATA BY HOUR SELECTED
#data = data[data[DATE_TIME].dt.hour == hour_selected]
data1 = data1[(data1[DATE_TIME].dt.hour == hour_selected) & (data1[DATE_TIME].dt.year == 2019)]

data2 = data2[(data2[DATE_TIME].dt.hour == hour_selected) & (data2[DATE_TIME].dt.year == 2019)]

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2 = st.columns(2)

# SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
zoom_level = 11
#midpoint1 = (np.average(data1["lat"]), np.average(data1["lon"]))
#midpoint2 = (np.average(data2["lat"]), np.average(data2["lon"]))
midpoint = [13.736717, 100.523186]

with row2_1:
    st.write("**All travelling started during %i:00 - %i:00**" % (hour_selected, (hour_selected + 1) % 24))
    map(data1, midpoint[0], midpoint[1], zoom_level)

with row2_2:
    st.write("**All destinations reached during %i:00 - %i:00**" % (hour_selected, (hour_selected + 1) % 24))
    map(data2, midpoint[0], midpoint[1], zoom_level)

# HISTOGRAM NUMBER 1

# FILTERING DATA FOR THE HISTOGRAM 1
filtered1 = data1[
    (data1[DATE_TIME].dt.hour >= hour_selected) & (data1[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist1 = np.histogram(filtered1[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data1 = pd.DataFrame({"minute": range(60), "travelling started": hist1})

# LAYING OUT THE HISTOGRAM SECTION 2

st.write("")

st.write("**Breakdown of all travelling started per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data1)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("travelling started:Q"),
        tooltip=['minute', 'travelling started']
    ).configure_mark(
        opacity=0.5,
        color='red'
    ), use_container_width=True)

# HISTOGRAM NUMBER 2

# FILTERING DATA FOR THE HISTOGRAM 2
filtered2 = data2[
    (data2[DATE_TIME].dt.hour >= hour_selected) & (data2[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist2 = np.histogram(filtered2[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data2 = pd.DataFrame({"minute": range(60), "destinations reached": hist2})

# LAYING OUT THE HISTOGRAM SECTION 2

st.write("")

st.write("**Breakdown of all destinations reached per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data2)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("destinations reached:Q"),
        tooltip=['minute', 'destinations reached']
    ).configure_mark(
        opacity=0.5,
        color='blue'
    ), use_container_width=True)
