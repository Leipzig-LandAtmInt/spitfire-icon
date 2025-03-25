"""
Required modules on Levante:

module load python3 texlive

Use 'evince' to load pdf
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.pyplot import rc


mpl.rcParams.update(mpl.rcParamsDefault)
rc('figure', figsize=(8.27,11.69)) # A4 size, portrait 

cell_id=1


# Outputs to show 
vars_phys={'name':'physics', 'vars':["a2l_t_air_box","a2l_wind_air_box", "a2l_wind_10m_box"]}
vars_veg_totals={'name':'veg totals', 'vars':["veg_veg_pool_total_c_box", "veg_veg_litterfall_total_c_box"]} # also N
vars_veg_pools={'name':'veg pools', 'vars':["veg_veg_pool_leaf_c_box", "veg_veg_pool_wood_c_box", "veg_veg_pool_fine_root_c_box"]} # also N
vargs_sb = {'name':'sb', 'vars':["sb_sb_pool_total_c_box", "sb_sb_pool_woody_litter_c_box"]} # el primer nomes N
vars_dfire_dead_fuel = {'name':'dfire dead fuel', 'vars':["dfire_fuel_dead_fuel_1hr_dfp_box", 
                                                    "dfire_fuel_dead_fuel_10hr_dfp_box",
                                                    "dfire_fuel_dead_fuel_100hr_dfp_box",
                                                    "dfire_fuel_dead_fuel_1000hr_dfp_box"]} 
vars_dfire_live_fuel = {'name':'dfire live fuel', 'vars':["dfire_fuel_live_fuel_1hr_lfp_box", 
                                                    "dfire_fuel_live_fuel_10hr_lfp_box", 
                                                    "dfire_fuel_live_fuel_100hr_lfp_box", 
                                                    "dfire_fuel_live_fuel_1000hr_lfp_box"]} 
vars_dfire_live_grass = {'name':'dfire live grass', 'vars':["dfire_fuel_live_grass_fuel_1hr_lfp_box", 
                                                    "dfire_fuel_live_grass_fuel_10hr_lfp_box", 
                                                    "dfire_fuel_live_grass_fuel_100hr_lfp_box",
                                                    "dfire_fuel_live_grass_fuel_1000hr_lfp_box"]}
vars_dfire_live_tree  = {'name':'dfire live tree', 'vars':["dfire_fuel_live_tree_fuel_1hr_lfp_box", 
                                                    "dfire_fuel_live_tree_fuel_10hr_lfp_box",
                                                    "dfire_fuel_live_tree_fuel_100hr_lfp_box",
                                                    "dfire_fuel_live_tree_fuel_1000hr_lfp_box"]}
vars_dfire_phys = {'name':'dfire phys', 'vars':["dfire_fuel_forest_fract_box", "dfire_fuel_grass_fract_box", "dfire_fuel_moisture_extinction_box", "dfire_fuel_fwd_wind_factor_box"]}
vars_dfire_spread = {'name':'dfire spread', 'vars':["dfire_fuel_fuel_bulk_density_box", "dfire_fuel_pm_fire_box", "dfire_fuel_pm_prop_ck_box"]}

# FR-Pue coordiantes
lat_site=44.24
lon_site=5.4

years = {}
years["start"]= 1901
years["end"]  = 1910
# YYYY is replaced by year
filename_template="quincy_standalone_R2B4_land-C-S0-1901-2019-gswp3_lnd_basic_ml_YYYY0101T000000Z_t63.nc"

# generate filename(s)
filenames=[]
for year in range(years["start"], years["end"]):
    filenames.append(filename_template.replace("YYYY", str(year)))

print("Filenames:", filenames)
outputs = xr.open_mfdataset(filenames)


# List to include pages into the pdf
pageCount = 1
outputPages = []
outputPages.append(vars_phys)
outputPages.append(vars_veg_totals)
outputPages.append(vars_veg_pools)
outputPages.append(vargs_sb)
outputPages.append(vars_dfire_dead_fuel)
outputPages.append(vars_dfire_live_fuel)
outputPages.append(vars_dfire_live_grass)
outputPages.append(vars_dfire_live_tree)
outputPages.append(vars_dfire_phys)
outputPages.append(vars_dfire_spread)

with PdfPages('outputs.pdf') as pdf:

    for newPage in outputPages: # Create a new page
        print("New page '%s'" % newPage['name'])
        # if LaTeX is not installed or error caught, change to `usetex=False`
        plt.rc('text', usetex=True)
        plt.figure() 
        plt.axis('off')
        plt.text(0.5,0.5,"my title",ha='center',va='top')

        figureCount=1
        for varName in newPage['vars']: # Plot each variable into the same page
            print("  Plotting var '%s' ... " % varName)
            plt.subplot(3,2,figureCount) # row, col, index position
            var_site = outputs[varName].sel(lat=lat_site, lon=lon_site, method='nearest')

            print("Number of dims, shape:", var_site.ndim, var_site.shape)
            is_var_multi_dim = var_site.ndim > 1
            is_var_many_dims = var_site.ndim > 2

            if is_var_multi_dim: # Aggregate dimensions (when > 1 dims)
                var_site=var_site.sum(axis=1) #
            elif is_var_many_dims:
                raise Exception("Not implementation for more than 2 dimenions")

            var_site.plot()
            figureCount=figureCount+1

        #plt.tight_layout()
        #plt.title('%s (Page %d)' % (newPage["name"], pageCount)) # related to the plot title, not the page 
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

        pageCount = pageCount + 1

    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'IQ outputs'
    d['Author'] = 'Ajp'
    d['Subject'] = 'Spitfire outputs from IQ'
    d['Keywords'] = 'quincy icon spitfire'
    d['CreationDate'] = datetime.datetime.today()
    d['ModDate'] = datetime.datetime.today()
