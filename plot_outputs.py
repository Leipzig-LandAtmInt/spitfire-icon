"""
Required modules on Levante:

module load python3 texlive

Use 'evince' to load pdf
"""

import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.pyplot import rc

import sys

mpl.rcParams.update(mpl.rcParamsDefault)
rc('figure', figsize=(8.27,11.69)) # A4 size, portrait 


# Template (up 6 plots per page)
#vars_HERE={'name':'', 'vars':[""], 'vars_aggr':{'name':dim_index}}

# Outputs to show 
vars_phys={'name':'physics', 'vars':["a2l_t_air_box","a2l_wind_air_box", "a2l_wind_10m_box"]}
# page 13
vars_weather={'name':'weather','vars':["dfire_t_air_min_box", "dfire_t_air_max_box", "dfire_precip_daytime_box", "dfire_precip_qc_mavg_box", 
                                       "dfire_precip_mavg_box", "dfire_precip_daily_mmd_box"]}
# page 13 + page 22
vars_ni={'name':'Nesterov index', 'vars':["dfire_nesterov_index_box", "dfire_ab_moisture_diag_box"], 
                             'vars_aggr':{"dfire_fuel_moisture_box":{'omega_O':0, 'omega_NL':1}}} 

# page 16 (1st)
vars_spread_first={'name':'spread (page 16-1)', 'vars':["dfire_i_surface_box", "dfire_fdi_box", "dfire_fuel_pm_tau_box", 
                                        "dfire_fuel_pm_prop_ck_box", "dfire_fuel_pm_fire_box"]} # missing pm_fire_by_area
vars_spread_second={'name':'spread (page 16-2)', 'vars':["dfire_ros_f_box", "dfire_mean_fire_area_box", "dfire_fire_duration_box", 
                                        "dfire_area_burned_box", "dfire_area_burned_fract_box"]}
# page 17
vars_area_burned_diag={'name':'area burned diag', 'vars':["dfire_area_burned_box", "dfire_e_n_ignitions_box", "dfire_fdi_box", 
                                        "dfire_mean_fire_area_box"]} # missing box area
# page 18
vars_mean_fire_area_diag={'name':'mean fire area diag', 'vars':["dfire_mean_fire_area_box", "dfire_l2b_ratio_box", "dfire_distance_travelled_box", 
                                        "dfire_ros_f_box", "dfire_ros_b_box", "dfire_fdi_box"]}
# page 19
vars_ros_diag_first={'name':'ROS diagnostics (1st)', 'vars':["dfire_ros_f_box", "dfire_reaction_intensity_box", "dfire_prop_flux_ratio_box", 
                                        "dfire_fuel_fwd_wind_factor_box", "dfire_preig_heat_box", "dfire_eff_heating_number_box"]}
vars_ros_diag_second={'name':'ROS diagnostics (2nd)', 'vars':["dfire_fuel_fuel_bulk_density_box" ]}

# page 20
vars_pm_tau_diag_general={'name':'pm tau diag', 'vars':["dfire_fuel_pm_tau_box", "dfire_fuel_tau_l_box", "dfire_fuel_tau_c_box"]}
vars_tau_l_diag={'name':'tau l diag', 'vars':["dfire_fuel_tau_l_box"], 'vars_aggr':{"dfire_frac_consump_fcl_box":{'CF1hr':0, 'CF10hr':1, 'CF100hr':2, 'CF1000hr':3}}} 
vars_tau_c_diag={'name':'tau c diag', 'vars':["dfire_fuel_tau_c_box", "dfire_fuel_bark_thickness_box", "dfire_fuel_DBH_diag_box", 
                                        "dfire_fuel_par1_diag_box", "dfire_fuel_par2_diag_box"]}


# page 21 (pm ck diag)
vars_pm_ck_diag_first={'name':'pm_ck diag (1st)', 'vars':["dfire_fuel_pm_prop_ck_box", "dfire_fuel_ck_p_box", "dfire_fuel_r_ck_box", 
                                         "dfire_ck_box", "dfire_fuel_tree_height_box", "dfire_fuel_crown_length_box"]}
vars_pm_ck_diag_second={'name':'pm_ck diag (2nd)', 'vars':["dfire_scorch_height_box", "dfire_fuel_F_scorch_height_box", "dfire_i_surface_box"]}

# page 23 (dead fuel consumption)
vars_dead_fuel_consumption={'name':'dead fuel consumption', 'vars':["dfire_dead_fuel_consumption_1hr_box", "dfire_dead_fuel_consumption_10hr_box", 
    "dfire_dead_fuel_consumption_100hr_box", "dfire_dead_fuel_consumption_1000hr_box"]} # todo: add live fuel consumption

# page  24 (emissions -co2, co, nh4, nh23, n2o, n2-)
# source: mo_dfire_constants.f90
vars_emissions_spc={'name':'emissions by species', 'vars':[],
        'vars_aggr':{"dfire_fuel_emissions_spc_box": {"CO2":0, "CO":1, "CH4":2, "NH3":3, "N2O":4, "N2":5}}} # todo: by element instead of SUM

# page 25 (FC in mol/m2)
# todo

# page 26 (emissions by elements)
vars_emissions_els={'name':'emissions by elements', 'vars':[],
        'vars_aggr':{"dfire_fuel_emissions_els_box": {"C":0, "N":1, "P":2, "C13":3, "C14":4, "N15":5}}} 

# page 27 (residue by elements)
vars_residue={'name':'residue by elements', 'vars':[],
        'vars_aggr':{"dfire_fuel_residue_els_box": {"C":0, "N":1, "P":2, "C13":3, "C14":4, "N15":5}}} 

# page 28 (overflow)
vars_overflow={'name':'overflow by elements', 'vars':[],
        'vars_aggr':{"dfire_fuel_overflow_els_box": {"C":0, "N":1, "P":2, "C13":3, "C14":4, "N15":5}}} 


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
years["end"]  = 1903 # last year not included
#plt_year_start='1901-01-01'
#plt_year_end  ='1902-12-01' # ploting dates, due some discontinuity issues 

# YYYY is replaced by year
filename_template="quincy_standalone_R2B4_land-C-S0-1901-2019-gswp3_lnd_basic_ml_YYYY0101T000000Z_t63.nc"

# generate filename(s)
filenames=[]
for year in range(years["start"], years["end"]):
    filenames.append(filename_template.replace("YYYY", str(year)))
    print("Expected files: %s" % (filenames[-1]))

print("Filenames:", filenames)
outputs = xr.open_mfdataset(filenames, decode_times=False)


# parse date format given by IQ output file.
units, formatting = outputs.time.attrs['units'].split('as') # parse netcdf 'time' units
starting_date=datetime.datetime.strptime(str(outputs['time'].values[0]), formatting.lstrip()) # convert to datetime type
gen_dates=pd.date_range(start=starting_date.strftime('%d/%m/%Y'), periods=outputs.sizes['time'], freq='MS') # convert to likeable format
outputs['time']=gen_dates # put back to dataset

#print(outputs)
#print(outputs.time[:][0])

# testing
#plt.figure() 
#plt.axis('off')
#plt.text(0.5,1,'testing',ha='center',va='top', fontweight='bold')
#ni = outputs["dfire_nesterov_index_box"].sel(lat=lat_site, lon=lon_site, method='nearest')
#ni_short = ni.loc['1901-01-01':'1902-12-01']
#with PdfPages('outputs.pdf') as pdf:
#    plt.subplot(3,2,1) # row, col, index position
#    ni_short.plot()
#    plt.subplot(3,2,2) # row, col, index position
##    ni_short.plot()

    #plt.show()
#    plt.tight_layout()
#    pdf.savefig()  # saves the current figure into a pdf page
#    plt.close()
#sys.exit()

# List to include pages into the pdf
outputPages = []
outputPages.extend([vars_pm_tau_diag_general, vars_tau_l_diag, vars_tau_c_diag])
outputPages.append(vars_phys)
outputPages.append(vars_veg_totals)
outputPages.append(vars_veg_pools)
outputPages.append(vargs_sb)
outputPages.append(vars_dfire_dead_fuel)
outputPages.append(vars_dfire_live_fuel)
#outputPages.append(vars_dfire_live_grass)
outputPages.append(vars_dfire_live_tree)
outputPages.append(vars_dfire_phys)
outputPages.append(vars_dfire_spread)
outputPages.append(vars_weather)
outputPages.append(vars_ni)
outputPages.extend([vars_spread_first, vars_spread_second])
outputPages.append(vars_area_burned_diag)
outputPages.append(vars_mean_fire_area_diag)
outputPages.extend([vars_ros_diag_first, vars_ros_diag_second])
outputPages.extend([vars_pm_ck_diag_first, vars_pm_ck_diag_second])
outputPages.append(vars_dead_fuel_consumption)
outputPages.append(vars_emissions_spc)
outputPages.append(vars_emissions_els)
outputPages.append(vars_residue)
outputPages.append(vars_overflow)

# 

pageCount = 1
with PdfPages('outputs.pdf') as pdf:

    for newPage in outputPages: # Create a new page
        print("New page '%s'" % newPage['name'])
        # if LaTeX is not installed or error caught, change to `usetex=False`
        plt.rc('text', usetex=True)
        plt.figure() 
        plt.axis('off')
        plt.text(0.5,1,newPage['name'],ha='center',va='top', fontweight='bold')

        figureCount=1 # shared between vars and vars_aggr

        if 'vars' in newPage: # if defined, keep going
            for varName in newPage['vars']: # Plot each variable into the same page
                print("  Plotting var '%s' ... " % varName)
                plt.subplot(3,2,figureCount) # row, col, index position
                var_site = outputs[varName].sel(lat=lat_site, lon=lon_site, method='nearest')

                #print("Number of dims, shape:", var_site.ndim, var_site.shape)
                is_var_multi_dim = var_site.ndim > 1
                is_var_many_dims = var_site.ndim > 2
                std_name=var_site.attrs['standard_name']
                units = var_site.attrs['units']

                if is_var_multi_dim: # Aggregate dimensions (when > 1 dims)
                    var_site=var_site.sum(axis=1) #
                elif is_var_many_dims:
                    raise Exception("Not implementation for more than 2 dimenions")

                var_site.plot()
                ylabel_name ="%s [%s]" % (std_name, units)
                plt.ylabel(ylabel_name)
                plt.xlabel('') # remove
                plt.title('') # remove
                figureCount=figureCount+1

        # example
        vars_emissions_spc={'name':'emissions by species', 'vars':[],
                'vars_aggr':{"dfire_fuel_emissions_spc_box": {"CO2":1, "CO":2, "CH4":3, "NH3":4, "N2O":5, "N2":6}}} # todo: by element instead of SUM
        if 'vars_aggr' in newPage: # quincy 3d variables: plot each dimension separately
            for vname, subplots in newPage['vars_aggr'].items(): # for each variable with subplots
                print("  Plotting var_aggr... ", vname, subplots)
                for subVName, ixDim in subplots.items(): # for 
                    print("  Plotting var_aggr '%s' ... " % subVName, ixDim)
                    plt.subplot(3,2,figureCount) # row, col, index position
                    var_site = outputs[vname].sel(lat=lat_site, lon=lon_site, method='nearest')
                    print("Number of dims, shape:", var_site.ndim, var_site.shape)

                    std_name=var_site.attrs['standard_name']
                    units = var_site.attrs['units']
                    ylabel_name ="%s - %s [%s]" % (std_name, subVName, units)
   
                    var_site[:,ixDim].plot()
                    plt.ylabel(ylabel_name)
                    plt.xlabel('') # remove
                    plt.title('') # remove
                    figureCount=figureCount+1

        #plt.tight_layout()
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
