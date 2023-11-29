"""
Python script to the uniform manifold approximation and projection (UMAP) approach directly on genome-wide SNP data
"""
__author__ = 'Rickard Hammarén'

#!/usr/bin/env python
import argparse
import pandas as pd
import numpy as np

#pip install umap-learn
import umap.umap_ as umap
import warnings
import sys
warnings.filterwarnings('ignore')

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Legend, HoverTool, LegendItem
from bokeh.transform import linear_cmap
from bokeh.palettes import inferno

from pandas_plink import read_plink

def read_input(input_file):
    print("Reading data..")
    (bim, fam, G) = read_plink(input_file)
    return (bim, fam, G)

def do_UMAP(data):
    print("Performing dimensionality reduction")
    reducer = umap.UMAP()
    ## set missing data to 0 and transpose the data so the rows are individuals not SNPs
    embedding = reducer.fit_transform(np.nan_to_num(data.T))
    return embedding

def plotting(umaped_data, bim, fam, output, key_file):
    key=key_file
    
    print("Building plot")
    umaped_df =  pd.DataFrame(data=umaped_data)

    source = pd.concat([fam[['fid','iid']], umaped_df], axis=1) 
    source.set_index('fid')
    source  = source.rename(columns={0: "x", 1: "y"})
    source.to_csv('UMAP_on_BED_file_components.csv', index=False)
    p = figure(title="UMAP of genotypes", toolbar_location="above", x_axis_label="UMAP 1",y_axis_label="UMAP 2",plot_width = 1500, plot_height = 1000)
    
    fids = source.fid.unique()
    lenght_of_leg = len(fids)/2
    colours = inferno(len(fids))
    leg_1 = []
    leg_2 = [] 
    if key:
        key_info = {}
        try:
            with open(key, 'r') as f:
                for line in f:
                    key_info[line.split()[0]] =  " ".join(line.split()[1:]) 
        except  IOError:
            print("Could not open the file '{}'".format(key))
            sys.exit()

        regions = set(key_info.values())
        colours = inferno(len(regions))
        
        ki= (pd.Series(key_info)).to_frame()
        ki = ki.sort_values(0)
        ki_re = ki.reset_index()
        ki_re = ki_re.rename(columns={'index':'fid', 0:'Region'})
        source = pd.merge(source, ki_re, on = ['fid'])
        
        for counter,region in enumerate(regions):
            ## Legend takes "Text to print", figure object
            ##todo make a list/DF with pops for each region so that can be used below:
            leg_1.append(( region, [p.circle(x='x', y='y', source=source.loc[source['Region'] == region ], size=9, color=colours[counter], muted_alpha=0.2 ) ] ))
        legend1 = Legend(items=leg_1, location = (0, 400))
        p.add_layout(legend1, 'left')
        p.legend.label_text_font_size = '18pt'
       
    else:
        for counter,pop in enumerate(fids):
            ## Legend takes "Text to print", figure object.
            ## This is here being parsed through a list. Makes it easy to add additional legends later if I want to
             if counter < lenght_of_leg:
                leg_1.append(( pop, [p.circle(x='x', y='y', source=source.loc[source['fid'] == pop], size=6, color=colours[counter], muted_alpha=0.2 ) ] ))
   
             else:
                leg_2.append(( pop, [p.circle(x='x', y='y', source=source.loc[source['fid'] == pop], size=6, color=colours[counter], muted_alpha=0.2 ) ] ))

        legend1 = Legend(items=leg_1, location = (20, 20))
        legend2 = Legend(items=leg_2, location = (25,20))
        p.add_layout(legend1, 'left')
        p.add_layout(legend2, 'left')
        p.legend.label_text_font_size = '10pt'
    
    p.legend.click_policy="mute"
    if key:
        p.add_tools(HoverTool(
         tooltips = [
             ('Population', '@fid'),
             ('Region', '@Region'),
             ('Individual', '@IID'),
                 ]
             ))
    else:
        p.add_tools(HoverTool(
         tooltips = [
             ('Population', '@fid'),
             ('Region', '@Region'),
                 ]
             ))
    
    outfile = output
    print("Saving output to {}.html".format(outfile)) 
    output_file('{}.html'.format(outfile))
   
    show(p)
    return

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Take genotype data in PLINK format, perform UMAP dimension reduction and plot the result")
    parser.add_argument("-i", "--input", default = 'pcs.txt',
    help="Basename of the PLINK file")
    parser.add_argument("-o", "--output", default = 'UMAP',
    help="Name of outputfile")
    parser.add_argument("-k", "--key",
    help="File with Population legend key")

args = parser.parse_args()
(bim, fam, G) = read_input(args.input)
reduced = do_UMAP(G)
plotting(reduced, bim, fam, args.output, args.key)
