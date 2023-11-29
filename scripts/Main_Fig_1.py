"""
Script to plot interactive plots for all the figures included in panel Fig. 1
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
from bokeh.models import TabPanel, Tabs, Label, GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.models import Legend, HoverTool, LegendItem, WheelZoomTool, ColumnDataSource

# Usage:
# python3 0-Main_Figures/scripts/Main_Fig_1.py

output= '0-Main_Figures/Fig_'
legend= 'True'

# Fig 1a 
a_figure= '1a'
a_input= '01-Maps/Map_Only-African_Groups_df.csv'
a_title= 'Fig. 1a | Population structure within sub-Saharan African populations'
a_add_info= 'Geographical locations of the 111 sub-Saharan African populations selected for population genetic analysis within the AfricanNeo dataset.'
a_width= '2500'

df= pd.read_csv(a_input, index_col= 0)
df.head()
source = df
source.set_index('Population')
fids = source.Population.unique()
labels = fids
width= a_width

# Define function to switch from lat/long to mercator coordinates
def x_coord(x, y):
	lat= x
	lon= y 
	r_major= 6378137.000
	x= r_major * np.radians(lon)
	scale= x/lon
	y= 180.0/np.pi*np.log(np.tan(np.pi/4.0 + lat*(np.pi/180.0)/2.0))*scale
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
output_file(output+'1.html', mode='inline')
plot= figure(title= a_title, toolbar_location="above", x_axis_type= "mercator", x_axis_label= 'Longitude', y_axis_type= "mercator", y_axis_label= 'Latitude', height = 1000, width = int(width), 
	tooltips= tooltips, tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color=None, border_fill_color=None)

# Add map tile. https://docs.bokeh.org/en/dev-3.0/docs/user_guide/geo.html
plot.add_tile("CartoDB Positron", retina=True)

# Add points using Mercator coordinates
leg_1 = []

for counter,pop in enumerate(labels):
	#labels.append(pop)
	leg_1.append((pop, [plot.scatter(x= 'mercator_x', y= 'mercator_y', source=source.loc[source['Population'] == pop], color= 'Colour', marker= 'Shape', fill_color= 'Filling', 
	fill_alpha= 1, size= 30, muted_alpha= 0, line_width= 2) ] ))

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text='.', text_font_size='16pt', text_color="white")
plot.add_layout(text, 'below')

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= a_add_info, text_font_size='16pt')
plot.add_layout(text, 'below')

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption1= Label(text=' Figure presented in Fortes-Lima et al. 2023 (Copyright 2023)', **label_opts)
plot.add_layout(caption1, "above")

plot.title.text_font_size = '20pt'
#plot.xaxis.axis_label="Latitude"
plot.xaxis.axis_label_text_font_size= "18pt"
plot.xaxis.major_label_text_font_size= "15pt"
plot.xaxis.axis_label_text_font= "arial"
plot.xaxis.axis_label_text_color= "black"
plot.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_tick_line_width= 5

#plot.yaxis.axis_label="Longitud"
plot.yaxis.axis_label_text_font_size= "18pt"
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

if legend=='True':
	ncolumn=int((len(labels))/4+1)
	# print "populations=",len(fids),"pop/column",ncolumn
	legend1 = Legend(
		items=leg_1[0:ncolumn], location=(0, 30))
	
	legend2 = Legend(
		items=leg_1[ncolumn:ncolumn*2], location=(0, 30))
	
	legend3 = Legend(
		items=leg_1[ncolumn*2:ncolumn*3], location=(0, 30))
	
	legend4 = Legend(
		items=leg_1[ncolumn*3:], location=(0, 30))
	
	#legend5 = Legend(
	#    items=leg_1[ncolumn*4:], location=(0, 30))
	
	plot.add_layout(legend1, 'right')
	plot.add_layout(legend2, 'right')
	plot.add_layout(legend3, 'right')
	plot.add_layout(legend4, 'right')
	#plot.add_layout(legend5, 'right')
	
	plot.legend.location = "top_right"
	plot.legend.click_policy="hide" # "mute"
	# plot.legend.glyph_width= 18
	# plot.legend.glyph_height= 18
	
	plot.legend.label_text_font_style = "normal"
	plot.legend.label_text_font_size = '12pt'
	plot.legend.label_width= 28
	plot.legend.label_height= 8

# Save Map
plot.output_backend= "svg"
export_svgs(plot, filename=output+a_figure+".svg")
a_tab = TabPanel(child=plot, title="See Figure "+a_figure)
print("\n"+"Figure "+a_figure+" completed")


######################################################

# Fig 1b
b_figure= '1b'
b_input= '02-DRM/UMAP_AfricanNeo_Selection_DB_table.txt'
b_pattern= 'Patterns/AfricanNeo_Groups_umap_df.csv'
b_title= 'Fig. 1b | UMAP analysis of selected populations'
b_add_info= 'Uniform manifold approximation and projection (UMAP) analysis of selected populations.'
b_which_dim= '2,1'
b_plot_width= '2550'

evec= open(b_input)
which_dim= list(map(int, b_which_dim.split(',')))
eigs= {}
evec.readline()
evec_all= pd.read_csv(evec, header=None, sep='\s+')

pcs= ['ID']
pcs.extend(['UMAP' + str(x) for x in range(1, evec_all.shape[1]-1)])
pcs.append('UMAP')
evec_all.columns= pcs
iid_fid= pd.DataFrame(evec_all['ID'].str.split(':').tolist())
df= pd.concat([iid_fid, evec_all], axis=1)
df.rename(columns={0: 'FID', 1: 'IID'}, inplace=True)
source= df
#source= pd.concat([evec_all[['FID','IID']], iid_fid], axis=1)
source.set_index('FID')
source = source.rename(columns={0: "FID", 1: "IID"})
fids= source.FID.unique()

# Set your own pattern
title=b_title

pattern= csv.reader(open(b_pattern, 'r'), delimiter=",")
labels, colours, markers, filling= [], [], [], []

for row in pattern:
	labels.append(row[1])
	colours.append(row[2])
	markers.append(row[3])
	filling.append(row[4])
	filling= [d if d!='None' else None for d in filling]

# Plot
print ('UMAP' + str(p) + ' ' for p in which_dim)
plot= figure(title=title, toolbar_location="above", x_axis_label="PC"+str(which_dim[0]), y_axis_label="PC"+str(which_dim[1]), width= int(b_plot_width), height= 1000, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color= None, border_fill_color= None)

leg_1= []

sizes= [10]
while len(sizes) < len(fids):
	sizes.extend(sizes)
	sizes=sizes[0:len(fids)]

for counter,pop in enumerate(labels):
	leg_1.append(( pop, [plot.scatter(x='UMAP'+str(which_dim[0]), y='UMAP'+str(which_dim[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text='.', text_font_size='16pt', text_color="white")
plot.add_layout(text, 'below')

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= b_add_info, text_font_size='16pt')
plot.add_layout(text, 'below')

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption1= Label(text=' Figure presented in Fortes-Lima et al. 2023 (Copyright 2023)', **label_opts)
plot.add_layout(caption1, "above")

plot.title.text_font_size= '20pt'
plot.xaxis.axis_label="UMAP"+str(which_dim[0])
plot.xaxis.axis_label_text_font_size= "18pt"
plot.xaxis.major_label_text_font_size= "15pt"
plot.xaxis.axis_label_text_font= "arial"
plot.xaxis.axis_label_text_color= "black"
plot.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_tick_line_width= 5

plot.yaxis.axis_label="UMAP"+str(which_dim[1])
plot.yaxis.axis_label_text_font_size= "18pt"
plot.yaxis.major_label_text_font_size= "15pt"
plot.yaxis.axis_label_text_font= "arial"
plot.yaxis.axis_label_text_color= "black"
plot.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_tick_line_width= 5

plot.x_range.flipped= True
plot.y_range.flipped= True

#Grid lines
plot.xgrid.visible= False
plot.ygrid.visible= False

plot.outline_line_color= 'black'
outline_line_alpha= 1
plot.outline_line_width= 2

ncolumn=int((len(labels)+1)/4)
legend1 = Legend(
    items=leg_1[0:ncolumn], location=(0, 30))

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
plot.legend.click_policy="hide"
plot.legend.label_text_font_size = '12pt'
plot.legend.label_text_font_style = "bold"

plot.add_tools(WheelZoomTool(), HoverTool(
 tooltips= [
	 ('Population:', '@FID'),
	 ('ID:', '@IID'),
		 ]
	 ))

# Save UMAP plot
plot.output_backend= "svg"
export_svgs(plot, filename=output+b_figure+".svg")
b_tab = TabPanel(child=plot, title="See Figure "+b_figure)
print("\n"+"Figure "+b_figure+" completed")


######################################################

# Fig 1c
c_figure= '1c'
c_input= '02-DRM/Procrustes_OnlyAfrican_DB_minN10_Jan2022.pca.evec'
c_pattern= 'Patterns/Only-African_Groups_df.csv'
c_title= 'Fig. 1c | Procrustes rotated principal component analysis (PCA)'
c_add_info= 'Procrustes rotated PCA of sub-Saharan African populations (Procrustes correlation to geography > 0.576, P-value < 0.001).'
c_which_pcs= '1,2'
c_plot_width= '2550'


evec = open(c_input)
which_pcs = list(map(int, c_which_pcs.split(',')))

eigs = {}
evec.readline()
evec_all = pd.read_csv(evec, header=None, sep='\s+')
pcs = ['ID']
pcs.extend(['PC' + str(x) for x in range(1, evec_all.shape[1]-1)])
pcs.append('PC')
evec_all.columns = pcs
iid_fid = pd.DataFrame(evec_all['ID'].str.split(':').tolist())
df = pd.concat([iid_fid, evec_all], axis=1)
df.rename(columns={0: 'FID', 1: 'IID'}, inplace=True)
source = df
#source = pd.concat([evec_all[['FID','IID']], iid_fid], axis=1)
source.set_index('FID')
source  = source.rename(columns={0: "FID", 1: "IID"})
fids = source.FID.unique()

# Set your own pattern
title=c_title

pattern = csv.reader(open(c_pattern, 'r'), delimiter=",")
labels, colours, markers, filling = [], [], [], []

for row in pattern:
	labels.append(row[1])
	colours.append(row[2])
	markers.append(row[3])
	filling.append(row[4])
	filling = [d if d!='None' else None for d in filling]


# Plot
# print ['PC' + str(p) + ' ' for p in which_pcs]
plot = figure(title=title, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width= int(c_plot_width), height= 1000, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color=None, border_fill_color=None) #, background_fill_color="#fafafa")

leg_1 = []
sizes= [10]
while len(sizes) < len(fids):
	sizes.extend(sizes)
	sizes=sizes[0:len(fids)]

# sizes= [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15]

for counter,pop in enumerate(labels):
	leg_1.append(( pop, [plot.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text='.', text_font_size='16pt', text_color="white")
plot.add_layout(text, 'below')

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= c_add_info, text_font_size='16pt')
plot.add_layout(text, 'below')

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption1= Label(text=' Figure presented in Fortes-Lima et al. 2023 (Copyright 2023)', **label_opts)
plot.add_layout(caption1, "above")

plot.title.text_font_size = '20pt'
plot.xaxis.axis_label= "Dimension "+str(which_pcs[0])
plot.xaxis.axis_label_text_font_size = "18pt"
plot.xaxis.major_label_text_font_size = "15pt"
plot.xaxis.axis_label_text_font= "arial"
plot.xaxis.axis_label_text_color= "black"
plot.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_tick_line_width= 5

plot.yaxis.axis_label= "Dimension "+str(which_pcs[1])
plot.yaxis.axis_label_text_font_size = "18pt"
plot.yaxis.major_label_text_font_size = "15pt"
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
plot.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [
	 ('', '@FID'),
	 ('ID:', '@IID'),
		 ]
	 ))

ncolumn=int((len(labels)+1)/4)
legend1 = Legend(
    items=leg_1[0:ncolumn], location=(0, 30))

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
plot.legend.click_policy="hide"
plot.legend.label_text_font_size = '12pt'
plot.legend.label_text_font_style = "bold"


# Save PCA plot
plot.output_backend= "svg"
export_svgs(plot, filename=output+c_figure+".svg")
c_tab = TabPanel(child=plot, title="See Figure "+c_figure)
print("\n"+"Figure "+c_figure+" completed")


######################################################

# Fig 1d
d_figure= '1d'
d_input= '12-aDNA/PCA_aDNA_OnlyAfrican_DB/Procrustes/aDNA_OnlyAfrican_DB.pca.evec'
d_pattern= '12-aDNA/PCA_aDNA_OnlyAfrican_DB/Procrustes/aDNA_OnlyAfrican_DB_gray_pattern.csv'
d_title= 'Fig. 1d | Procrustes rotated PCA for projected ancient DNA individuals'
d_add_info= 'Procrustes rotated PCA for projected aDNA individuals and present-day sub-Saharan African populations.'
d_which_pcs= '1,2'
d_plot_width= '2550'

evec = open(d_input)
which_pcs = list(map(int, d_which_pcs.split(',')))

eigs = {}
evec.readline()
eved_all = pd.read_csv(evec, header=None, sep='\s+')
pcs = ['ID']
pcs.extend(['PC' + str(x) for x in range(1, eved_all.shape[1]-1)])
pcs.append('PC')
eved_all.columns = pcs
iid_fid = pd.DataFrame(eved_all['ID'].str.split(':').tolist())
df = pd.concat([iid_fid, eved_all], axis=1)
df.rename(columns={0: 'FID', 1: 'IID'}, inplace=True)
source = df
#source = pd.concat([eved_all[['FID','IID']], iid_fid], axis=1)
source.set_index('FID')
source  = source.rename(columns={0: "FID", 1: "IID"})
fids = source.FID.unique()

# Set your own pattern
title=d_title

pattern = csv.reader(open(d_pattern, 'r'), delimiter=",")
labels, colours, markers, filling = [], [], [], []

for row in pattern:
	labels.append(row[1])
	colours.append(row[2])
	markers.append(row[3])
	filling.append(row[4])
	filling = [d if d!='None' else None for d in filling]


# Plot
# print ['PC' + str(p) + ' ' for p in which_pcs]
plot = figure(title=title, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width= int(d_plot_width), height= 1000, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color=None, border_fill_color=None) #, background_fill_color="#fafafa")

leg_1 = []

sizes= [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15]

for counter,pop in enumerate(labels):
	leg_1.append(( pop, [plot.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text='.', text_font_size='16pt', text_color="white")
plot.add_layout(text, 'below')
text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= d_add_info, text_font_size='16pt')
plot.add_layout(text, 'below')

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption1= Label(text=' Figure presented in Fortes-Lima et al. 2023 (Copyright 2023)', **label_opts)
plot.add_layout(caption1, "above")

plot.title.text_font_size = '20pt'
plot.xaxis.axis_label= "Dimension "+str(which_pcs[0])
plot.xaxis.axis_label_text_font_size = "18pt"
plot.xaxis.major_label_text_font_size = "15pt"
plot.xaxis.axis_label_text_font= "arial"
plot.xaxis.axis_label_text_color= "black"
plot.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_tick_line_width= 5

plot.yaxis.axis_label= "Dimension "+str(which_pcs[1])
plot.yaxis.axis_label_text_font_size = "18pt"
plot.yaxis.major_label_text_font_size = "15pt"
plot.yaxis.axis_label_text_font= "arial"
plot.yaxis.axis_label_text_color= "black"
plot.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_tick_line_width= 5

#Grid lines
plot.xgrid.visible = False
plot.ygrid.visible = False

# Reverse Axes
# plot.x_range.flipped = True
# plot.y_range.flipped = True

plot.outline_line_color= 'black'
outline_line_alpha= 1
plot.outline_line_width= 2
plot.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [
	 ('', '@FID'),
	 ('ID:', '@IID'),
		 ]
	 ))

ncolumn=int((len(labels)+1)/4)
legend1 = Legend(
    items=leg_1[0:ncolumn], location=(0, 30))

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
plot.legend.click_policy="hide"
plot.legend.label_text_font_size = '12pt'
plot.legend.label_text_font_style = "bold"


# Save PCA plot
plot.output_backend= "svg"
export_svgs(plot, filename=output+d_figure+".svg")
d_tab = TabPanel(child=plot, title="See Figure "+d_figure)
print("\n"+"Figure "+d_figure+" completed")

show(Tabs(tabs=[a_tab, b_tab, c_tab, d_tab]))
exit()


