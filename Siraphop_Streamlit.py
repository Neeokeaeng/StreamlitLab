
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide",
                   page_title="Siraphop Streamlit",
                   page_icon =":car:")
#https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json
#https://hersanyagci.medium.com/introduction-to-streamlit-for-machine-learning-web-app-cd89c4181c33

st.markdown("""
<style>
.big-font {font-size:75px !important;color:black;}
.bgbg {background-image: url('https://www.trendingus.com/wp-content/uploads/2019/12/c1946e59f3f121584adce33f9133133d.jpeg');
background-repeat: no-repeat;background-attachment: fixed;background-size: 100% 100%;}
</style>
""", unsafe_allow_html=True)
#background: url("https://www.trendingus.com/wp-content/uploads/2019/12/c1946e59f3f121584adce33f9133133d.jpeg")

#st.markdown('<style>body{background-color: White;}</style>',unsafe_allow_html=True)

st.markdown('<div class="bgbg"><p class="big-font">Origins and Destinations of Travelling Data for Bangkok and Areas nearby🚘🚩</p></div>', unsafe_allow_html=True)

html_temp = """
<div style="background-color:grey;padding:1.5px">
<h1 style="color:white;text-align:left;font-size:30px;">By Siraphop Thanyapisetsak 6130828021 </h1>
</div><br>"""
st.markdown(html_temp,unsafe_allow_html=True)

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns(2)

with row1_1:
    date_select = st.selectbox("Date Selection",("Jan. 1, 2019", "Jan. 2, 2019","Jan. 3, 2019","Jan. 4, 2019","Jan. 5, 2019"))
    hour_selected = st.slider("Select hour of travelling", 0, 23)

with row1_2:
    st.info(
    """
    Examining the number of travelling started and destinations reached for Bangkok and areas nearby.
    By sliding the slider on the left and selecting date you can view different slices of date and time and explore different transportation trends.

    This website was created by Siraphop Thanyapisetsak Student NO. 6130828021
    """)

#timedisplay = "Date Displayed : " + date_select + " 🕒"
#st.title(timedisplay)

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
  html_temp = """
<div style="background-color:grey;padding:1.5px">
<h1 style="color:white;text-align:left;font-size:30px;">Date Displayed : Jan. 1, 2019  🕒</h1>
</div><br>"""
  st.markdown(html_temp,unsafe_allow_html=True)
  day_num,month_num,year_num = 1,1,2019
elif date_select == "Jan. 2, 2019" :
  DATA_URL = DATA20190102
  day_num,month_num,year_num = 2,1,2019
  html_temp = """
<div style="background-color:grey;padding:1.5px">
<h1 style="color:white;text-align:left;font-size:30px;">Date Displayed : Jan. 2, 2019  🕒</h1>
</div><br>"""
  st.markdown(html_temp,unsafe_allow_html=True)
elif date_select == "Jan. 3, 2019" :
  DATA_URL = DATA20190103
  day_num,month_num,year_num = 3,1,2019
  html_temp = """
<div style="background-color:grey;padding:1.5px">
<h1 style="color:white;text-align:left;font-size:30px;">Date Displayed : Jan. 3, 2019  🕒</h1>
</div><br>"""
  st.markdown(html_temp,unsafe_allow_html=True)
elif date_select == "Jan. 4, 2019" :
  DATA_URL = DATA20190104
  day_num,month_num,year_num = 4,1,2019
  html_temp = """
<div style="background-color:grey;padding:1.5px">
<h1 style="color:white;text-align:left;font-size:30px;">Date Displayed : Jan. 4, 2019  🕒</h1>
</div><br>"""
  st.markdown(html_temp,unsafe_allow_html=True)
elif date_select == "Jan. 5, 2019" :
  DATA_URL = DATA20190105
  day_num,month_num,year_num = 5,1,2019
  html_temp = """
<div style="background-color:grey;padding:1.5px">
<h1 style="color:white;text-align:left;font-size:30px;">Date Displayed : Jan. 5, 2019  🕒</h1>
</div><br>"""
  st.markdown(html_temp,unsafe_allow_html=True)

#LOAD DATA

@st.cache(persist=True)
def load_data_origin(nrows):
    datastart = pd.read_csv(DATA_URL, nrows=nrows)
    datastart = datastart[['timestart','latstartl','lonstartl']].copy()
    datastart = datastart.rename(columns = {'timestart': 'Date/Time', 'latstartl': 'Lat', 'lonstartl': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    datastart.rename(lowercase, axis="columns", inplace=True)
    datastart[DATE_TIME] = pd.to_datetime(datastart[DATE_TIME],format= '%d/%m/%Y %H:%M')
    return datastart
    
@st.cache(persist=True)
def load_data_destination(nrows):
    datastop = pd.read_csv(DATA_URL, nrows=nrows)
    datastop = datastop[['timestop','latstop','lonstop']].copy()
    datastop = datastop.rename(columns = {'timestop': 'Date/Time', 'latstop': 'Lat', 'lonstop': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    datastop.rename(lowercase, axis="columns", inplace=True)
    datastop[DATE_TIME] = pd.to_datetime(datastop[DATE_TIME],format= '%d/%m/%Y %H:%M')
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

# FILTERING DATA BY THE SELECTED DATE AND HOUR 
data1 = data1[(data1[DATE_TIME].dt.hour == hour_selected) & (data1[DATE_TIME].dt.day == day_num) & (data1[DATE_TIME].dt.month == month_num) & (data1[DATE_TIME].dt.year == year_num)]

data2 = data2[(data2[DATE_TIME].dt.hour == hour_selected) & (data2[DATE_TIME].dt.day == day_num) & (data2[DATE_TIME].dt.month == month_num) & (data2[DATE_TIME].dt.year == year_num)]

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2 = st.columns(2)

# SETTING THE ZOOM LOCATIONS FOR THE MAPS
zoom_level = 11

midpoint = [13.736717, 100.523186] #lat lon of Bangkok

with row2_1:
    st.info("**🚘All travelling started during %i:00 - %i:00🚘**" % (hour_selected, (hour_selected + 1) % 24))
    map(data1, midpoint[0], midpoint[1], zoom_level)

with row2_2:
    st.info("**🚩All destinations reached during %i:00 - %i:00🚩**" % (hour_selected, (hour_selected + 1) % 24))
    map(data2, midpoint[0], midpoint[1], zoom_level)

# HISTOGRAM NUMBER 1
# FILTERING DATA FOR THE HISTOGRAM 1
filtered1 = data1[(data1[DATE_TIME].dt.hour >= hour_selected) & (data1[DATE_TIME].dt.hour < (hour_selected + 1))]

hist1 = np.histogram(filtered1[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data1 = pd.DataFrame({"minute": range(60), "travelling started": hist1})

# LAYING OUT THE HISTOGRAM SECTION 2

st.write("")

st.info("**🚘Breakdown of all travelling started per minute between %i:00 and %i:00🚘**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data1)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("travelling started:Q"),
        tooltip=['minute', 'travelling started']
    ).configure_mark(
        opacity=0.5,
        color='blue'
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

st.info("**🚩Breakdown of all destinations reached per minute between %i:00 and %i:00🚩**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data2)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("destinations reached:Q"),
        tooltip=['minute', 'destinations reached']
    ).configure_mark(
        opacity=0.5,
        color='red'
    ), use_container_width=True)
