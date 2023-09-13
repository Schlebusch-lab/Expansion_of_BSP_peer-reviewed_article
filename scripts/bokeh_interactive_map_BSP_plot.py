"""
Interactive plots for maps
"""
__author__ = 'Cesar Fortes-Lima'

import numpy as np
import pandas as pd
import argparse, pdb
import sys, random, csv
from tabulate import tabulate
# pdb.set_trace()
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure, ColumnDataSource
from bokeh.tile_providers import get_provider, Vendors
from bokeh.palettes import Spectral, RdYlBu, RdYlGn
from bokeh.transform import linear_cmap,factor_cmap
from bokeh.layouts import row, column
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter

parser = argparse.ArgumentParser(description='Parse some args')
parser.add_argument('-i', '--input', default='', help='input file') #assumes eval in same place
parser.add_argument('-o', '--output', help='uses .png or .pdf suffix to determine type of file to plot')
parser.add_argument('--title', default='')
parser.add_argument('-f', '--add_figure', default='', action='store')

args = parser.parse_args()

# Usage:
# python2 bokeh_interactive_map_plot.py -i Suppl_Fig_Map2/Bantu_Full_df.csv -o Fig.S_1_Maps/Suppl_Fig_Map2 # Full_AfricanNeo_bokeh_interactive_map
# 
# python2 bokeh_interactive_map_plot.py -i Suppl_Fig_Map3/Bantu_Groups_df.csv -o Fig.S_1_Maps/Suppl_Fig_Map3 # Groups_AfricanNeo_bokeh_interactive_map
# 
# python2 bokeh_interactive_map_plot.py -i Suppl_Fig_Map4/Bantu_Labels_df.csv -o Fig.S_1_Maps/Suppl_Fig_Map4 # Labels_AfricanNeo_bokeh_interactive_map
# 

df= pd.read_csv(args.input, index_col= 0)
df.head()
out = args.output

# Select type of map to use (see: https://docs.bokeh.org/en/2.4.0/docs/reference/tile_providers.html)
#chosentile= get_provider(Vendors.OSM)
chosentile= get_provider(Vendors.CARTODBPOSITRON_RETINA)

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
source= ColumnDataSource(data= df)

# Choose palette
palette= Spectral[11]

# Define color mapper - which column will define the colour of the data points
#color_mapper= linear_cmap(field_name= 'Latitude', palette= palette, low= df['Latitude'].min(), high= df['Latitude'].max())
palette= df['Colour']

# Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful
tooltips= [("Group","@Group"), ("Population","@Population"), ("N_samples","@N_samples")]

# Create figure
output_file(args.output+'.html', mode='inline')
plot= figure(title= args.title, toolbar_location="above", x_axis_type= "mercator", x_axis_label= 'Longitude', y_axis_type= "mercator", y_axis_label= 'Latitude', 
	tooltips= tooltips, plot_height = 1000, plot_width = 800, # plot_width = 800, for Only-BSP
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom')

# Add map tile
plot.add_tile(chosentile)

# Add points using mercator coordinates
# p.circle(x= 'mercator_x', y= 'mercator_y', color= color_mapper, source= source, size= 30, fill_alpha= 0.7)
plot.scatter(x= 'mercator_x', y= 'mercator_y', source= source, color= 'Colour', marker= 'Shape', fill_color= 'Filling', 
	fill_alpha= 1, size= 30, muted_alpha= 0, line_width= 4)

#Defines color bar
#color_bar= ColorBar(color_mapper= color_mapper['transform'],
#	formatter= NumeralTickFormatter(format= '0.0[0000]'), label_standoff= 13, width= 8, location= (0,0))

# Set color_bar location
#plot.add_layout(color_bar, 'right')

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption1= Label(text=' Supplementary Fig. '+args.add_figure+' presented in Fortes-Lima et al. 2023 (Copyright 2023)', **label_opts)
plot.add_layout(caption1, "above")

plot.title.text_font_size = '25pt'
#plot.xaxis.axis_label="Latitude"
plot.xaxis.axis_label_text_font_size = "20pt"
plot.xaxis.major_label_text_font_size = "15pt"
plot.xaxis.axis_label_text_font= "arial"
plot.xaxis.axis_label_text_color= "black"
plot.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_tick_line_width= 5

#plot.yaxis.axis_label="Longitud"
plot.yaxis.axis_label_text_font_size = "20pt"
plot.yaxis.major_label_text_font_size = "18pt"
plot.yaxis.axis_label_text_font= "arial"
plot.yaxis.axis_label_text_color= "black"
plot.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_tick_line_width= 5

#Grid lines
plot.xgrid.visible = False
plot.ygrid.visible = False

plot.outline_line_color= 'black'
outline_line_alpha= 1
plot.outline_line_width= 2

# Show map
output_file('{}.html'.format(out)) 
show(plot)











