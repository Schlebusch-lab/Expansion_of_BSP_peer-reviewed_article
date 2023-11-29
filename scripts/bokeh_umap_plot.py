"""
Script to plot the outputs of PCA-UMAP
"""
__author__= 'Cesar Fortes-Lima'

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
from bokeh.io.export import export_svgs, export_png
from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import column
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Label, Legend, HoverTool, LegendItem, WheelZoomTool, ColumnDataSource
from bokeh.transform import linear_cmap
from bokeh.palettes import inferno, Spectral6, Plasma
# from bokeh.models.widgets import Tabs, Panel

# reload(sys)
# sys.setdefaultencoding('utf8')

parser= argparse.ArgumentParser(description='Parse some args')
parser.add_argument('-i', '--input') #assumes eval in same place
parser.add_argument('-o', '--output', help='uses png or pdf suffix to determine type of file to plot')
parser.add_argument('-p', '--pattern', default=None)
parser.add_argument('--flip', default=None)
parser.add_argument('-d', '--which_dim', default='1,2', help='comma-separated list of dimensions')
parser.add_argument('-w', '--plot_width', default='2500', help='comma-separated list of dimensions')
parser.add_argument('-t', '--title', default='', action='store', help='Title of the plot')
parser.add_argument('-a', '--add_info', default='', action='store', help='Additiona information for the plot')
parser.add_argument('-f', '--add_figure', default=None, action='store')

args= parser.parse_args()

# Usage:
# python2 scripts/bokeh_umap_plot.py -i [INPUT]_genotype.txt -o [OUTPUT]_UMAP_plot -t [TITLE] -a [Additional Information] -p [Patterns].csv --which_dim 2,1; done
#

evec= open(args.input)
which_dim= list(map(int, args.which_dim.split(',')))
out= args.output
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

if args.pattern==None:
	labels= fids
	markers= ['x', 'asterisk', 'cross', 'hex', 'circle', 'circle_cross', 'circle_x', 'diamond', 'diamond_cross', 'square', 'square_x', 'square_cross', 'triangle', 'inverted_triangle']#, 'dash'
	while len(markers) < len(fids):
		markers.extend(markers)
		markers=markers[0:len(fids)]
	
	filling= ['white']
	while len(filling) < len(fids):
		filling.extend(filling)
		filling=filling[0:len(fids)]
	
	# To select colours
	colours= ['aqua', 'aquamarine', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick', 'forestgreen', 'fuchsia', 'gainsboro', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'hotpink', 'indianred', 'indigo', 'khaki', 'lavender', 'lawngreen', 'lemonchiffon', 'lime', 'limegreen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'moccasin', 'navy', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'yellow', 'yellowgreen']
	while len(colours) < len(fids):
		colours.extend(colours)
	colours= random.sample(colours, len(fids))

# Set your own pattern
title=args.title
#title=''

if args.pattern!=None:
	pattern= csv.reader(open(args.pattern, 'r'), delimiter=",")
	labels, colours, markers, filling= [], [], [], []
	
	for row in pattern:
		labels.append(row[1])
		colours.append(row[2])
		markers.append(row[3])
		filling.append(row[4])
		filling= [d if d!='None' else None for d in filling]

# Plot
print ('UMAP' + str(p) + ' ' for p in which_dim)
output_file(args.output+'.html', mode='inline')
plot= figure(title=title, toolbar_location="above", x_axis_label="PC"+str(which_dim[0]), y_axis_label="PC"+str(which_dim[1]), width= int(args.plot_width), height= 1000, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color= None, border_fill_color= None)

leg_1= []
sizes= [8]

while len(sizes) < len(fids):
	sizes.extend(sizes)
	sizes=sizes[0:len(fids)]

if args.pattern!=None:
	for counter,pop in enumerate(labels):
		#labels.append(pop)
		leg_1.append(( pop, [plot.scatter(x='UMAP'+str(which_dim[0]), y='UMAP'+str(which_dim[1]), source=source.loc[source['FID'] == pop],
			marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

if args.output=="":
	for counter,pop in enumerate(fids):
		#labels.append(pop)
		leg_1.append(( pop, [plot.scatter(x='UMAP'+str(which_dim[0]), y='UMAP'+str(which_dim[1]), source=source.loc[source['FID'] == pop],
			marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.4, fill_color=filling[counter] ) ] ))
	f= open('pattern.txt', 'w')
	pattern= pd.DataFrame({'1_Labels':labels,'2_Colours':colours,'3_Markers':markers,'4_Filling':filling})
	f.write(tabulate(pattern, headers='keys', tablefmt='psql'))
	f.close()

text= args.add_info
text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= text, text_font_size='16pt')
plot.add_layout(text, 'below')

plot.title.text_font_size= '20pt'
plot.xaxis.axis_label="UMAP"+str(which_dim[0])
plot.xaxis.axis_label_text_font_size= "20pt"
plot.xaxis.major_label_text_font_size= "15pt"
plot.xaxis.axis_label_text_font= "arial"
plot.xaxis.axis_label_text_color= "black"
plot.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_tick_line_width= 5

plot.yaxis.axis_label="UMAP"+str(which_dim[1])
plot.yaxis.axis_label_text_font_size= "20pt"
plot.yaxis.major_label_text_font_size= "18pt"
plot.yaxis.axis_label_text_font= "arial"
plot.yaxis.axis_label_text_color= "black"
plot.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_tick_line_width= 5

if args.flip!=None: # Reverse axes
	plot.x_range.flipped= True
	plot.y_range.flipped= True

#Grid lines
plot.xgrid.visible= False
plot.ygrid.visible= False

plot.outline_line_color= 'black'
outline_line_alpha= 1
plot.outline_line_width= 2

plot.add_tools(WheelZoomTool(), HoverTool(
 tooltips= [
	 ('', '@FID'),
	 ('ID:', '@IID'),
		 ]
	 ))

# print "Saving output to {}.html".format(out)
# output_file('{}.html'.format(out))

plot.output_backend= "svg"
export_svgs(plot, filename=out+".svg")

show(plot)
exit()

# Create two panels, one for each conference
UMAP1vs2_panel= Panel(child=plot, title="UMAP"+str(which_dim[0])+" vs "+"UMAP"+str(which_dim[1]))

# Assign the panels to Tabs
tabs= Tabs(tabs=[UMAP1vs2_panel])

# Show the tabbed layout
# show(plot)
# show(tabs)

#######################



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


