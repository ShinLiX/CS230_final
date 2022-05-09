"""
Name: Shin Li
CS230: Section 5
Data: Boston Crime
URL:

Description:
This project analyse data from boston crime in 2020 and display them on streamlit with various charts and graphs
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydeck as pdk

df = pd.read_csv("BostonCrime2022_8000_sample.csv")

pd.set_option("display.max_rows", 10, "display.max_columns", 10, 'display.width', None, 'max_colwidth', None)


df = df.drop(["OFFENSE_CODE_GROUP", "UCR_PART","SHOOTING"], axis = 1)
df_new = df.replace(0,np.nan).dropna()

print(df_new)

all_district = df_new["DISTRICT"].values.tolist()
print(all_district)
print(all_district)
district = []
for n in all_district:
    if n not in district:
        district.append(n)
print(district)


st.title("2020 Boston Crime Analysis")
st.sidebar.header("Inputs")

st.image("boston_crime.jpg",width=600)
st.markdown("##")
def converteddict(selected_row, selected_column, selected_district):

    select = df_new[df_new[selected_row] == selected_district][[selected_column]]
    select_list = select.astype(str).values.tolist()
    select_dict = {}
    for sublist in select_list:
        for item in sublist:
            if item not in select_dict.keys():
                select_dict[item] = 1
            else:
                select_dict[item] += 1

    return select_dict


incident_list = (df_new.loc[:,["DISTRICT"]].astype(str).values.tolist())
incident_dict = {}
for sublist in incident_list:
    for item in sublist:
        if item not in incident_dict.keys():
            incident_dict[item] = 1
        else:
            incident_dict[item] += 1

select_incident_number = st.sidebar.slider("The districts where incidents number less than: ", 0, 1050)
select_incident_list = []
for n in incident_dict:
    if incident_dict[n] < select_incident_number:
        select_incident_list.append(n)

st.sidebar.write(len(select_incident_list),'districts with incidents number less than',select_incident_number)

df_new.rename(columns={"Lat": "lat", "Long": "lon"}, inplace = True)
lat_list = []
lon_list = []
for n in district:
    e = df_new[df_new["DISTRICT"] == n][["lat"]].values.mean()
    f = df_new[df_new["DISTRICT"] == n][["lon"]].values.mean()
    lat_list.append(e)
    lon_list.append(f)
print(lat_list)
print(lon_list)

dict_data = {}
dict_data["district"] = district
dict_data["frequency"] = incident_dict.values()
dict_data["lat"] = lat_list
dict_data["lon"] = lon_list
print(dict_data)
df_data = pd.DataFrame(dict_data)
print(df_data)
print(df_data["lat"].mean())


st.subheader("Boston Map with incidents")

select_data = df_data[df_data["frequency"] <= select_incident_number]

layer1 = pdk.Layer(type = "ScatterplotLayer", # layer type
                   data=select_data, # data source
                   get_position='[lon, lat]',
                   get_radius=300,
                   get_color=[138,54,15],
                   pickable=True # work with tooltip
                   )

view_state = pdk.ViewState(
    latitude=df_data["lat"].mean(),
    longitude=df_data["lon"].mean(),
    zoom=11,
    pitch=0)

tool_tip = {"html": "District: <br/><b>{district}  </b>   Frequency:<br/> <b>{frequency}</b>   Latitude: <br/><b>{lat}</b>  longitude:<br/> <b>{lon}</b>",
            "style":{"backgroundColor": "salmon",
                     "color": "white"}
           }

my_map = pdk.Deck(
    map_style = 'mapbox://styles/mapbox/streets-v11',
    initial_view_state = view_state,
    layers = [layer1],
    tooltip=tool_tip
    )
st.pydeck_chart(my_map)
st.markdown("##")
st.markdown("##")
st.markdown("##")

select_district = st.sidebar.selectbox("Please select the district you are interested in: ", district)
if not select_district:
    st.write("Please select the district you are interested in")

dict_select_district_offenses = converteddict("DISTRICT","OFFENSE_DESCRIPTION",select_district)
offenses = dict_select_district_offenses.keys()
occurence = dict_select_district_offenses.values()
colors = ["Salmon","Steelblue","Gold","Darkseagreen"]
select_chart = st.sidebar.selectbox("Please select your preferred graph:",["","Bar Chart","Pie Chart"])

if select_chart == "Bar Chart":
    selected_bar_color = st.sidebar.radio("Please select color for your bar chart: ",colors)
    fig, ax = plt.subplots()
    ax.bar(offenses, occurence, color = selected_bar_color)
    ax.set_ylabel("Occurence")
    ax.set_xlabel("Offense description")
    ax.set_title("The number of different offense in the district you selected")
    st.pyplot(fig)
elif select_chart == "Pie Chart":

    max_num_of_occurence = int(st.sidebar.slider("Select the maximum number of incidents in that district",1,20))
    list_occurence = list(occurence)
    pie_occurence = list_occurence[:max_num_of_occurence]
    labels = [f'{l},    {s:0.2f}%' for l, s in zip(offenses, occurence)]
    fig, ax = plt.subplots()
    ax.pie(pie_occurence)
    plt.legend(labels, bbox_to_anchor = (1,0))
    st.pyplot(fig)

dict_select_district_month = converteddict("DISTRICT","MONTH",select_district)
dict_select_district_month= dict(sorted(dict_select_district_month.items()))
month = dict_select_district_month.keys()
number = dict_select_district_month.values()
st.markdown("##")
st.markdown("##")
st.markdown("##")
if select_chart:
    selected_line_color = st.sidebar.radio("Please select color for your line chart: ",colors)
    fig, ax = plt.subplots(figsize=(5,5))
    ax.plot(month, number, color = selected_line_color)
    ax.set_xlabel("Month")
    ax.set_ylabel("Occurence")
    ax.set_title("The change in total incidents' number of the district you chose over the four months")
    st.pyplot(fig)
