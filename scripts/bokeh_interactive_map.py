"""
Script to plot interactive plots for maps showing the geographic locations of the studied groups/populations.
"""
__author__ = 'Cesar Fortes-Lima'

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import sys, random, csv
from tabulate import tabulate

# bokeh
from bokeh.io.export import export_svgs, export_png
from bokeh.io import show, output_file
from bokeh.plotting import figure, ColumnDataSource
from bokeh.palettes import Spectral, RdYlBu, RdYlGn
from bokeh.transform import linear_cmap,factor_cmap
from bokeh.layouts import row, column
from bokeh.models import Label, GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.models import Legend, HoverTool, LegendItem, WheelZoomTool, ColumnDataSource

parser = argparse.ArgumentParser(description='Parse some args')
parser.add_argument('-i', '--input', default='', help='input file')
parser.add_argument('-o', '--output', help='uses .png or .pdf suffix to determine type of file to plot')
parser.add_argument('-t', '--title', default='', action='store')
parser.add_argument('-a', '--add_info', default='', action='store')
parser.add_argument('-f', '--add_figure', default=None, action='store')
parser.add_argument('-w', '--width', default='2000', action='store')
parser.add_argument('-l', '--legend', default=None, help='None to remove the legend')
args = parser.parse_args()

# Usage:
# python3 bokeh_interactive_map.py -i Suppl_Fig_Map2/Bantu_Full_df.csv -o Fig.S_1_Maps/Suppl_Fig_Map2 # Full_AfricanNeo_bokeh_interactive_map
# 

out = args.output
df= pd.read_csv(args.input, index_col= 0)
df.head()
source = df
source.set_index('Population')
fids = source.Population.unique()
labels = fids
width= args.width

# Define function to switch from lat/long to mercator coordinates
def x_coord(x, y):
	lat= x
	lon= y 
	r_major= 6378137.000
	x= r_major * np.radians(lon)
	scale= x/lon
	y= 180.0/np.pi * np.log(np.tan(np.pi/4.0 + lat * (np.pi/180.0)/2.0)) * scale
	return (x, y)

# Define coord as tuple (lat,long)
df['coordinates']= list(zip(df['Latitude'], df['Longitude']))

# Obtain list of mercator coordinates
mercators= [x_coord(x, y) for x, y in df['coordinates'] ]

# Create mercator column in our df
df['mercator']= mercators

# Split that column out into two separate columns - mercator_x and mercator_y
df[['mercator_x', 'mercator_y']]= df['mercator'].apply(pd.Series)

# Examine our modified DataFrame
df.head()
# Tell Bokeh to use df as the source of the data
# source= ColumnDataSource(data= df)

# Choose palette
palette= Spectral[11]

# Define color mapper - which column will define the colour of the data points
# color_mapper= linear_cmap(field_name= 'Latitude', palette= palette, low= df['Latitude'].min(), high= df['Latitude'].max())
palette= df['Colour']

# Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful
tooltips= [("Group","@Group"), ("Population","@Population"), ("N samples","@N_samples")]

# Create figure
output_file(args.output+'.html', mode='inline')
plot= figure(title= args.title, toolbar_location="above", x_axis_type= "mercator", x_axis_label= 'Longitude', y_axis_type= "mercator", y_axis_label= 'Latitude', height = 1000, width = int(width), 
	tooltips= tooltips, tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color=None, border_fill_color=None)

# Add map tile. https://docs.bokeh.org/en/dev-3.0/docs/user_guide/geo.html
plot.add_tile("CartoDB Positron", retina=True)

# Add points using mercator coordinates
leg_1 = []

for counter,pop in enumerate(labels):
	#labels.append(pop)
	leg_1.append((pop, [plot.scatter(x= 'mercator_x', y= 'mercator_y', source=source.loc[source['Population'] == pop], color= 'Colour', marker= 'Shape', fill_color= 'Filling', 
	fill_alpha= 1, size= 30, muted_alpha= 0, line_width= 2) ] ))

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= args.add_info, text_font_size='16pt')
plot.add_layout(text, 'below')

plot.title.text_font_size = '25pt'
#plot.xaxis.axis_label="Latitude"
plot.xaxis.axis_label_text_font_size= "20pt"
plot.xaxis.major_label_text_font_size= "15pt"
plot.xaxis.axis_label_text_font= "arial"
plot.xaxis.axis_label_text_color= "black"
plot.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_tick_line_width= 5

#plot.yaxis.axis_label="Longitud"
plot.yaxis.axis_label_text_font_size= "20pt"
plot.yaxis.major_label_text_font_size= "15pt"
plot.yaxis.axis_label_text_font= "arial"
plot.yaxis.axis_label_text_color= "black"
plot.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_tick_line_width= 5

#Grid lines
plot.xgrid.visible= False
plot.ygrid.visible= False

plot.outline_line_color= 'black'
outline_line_alpha= 1
plot.outline_line_width= 2

# Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful
plot.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [("Group","@Group"), ("Population","@Population"), ("N_samples","@N_samples")]
	 ))

if args.legend=='Two':
	ncolumn=int((len(labels))/2)
	# print "populations=",len(fids),"pop/column",ncolumn
	legend1 = Legend(
		items=leg_1[0:ncolumn], location=(0, 30))
	
	legend2 = Legend(
		items=leg_1[ncolumn:], location=(0, 30))
	
	plot.add_layout(legend1, 'right')
	plot.add_layout(legend2, 'right')
	plot.legend.location = "top_right"
	plot.legend.click_policy="hide" # "mute"
	plot.legend.glyph_width= 18
	plot.legend.glyph_height= 18
	
	plot.legend.label_text_font_style = "normal"
	plot.legend.label_text_font_size = '10pt'
	plot.legend.label_width= 28
	plot.legend.label_height= 8

if args.legend=='True':
	ncolumn=int((len(labels))/5)
	# print "populations=",len(fids),"pop/column",ncolumn
	legend1 = Legend(
		items=leg_1[0:ncolumn], location=(0, 30))
	
	legend2 = Legend(
		items=leg_1[ncolumn:ncolumn*2], location=(0, 30))
	
	legend3 = Legend(
		items=leg_1[ncolumn*2:ncolumn*3], location=(0, 30))
	
	legend4 = Legend(
		items=leg_1[ncolumn*3:ncolumn*4], location=(0, 30))
	
	legend5 = Legend(
	    items=leg_1[ncolumn*4:], location=(0, 30))
	
	plot.add_layout(legend1, 'right')
	plot.add_layout(legend2, 'right')
	plot.add_layout(legend3, 'right')
	plot.add_layout(legend4, 'right')
	plot.add_layout(legend5, 'right')
	
	plot.legend.location = "top_right"
	plot.legend.click_policy="hide" # "mute"
	# plot.legend.glyph_width= 18
	# plot.legend.glyph_height= 18
	
	plot.legend.label_text_font_style = "normal"
	plot.legend.label_text_font_size = '12pt'
	plot.legend.label_width= 28
	plot.legend.label_height= 8

# Save map
# output_file('{}.html'.format(out))
export_png(plot, filename=out+".png")
plot.output_backend= "svg"
export_svgs(plot, filename=out+".svg")
show(plot)
exit()
