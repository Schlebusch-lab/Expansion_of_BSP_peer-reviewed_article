"""
Script to plot interactive plots for all the figures included in panel Fig. 3
"""
__author__= 'Cesar Fortes-Lima'

import matplotlib
matplotlib.rcParams['pdf.fonttype']= 42
matplotlib.rcParams['ps.fonttype']= 42
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import sys, random, csv
from io import StringIO
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')

# Bokeh imports
from bokeh.io.export import export_svgs, export_png
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, gridplot
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Label, Legend, HoverTool, LegendItem, WheelZoomTool, ColumnDataSource
from bokeh.transform import linear_cmap
from bokeh.palettes import inferno, Spectral6, Plasma

# Usage: 
# python3 0-Main_Figures/scripts/Main_Fig_3.py
#
#

input_Fig3="13-ASPCA_after_masking/Imputed_Bantu-sp_70WCA_DB_clean_March2022.pca.evec"
evec= open(input_Fig3)

output="0-Main_Figures/Fig_3"
out= output

if input_Fig3.endswith('evec')==True:
	my_eval= open(input_Fig3.replace('evec', 'eval'))
	eval_per= []
	for line in my_eval:
		eval_per.append(float(line.strip()))
	eval_per= [x/sum(eval_per)*100 for x in eval_per]

eigs= {}
evec.readline()
evec_all= pd.read_csv(evec, header=None, sep='\s+')
pcs= ['ID']
pcs.extend(['PC' + str(x) for x in range(1, evec_all.shape[1]-1)])
pcs.append('PC')
evec_all.columns= pcs
iid_fid= pd.DataFrame(evec_all['ID'].str.split(':').tolist())
df= pd.concat([iid_fid, evec_all], axis=1)
df.rename(columns={0: 'FID', 1: 'IID'}, inplace=True)
source= df
source.set_index('FID')
source = source.rename(columns={0: "FID", 1: "IID"})
fids= source.FID.unique()

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption1= Label(text=' Figure presented in Fortes-Lima et al. 2023 (Copyright 2023)', **label_opts)

###############################

# Fig. 3a

pattern_a="Patterns/Masked_Groups_df.csv"
title_a="Fig. 3a | PCA plot on the masked Only-BSP dataset"
add_info_a="PC1 vs PC2 and plot highlighting different groups included in the dataset"
which_pcs= "1,2"
which_pcs= list(map(int, which_pcs.split(',')))

pattern= csv.reader(open(pattern_a, 'r'), delimiter=",")
labels, colours, markers, filling= [], [], [], []
for row in pattern:
	labels.append(row[1])
	colours.append(row[2])
	markers.append(row[3])
	filling.append(row[4])
	filling= [d if d!='None' else None for d in filling]
# Plot
print ('Fig. 3a', ['PC' + str(p) + ' ' for p in which_pcs])
output_file(output+'.html', mode='inline')
plot_a= figure(title= title_a, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width= 800, height= 700, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color=None, border_fill_color=None) #, background_fill_color="#fafafa")

leg_1= []
sizes= [10]
while len(sizes) < len(fids):
	sizes.extend(sizes)
	sizes=sizes[0:len(fids)]

for counter,pop in enumerate(labels):
	leg_1.append((pop, [plot_a.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= add_info_a, text_font_size='16pt')
plot_a.add_layout(text, 'below')

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= add_info_a, text_font_size='16pt', text_color="white")
plot_a.add_layout(text, 'below')
plot_a.add_layout(caption1, "above")

plot_a.title.text_font_size= '20pt'
# plot_a.xaxis.axis_label="PC1"
if input_Fig3.endswith('evec')==True:
	plot_a.xaxis.axis_label= "PC"+str(which_pcs[0])+' ('+"%.2f" % eval_per[which_pcs[0]-1]+'%)' # '% var explained)'

plot_a.xaxis.axis_label_text_font_size= "18pt"
plot_a.xaxis.major_label_text_font_size= "15pt"
plot_a.xaxis.axis_label_text_font= "arial"
plot_a.xaxis.axis_label_text_color= "black"
plot_a.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_a.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_a.xaxis.major_tick_line_width= 5
# plot_a.xaxis.axis_label="PC2"
if input_Fig3.endswith('evec')==True:
	plot_a.yaxis.axis_label= "PC"+str(which_pcs[1])+' ('+"%.2f" % eval_per[which_pcs[1]-1]+'%)'

plot_a.yaxis.axis_label_text_font_size= "18pt"
plot_a.yaxis.major_label_text_font_size= "15pt"
plot_a.yaxis.axis_label_text_font= "arial"
plot_a.yaxis.axis_label_text_color= "black"
plot_a.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_a.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_a.yaxis.major_tick_line_width= 5

#Grid lines
plot_a.xgrid.visible= False
plot_a.ygrid.visible= False

plot_a.outline_line_color= 'black'
outline_line_alpha= 1
plot_a.outline_line_width= 2

###############################

# Fig. 3b

pattern_b="Patterns/Masked_Populations_df.csv"
title_b="Fig. 3b | PCA plot on the masked Only-BSP dataset"
add_info_b="PC1 vs PC2 and plot highlighting different populations included in the dataset"
which_pcs= "1,2"
which_pcs= list(map(int, which_pcs.split(',')))

pattern= csv.reader(open(pattern_b, 'r'), delimiter=",")
labels, colours, markers, filling= [], [], [], []
for row in pattern:
	labels.append(row[1])
	colours.append(row[2])
	markers.append(row[3])
	filling.append(row[4])
	filling= [d if d!='None' else None for d in filling]
# Plot
print ('Fig. 3b', ['PC' + str(p) + ' ' for p in which_pcs])
output_file(output+'.html', mode='inline')
plot_b= figure(title= title_b, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width= 800, height= 700, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color=None, border_fill_color=None) #, background_fill_color="#fafafa")

leg_1= []
sizes= [10]
while len(sizes) < len(fids):
	sizes.extend(sizes)
	sizes=sizes[0:len(fids)]

for counter,pop in enumerate(labels):
	leg_1.append((pop, [plot_b.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= add_info_b, text_font_size='16pt')
plot_b.add_layout(text, 'below')
plot_b.add_layout(caption1, "above")

plot_b.title.text_font_size= '20pt'
# plot_b.xaxis.axis_label="PC1"
if input_Fig3.endswith('evec')==True:
	plot_b.xaxis.axis_label= "PC"+str(which_pcs[0])+' ('+"%.2f" % eval_per[which_pcs[0]-1]+'%)' # '% var explained)'

plot_b.xaxis.axis_label_text_font_size= "18pt"
plot_b.xaxis.major_label_text_font_size= "15pt"
plot_b.xaxis.axis_label_text_font= "arial"
plot_b.xaxis.axis_label_text_color= "black"
plot_b.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_b.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_b.xaxis.major_tick_line_width= 5

# plot_b.xaxis.axis_label="PC2"
if input_Fig3.endswith('evec')==True:
	plot_b.yaxis.axis_label= "PC"+str(which_pcs[1])+' ('+"%.2f" % eval_per[which_pcs[1]-1]+'%)'

plot_b.yaxis.axis_label_text_font_size= "18pt"
plot_b.yaxis.major_label_text_font_size= "15pt"
plot_b.yaxis.axis_label_text_font= "arial"
plot_b.yaxis.axis_label_text_color= "black"
plot_b.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_b.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_b.yaxis.major_tick_line_width= 5

#Grid lines
plot_b.xgrid.visible= False
plot_b.ygrid.visible= False

plot_b.outline_line_color= 'black'
outline_line_alpha= 1
plot_b.outline_line_width= 2

plot_b.add_tools(WheelZoomTool(), HoverTool(
 tooltips= [
	 ('Population', '@FID'),
	 ('Sample ID', '@IID'),
		 ]
	 ))

###############################

# Fig. 3c

pattern_c="Patterns/Masked_Groups_df.csv"
title_c="Fig. 3c | Procrustes rotated PCA on the masked dataset"
add_info_c="Dimension 1 vs Dimension 3 and plot highlighting different groups"
which_pcs= "1,3"
which_pcs= list(map(int, which_pcs.split(',')))

pattern= csv.reader(open(pattern_c, 'r'), delimiter=",")
labels, colours, markers, filling= [], [], [], []
for row in pattern:
	labels.append(row[1])
	colours.append(row[2])
	markers.append(row[3])
	filling.append(row[4])
	filling= [d if d!='None' else None for d in filling]
# Plot
print ('Fig. 3c', ['PC' + str(p) + ' ' for p in which_pcs])
output_file(output+'.html', mode='inline')
plot_c= figure(title= title_c, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width= 800, height= 700, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color=None, border_fill_color=None) #, background_fill_color="#fafafa")

leg_1= []
sizes= [10]
while len(sizes) < len(fids):
	sizes.extend(sizes)
	sizes=sizes[0:len(fids)]

for counter,pop in enumerate(labels):
	leg_1.append((pop, [plot_c.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= add_info_c, text_font_size='16pt')
plot_c.add_layout(text, 'below')
plot_c.add_layout(caption1, "above")

plot_c.title.text_font_size= '20pt'

plot_c.xaxis.axis_label="Dimension 1"
plot_c.xaxis.axis_label_text_font_size= "18pt"
plot_c.xaxis.major_label_text_font_size= "15pt"
plot_c.xaxis.axis_label_text_font= "arial"
plot_c.xaxis.axis_label_text_color= "black"
plot_c.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_c.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_c.xaxis.major_tick_line_width= 5

plot_c.yaxis.axis_label="Dimension 3"
plot_c.yaxis.axis_label_text_font_size= "18pt"
plot_c.yaxis.major_label_text_font_size= "15pt"
plot_c.yaxis.axis_label_text_font= "arial"
plot_c.yaxis.axis_label_text_color= "black"
plot_c.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_c.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_c.yaxis.major_tick_line_width= 5

# Reverse Axes
# plot_c.x_range.flipped= True
plot_c.y_range.flipped= True

#Grid lines
plot_c.xgrid.visible= False
plot_c.ygrid.visible= False

plot_c.outline_line_color= 'black'
outline_line_clpha= 1
plot_c.outline_line_width= 2

plot_c.add_tools(WheelZoomTool(), HoverTool(
 tooltips= [
	 ('Population', '@FID'),
	 ('Sample ID', '@IID'),
		 ]
	 ))

###############################

# Fig. 3d

pattern_d="Patterns/Masked_Populations_df.csv"
title_d="Fig. 3d | Procrustes rotated PCA on the masked dataset"
add_info_d="Dimension 1 vs Dimension 3 and plot highlighting different populations"
which_pcs= "1,3"
which_pcs= list(map(int, which_pcs.split(',')))

pattern= csv.reader(open(pattern_d, 'r'), delimiter=",")
labels, colours, markers, filling= [], [], [], []
for row in pattern:
	labels.append(row[1])
	colours.append(row[2])
	markers.append(row[3])
	filling.append(row[4])
	filling= [d if d!='None' else None for d in filling]
# Plot
print ('Fig. 3d', ['PC' + str(p) + ' ' for p in which_pcs])
output_file(output+'.html', mode='inline')
plot_d= figure(title= title_d, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width= 800, height= 700, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color=None, border_fill_color=None) #, background_fill_color="#fafafa")

leg_1= []
sizes= [10]
while len(sizes) < len(fids):
	sizes.extend(sizes)
	sizes=sizes[0:len(fids)]

for counter,pop in enumerate(labels):
	leg_1.append((pop, [plot_d.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= add_info_d, text_font_size='16pt')
plot_d.add_layout(text, 'below')
plot_d.add_layout(caption1, "above")

plot_d.title.text_font_size= '20pt'

plot_d.xaxis.axis_label="Dimension 1"
plot_d.xaxis.axis_label_text_font_size= "18pt"
plot_d.xaxis.major_label_text_font_size= "15pt"
plot_d.xaxis.axis_label_text_font= "arial"
plot_d.xaxis.axis_label_text_color= "black"
plot_d.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_d.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_d.xaxis.major_tick_line_width= 5

plot_d.yaxis.axis_label="Dimension 3"
plot_d.yaxis.axis_label_text_font_size= "18pt"
plot_d.yaxis.major_label_text_font_size= "15pt"
plot_d.yaxis.axis_label_text_font= "arial"
plot_d.yaxis.axis_label_text_color= "black"
plot_d.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_d.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_d.yaxis.major_tick_line_width= 5

# Reverse Axes
# plot_d.x_range.flipped= True
plot_d.y_range.flipped= True

#Grid lines
plot_d.xgrid.visible= False
plot_d.ygrid.visible= False

plot_d.outline_line_color= 'black'
outline_line_alpha= 1
plot_d.outline_line_width= 2

plot_d.add_tools(WheelZoomTool(), HoverTool(
 tooltips= [
	 ('Population', '@FID'),
	 ('Sample ID', '@IID'),
		 ]
	 ))

#######################

# Map for each group

title="Geographic location for each group"
add_info=""
map_input="Patterns/Only-BSP_Groups_imputation_df.csv"
df= pd.read_csv(map_input, index_col= 0)
df.head()
source = df
source.set_index('Population')
fids = source.Population.unique()
labels = fids

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

# Define color mapper - which column will define the colour of the data points
# color_mapper= linear_cmap(field_name= 'Latitude', palette= palette, low= df['Latitude'].min(), high= df['Latitude'].max())
palette= df['Colour']

# Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful
tooltips= [("Group","@Group"), ("Population","@Population"), ("N samples","@N_samples")]

# Create figure
plot_map1= figure(title= title, toolbar_location="above", x_axis_type= "mercator", x_axis_label= 'Longitude', y_axis_type= "mercator", y_axis_label= 'Latitude', height = 700, width = 1000, 
	tooltips= tooltips, tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color=None, border_fill_color=None)

# Add map tile. https://docs.bokeh.org/en/dev-3.0/docs/user_guide/geo.html
plot_map1.add_tile("CartoDB Positron", retina=True)

# Add points using mercator coordinates
leg_1 = []

for counter,pop in enumerate(labels):
	#labels.append(pop)
	leg_1.append((pop, [plot_map1.scatter(x= 'mercator_x', y= 'mercator_y', source=source.loc[source['Population'] == pop], color= 'Colour', marker= 'Shape', fill_color= 'Filling', 
	fill_alpha= 1, size= 15, muted_alpha= 0, line_width= 2) ] ))

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= add_info, text_font_size='16pt')
plot_map1.add_layout(text, 'below')
plot_map1.add_layout(caption1, "above")

plot_map1.title.text_font_size = '20pt'
#plot_map1.xaxis.axis_label="Latitude"
plot_map1.xaxis.axis_label_text_font_size= "18pt"
plot_map1.xaxis.major_label_text_font_size= "15pt"
plot_map1.xaxis.axis_label_text_font= "arial"
plot_map1.xaxis.axis_label_text_color= "black"
plot_map1.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_map1.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_map1.xaxis.major_tick_line_width= 5

#plot_map1.yaxis.axis_label="Longitud"
plot_map1.yaxis.axis_label_text_font_size= "18pt"
plot_map1.yaxis.major_label_text_font_size= "15pt"
plot_map1.yaxis.axis_label_text_font= "arial"
plot_map1.yaxis.axis_label_text_color= "black"
plot_map1.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_map1.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_map1.yaxis.major_tick_line_width= 5

#Grid lines
plot_map1.xgrid.visible= False
plot_map1.ygrid.visible= False

plot_map1.outline_line_color= 'black'
outline_line_alpha= 1
plot_map1.outline_line_width= 2

ncolumn=int((len(labels))/2)
# print "populations=",len(fids),"pop/column",ncolumn
legend1= Legend(
    items=leg_1[0:ncolumn], location=(0, 30))

legend2= Legend(
    items=leg_1[ncolumn:], location=(0, 30))

plot_map1.add_layout(legend1, 'right')
plot_map1.add_layout(legend2, 'right')
plot_map1.legend.location= "top_right"
plot_map1.legend.click_policy="hide"
plot_map1.legend.label_text_font_size= '10pt'
plot_map1.legend.spacing= int(0.5)
plot_map1.legend.label_text_font_style= "normal"

# Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful
plot_map1.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [("Group","@Group"), ("Population","@Population"), ("N_samples","@N_samples")]
	 ))


#######################

# Map for each population

title="Geographic location for each population"
add_info=""
map_input="Patterns/Only-BSP_Populations_imputation_df.csv"
df= pd.read_csv(map_input, index_col= 0)
df.head()
source = df
source.set_index('Population')
fids = source.Population.unique()
labels = fids

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

# Define color mapper - which column will define the colour of the data points
# color_mapper= linear_cmap(field_name= 'Latitude', palette= palette, low= df['Latitude'].min(), high= df['Latitude'].max())
palette= df['Colour']

# Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful
tooltips= [("Group","@Group"), ("Population","@Population"), ("N samples","@N_samples")]

# Create figure
plot_map2= figure(title= title, toolbar_location="above", x_axis_type= "mercator", x_axis_label= 'Longitude', y_axis_type= "mercator", y_axis_label= 'Latitude', height = 700, width = 1000, 
	tooltips= tooltips, tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color=None, border_fill_color=None)

# Add map tile. https://docs.bokeh.org/en/dev-3.0/docs/user_guide/geo.html
plot_map2.add_tile("CartoDB Positron", retina=True)

# Add points using mercator coordinates
leg_1 = []

for counter,pop in enumerate(labels):
	leg_1.append((pop, [plot_map2.scatter(x= 'mercator_x', y= 'mercator_y', source=source.loc[source['Population'] == pop], color= 'Colour', marker= 'Shape', fill_color= 'Filling', 
	fill_alpha= 1, size= 15, muted_alpha= 0, line_width= 2) ] ))

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= add_info, text_font_size='16pt')
plot_map2.add_layout(text, 'below')
plot_map2.add_layout(caption1, "above")

plot_map2.title.text_font_size = '20pt'
#plot_map2.xaxis.axis_label="Latitude"
plot_map2.xaxis.axis_label_text_font_size= "18pt"
plot_map2.xaxis.major_label_text_font_size= "15pt"
plot_map2.xaxis.axis_label_text_font= "arial"
plot_map2.xaxis.axis_label_text_color= "black"
plot_map2.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_map2.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_map2.xaxis.major_tick_line_width= 5

#plot_map2.yaxis.axis_label="Longitud"
plot_map2.yaxis.axis_label_text_font_size= "18pt"
plot_map2.yaxis.major_label_text_font_size= "15pt"
plot_map2.yaxis.axis_label_text_font= "arial"
plot_map2.yaxis.axis_label_text_color= "black"
plot_map2.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_map2.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_map2.yaxis.major_tick_line_width= 5

#Grid lines
plot_map2.xgrid.visible= False
plot_map2.ygrid.visible= False

plot_map2.outline_line_color= 'black'
outline_line_alpha= 1
plot_map2.outline_line_width= 2

ncolumn=int((len(labels))/2)
# print "populations=",len(fids),"pop/column",ncolumn
legend1= Legend(
    items=leg_1[0:ncolumn], location=(0, 30))

legend2= Legend(
    items=leg_1[ncolumn:], location=(0, 30))

plot_map2.add_layout(legend1, 'right')
plot_map2.add_layout(legend2, 'right')
plot_map2.legend.location= "top_right"
plot_map2.legend.click_policy="hide"
plot_map2.legend.label_text_font_size= '10pt'
plot_map2.legend.spacing= int(0.5)
plot_map2.legend.label_text_font_style= "normal"

# Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful
plot_map2.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [("Group","@Group"), ("Population","@Population"), ("N_samples","@N_samples")]
	 ))

#######################

# Make a grid
grid= gridplot([[plot_a, plot_c, plot_map1], [plot_b, plot_d, plot_map2]]) #, width=250, height=250)

# Save plot
print ("Saving Fig. 3")
export_png(grid, filename=out+".png")
# plot.output_backend= "svg"
# export_svgs(plot, filename=out+".svg")
show(grid)
exit()
#######################

