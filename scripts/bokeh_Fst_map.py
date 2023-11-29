"""
Script to plot the maps with genetic distances (Fst)
"""
__author__ = 'Cesar Fortes-Lima'

# Usage
# Fig. 5a
# DB=Selection_file_with_Lozi; python3 scripts/bokeh_Fst_map.py -i ${dir}/${DB}.csv -o 0-Main_Figures/Fig_5a -l ${dir}/locations.csv -p dots
# Fig. 5b
# DB=Selection_file_without_Lozi; python3 scripts/bokeh_Fst_map.py -i ${dir}/${DB}.csv -o 0-Main_Figures/Fig_5b -l ${dir}/locations.csv -p dots
#
# Supplementary Fig. 83b | Fst map for BSP included in the AfricanNeo dataset except for the Lozi population
# DB=Selection_file_with_Lozi; python3 scripts/bokeh_Fst_map.py -i ${dir}/${DB}.csv -l ${dir}/locations.csv -p labels -o ${Folder}/Suppl_Fig_83a -f 83a
# Supplementary Fig. 83a | Fst map for all the BSP included in the AfricanNeo datase
# DB=Selection_file_without_Lozi; python3 scripts/bokeh_Fst_map.py -i ${dir}/${DB}.csv -l ${dir}/locations.csv -p labels -o ${Folder}/Suppl_Fig_83b -f 83b
#

__author__ = 'Cesar Fortes-Lima'
import argparse
import numpy as np
import pandas as pd
import plotly.graph_objects as go

parser = argparse.ArgumentParser(description='Parse some args')
parser.add_argument('-i', '--input') # assumes file is in same place
parser.add_argument('-o', '--output', help='Plot name')
parser.add_argument('-l', '--locations', help='Locations file in *.csv format')
parser.add_argument('-p', '--pattern', default=None)
parser.add_argument('-f', '--add_figure', default='', action='store')

args = parser.parse_args()

locations= pd.read_csv(args.locations, header=None)
arrows= pd.read_csv(args.input, header=None)

df= pd.DataFrame(arrows)
scale= 5000
fig= go.Figure()
fig.add_trace(go.Scattergeo(locationmode= 'country names'))

arrow= []
for arrow in df.itertuples(index= False):
	latitud= (arrow[0], arrow[2])
	longitud= (arrow[1], arrow[3])
	B= np.array([arrow[1], arrow[0]])
	A= np.array([arrow[3], arrow[2]])
	
	if args.pattern=="dots":
		fig.add_trace(go.Scattergeo(locationmode= 'country names', 
			lat= locations[1], lon= locations[2], mode ="markers+text",
			marker= dict(size= 15, color= "silver", line_color= "black", line_width=0.4, sizemode= 'area')))
	
	if args.pattern=="labels":
		fig.add_trace(go.Scattergeo(locationmode= 'country names', 
			text= locations[0], textposition="middle right", textfont= {"color": 'black', "family":'sans-serif', "size":16},
			lat= locations[1], lon= locations[2], mode ="markers+text",
			marker= dict(size= 15, color= "silver", line_color= "black", line_width=0.4, sizemode= 'area')))
		
	fig.add_trace(go.Scattergeo(lat= latitud, lon= longitud, mode= 'lines', line= dict(width= 3.0, color= arrow[5])))
	
	l= 3  # the arrow length
	widh= 0.08  #2*widh is the width of the arrow base as triangle
	v= B-A
	w= v/np.linalg.norm(v)     
	u= np.array([-v[1], v[0]])  #u orthogonal on  w
	P= B-l*(w/2)
	S= P - widh*u
	T= P + widh*u
	
	fig.add_trace(go.Scattergeo(lon= [S[0], T[0], B[0], S[0]], lat= [S[1], T[1], B[1], S[1]], 
		mode= 'lines', fill= 'toself', fillcolor= arrow[4], line_color= arrow[5]))
	
	# fig.add_trace(go.Scattergeo(lon =[0.5*(A+B)[0]], lat= [0.5*(A+B)[1]], mode='text', text='Your text')) #------Display your text at the middle of the segment AB
	fig.update_layout(showlegend= False, geo= dict(scope= 'africa', lakecolor= "aqua", landcolor= 'floralwhite'))


fig.update_layout(height=800, title_text='Fst map for the masked Only-BSP dataset.   Supplementary Fig. '+args.add_figure+' presented in Fortes-Lima et al. 2023 (Copyright 2023)')
fig.write_image(args.output+"_"+args.pattern+"_Map.svg")

fig.show()
fig.write_html(args.output+"_"+args.pattern+"_Map.html")



