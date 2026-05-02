#!/usr/bin/env python
# coding: utf-8

#pip install folium


import pandas as pd
import numpy as np
import folium
import branca.colormap as cm

df = pd.read_csv('/Users/champ/Documents/Jason/Data Analysis/Tornado/1950-2021_all_tornadoes.csv')

df = df[(df.sg == 1)] # Uses only data from entire segment
df = df.reset_index(drop=True)

#lat and long for geographic center of contiguous US
latitude = 39.833333 
longitude = -98.583333

# set a starting map using the above lat and long
tornado_map = folium.Map(location = [latitude, longitude], zoom_start = 5)

def popup_html(row):
    index = row
    date = df['date'].iloc[index]
    magnitude = df['mag'].iloc[index]
    length = df['len'].iloc[index]

    html = folium.Html(
            f"""
<!DOCTYPE html>
<html>
    <table>
    <tbody>
        <tr>
            <td>Date: </td>
            <td>{date}</td>
        </tr>
        <tr>
            <td>Magnitude: </td>
            <td>{magnitude}</td>
        </tr>
        <tr>
            <td>Length: </td>
            <td>{length}</td>
        </tr>
     </tbody>
     </table>
</html>
           """,
           script=True)


    return html

colormap = cm.LinearColormap(colors=['cadetblue', 'orange', 'darkblue', 'red', 'purple', 'darkred'], vmin=0, vmax=5)

for index, row in df.iterrows():

    date = df['date'].iloc[index]
    magnitude = df['mag'].iloc[index]
    length = df['len'].iloc[index]

    html = folium.Html(
            f"""
<!DOCTYPE html>
<html>
    <table style="height: 80px; width: 200px;">
    <tbody>
        <tr style="height:20px">
            <th style="width:150px">Date: </th>
            <td style="text-align: left; width:200px">{date}</td>
        </tr>
        <tr style="height:20px">
            <th style="width:100px">Magnitude: </th>
            <td style="text-align: left; width:200px">{magnitude}</td>
        </tr>
        <tr style="height:20px">
            <th style="width:100px">Length: </th>
            <td style="text-align: left; width:200px">{length}</td>
        </tr>
     </tbody>
     </table>
</html>
           """,
           script=True)

    if  row['elat'] == 0 and row['elon'] == 0:
        folium.Circle(location=[row['slat'], row['slon']],
        #html = popup_html(index),
        popup=folium.Popup(html),        
        radius = 8,
        color=colormap(df.iloc[index]['mag']),
        ).add_to(tornado_map)

    else:
        folium.PolyLine([[row['slat'], row['slon']], 
        [row['elat'], row['elon']]],
        #html = popup_html(index),
        popup=folium.Popup(html),
        color=colormap(df.iloc[index]['mag']),
        weight=3).add_to(tornado_map)

tornado_map

tornado_map.save("/Users/champ/Documents/Jason/Data Analysis/Tornado/tornado_map_color_coded.html")


