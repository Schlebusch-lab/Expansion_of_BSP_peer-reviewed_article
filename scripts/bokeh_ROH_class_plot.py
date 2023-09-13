"""
Plots the output of ROH
"""
__author__ = 'Cesar Fortes-Lima'

import matplotlib.pyplot as plt
import argparse
import pandas as pd
import numpy as np
import warnings
import sys, random, csv
warnings.filterwarnings('ignore')

from io import StringIO
from tabulate import tabulate

# Bokeh imports
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Label, Legend, HoverTool, LegendItem, WheelZoomTool, ColumnDataSource
from bokeh.transform import linear_cmap
from bokeh.palettes import inferno, Spectral6

reload(sys)
sys.setdefaultencoding('utf8')

parser = argparse.ArgumentParser(description='Parse some args')
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output', help='uses png or pdf suffix to determine type of file to plot')
parser.add_argument('-p', '--pattern', default=None)
parser.add_argument('-t', '--title', default='', action='store', help='Title of the plot')
parser.add_argument('-w', '--width', default='', action='store', help='')
parser.add_argument('-a', '--add_info', default='', action='store', help='Additiona information for the plot')
parser.add_argument('-f', '--add_figure', default='', action='store')

args = parser.parse_args()

# Usage: 
# python2 ROH_class_bokeh_plot.py -i [INPUT].txt -o [OUTPUT_bokeh_plot] --title "" 
#

ROH_data = open(args.input)
out = args.output

ROH_data.readline()
ROH_data_all = pd.read_csv(ROH_data, header=None, sep='\s+')
source = ROH_data_all
source  = source.rename(columns={0: "Population", 1: "Class", 2: "Mean"})
Populations = source.Population.unique()

# Set your own pattern
title=args.title
#title=''

width=args.width
# Plot
output_file(args.output+'.html', mode='inline')
plot = figure(title=title, toolbar_location="above", x_axis_label="ROH length category",y_axis_label="Mean total length of ROH (Mb)",plot_width = int(width), plot_height = 1000, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom')
#, background_fill_color="#fafafa"

leg_0 = []
leg_1 = []

# 
#print "labels (N=",len(Populations),") = \n",labels
#print "colours = ",colours
#print "markers = ",markers
#print "filling = ",filling

pattern = csv.reader(open(args.pattern, 'rb'), delimiter=",")
labels, colours, markers, filling = [], [], [], []

for row in pattern:
	labels.append(row[1])
	colours.append(row[2])
	markers.append(row[3])
	filling.append(row[4])
	filling = [d if d!='None' else None for d in filling]


for counter,pop in enumerate(labels):
	leg_0.append(( pop, [plot.line(x='Class', y='Mean', source=source.loc[source['Population'] == pop], color=colours[counter], muted_alpha=0.2 ) ] ))
	leg_1.append(( pop, [plot.scatter(x='Class', y='Mean', source=source.loc[source['Population'] == pop],
		marker=markers[counter], size=12, color=colours[counter], muted_alpha=0.6, fill_color=filling[counter] ) ] ))
f = open('pattern.txt', 'w')
pattern = pd.DataFrame({'1_Labels':labels,'2_Colours':colours,'3_Markers':markers,'4_Filling':filling})
f.write(tabulate(pattern, headers='keys', tablefmt='psql'))
f.close()

text= args.add_info
text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= text, text_font_size='16pt')
plot.add_layout(text, 'below')

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption1= Label(text=' Supplementary Fig. '+args.add_figure+' presented in Fortes-Lima et al. 2023 (Copyright 2023)', **label_opts)
plot.add_layout(caption1, "above")


plot.title.text_font_size = '20pt'
plot.xaxis.axis_label="ROH length category"
# plot.xaxis.ticker = ['class1', 'class2', 'class3', 'class4', 'class5', 'class6'] # First edit input file
plot.xaxis.axis_label_text_font_size = "20pt"
plot.xaxis.major_label_text_font_size = "15pt"
plot.xaxis.axis_label_text_font= "arial"
plot.xaxis.axis_label_text_color= "black"
plot.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_tick_line_width= 5

plot.yaxis.axis_label="Mean total length of ROH (Mb)"
plot.yaxis.axis_label_text_font_size = "20pt"
plot.yaxis.major_label_text_font_size = "18pt"
plot.yaxis.axis_label_text_font= "arial"
plot.yaxis.axis_label_text_color= "black"
plot.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_tick_line_width= 5


#Grid lines
plot.xgrid.visible = False
plot.xgrid.grid_line_alpha = 0.8
plot.xgrid.grid_line_dash = [6, 4]
plot.ygrid.visible = False
plot.ygrid.grid_line_alpha = 0.8
plot.ygrid.grid_line_dash = [6, 4]


ncolumn=(len(Populations)+21)/4
#print "populations=",len(Populations)
legend1 = Legend(
    items=leg_1[0:ncolumn], location=(0, 30),)

legend2 = Legend(
    items=leg_1[ncolumn:ncolumn*2], location=(0, 30))

legend3 = Legend(
    items=leg_1[ncolumn*2:ncolumn*3], location=(0, 30))

legend4 = Legend(
    items=leg_1[ncolumn*3:], location=(0, 30))

plot.add_layout(legend1, 'right')
plot.add_layout(legend2, 'right')
plot.add_layout(legend3, 'right')
plot.add_layout(legend4, 'right')
plot.legend.location = "top_right"
plot.legend.click_policy="hide"#"mute"
plot.legend.label_text_font_size = '10pt'

plot.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [
	 ('ID', '@Population'),
		 ]
	 ))

output_file('{}.html'.format(out))
print "Saving output to {}.html".format(out) 

show(plot)
exit()

#######################

