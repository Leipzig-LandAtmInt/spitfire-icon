#!/bin/bash

# select a box
# cdo sellonlatbox,-20,60,-40,40 bc_greenhouse_gases.nc bc_greenhouse_gases_africa.nc

# add attribute
# cdo setattribute,number_of_grid_used=50 icon_grid_africa_r2b3.nc icon_grid_africa_r2b3_50.nc
#
#set -eux

#
# DOCS:
# 
# sellonlatbox,lon1,lon2,lat1,lat2 infile outfile
#
# Where:
# lon1 is FLOAT  Western longitude
# lon2 is FLOAT  Eastern longitude
# lat1 is FLOAT  Southern or northern latitude
# lat2 is FLOAT  Northern or southern latitude
#
# -sellonlatbox,${lonMin},${lonMax},${latMin},${latMax} 
#

module load cdo
module load nco

set -eux

# FR Pue site coordinates
#lat=43.719
#lon=3.618
sitename="frpue"
#sitebox="2,6,42,46" 
#icongrid="icon_grid_0049_R02B04_germany.nc"
#icongrid_fname=$(basename ${icongrid} .nc)
new_icongrid="icon_grid_0049_R2B4_fr_pue.nc" #"${icongrid_fname}_${sitename}.nc"
climate_path="/work/mj0143/icon_land_data/forcing/gswp3/R02B04/0049/gswp3_with_np_depositions"
#climate_fname="gswp3_with_dep_R2B4_0049_YYYY.nc"

bc_quincy_soil="/work/mj0143/icon_land_data/icbc_files/rev001/r2b4/0049/bc_quincy_soil_0049.nc"
bc_land_sso="/pool/data/ICON/grids/public/mpim/0049/land/r0004/bc_land_sso_1979.nc"
bc_land_soil="/pool/data/ICON/grids/public/mpim/0049/land/r0004/bc_land_soil_1979.nc"
bc_land_phys="/pool/data/ICON/grids/public/mpim/0049/land/r0004/bc_land_phys_1979.nc"
bc_land_frac="/work/mj0143/icon_land_data/land_cover_fraction/rev001/r2b4/0049/Quincy_ESACCI_2020_r2b4_11_pft_bc_land_frac.nc"
ic_land_soil="/pool/data/ICON/grids/public/mpim/0049/land/r0004/ic_land_soil_1979.nc"

#echo "creating new icongrid for $sitename ..."
#cdo sellonlatbox,${sitebox} ${icongrid} ${new_icongrid}_tmp
## add attribute to conform icon standards
#cdo setattribute,number_of_grid_used=49 ${new_icongrid}_tmp ${new_icongrid}_tmp1
## add missing attributes
#cdo setattribute,uuidOfHGrid=2edbc23c-2027-11ef-a1e3-a9a7b49264d6 ${new_icongrid}_tmp1 ${new_icongrid}_tmp2
## rename modified dimension to original names (same as icon_grid_...)
#yes | ncrename -d y,max_chdom -d x,cell_grf -d x_2,edge_grf -d x_3,vert_grf ${new_icongrid}_tmp2 ${new_icongrid}
## remove temporary file(s)
#rm -f ${new_icongrid}_tmp ${new_icongrid}_tmp1 ${new_icongrid}_tmp2
#echo ""


# expected format: climate_YYYY.nc
for filename in climate_19*.nc; do
  echo $filename
  arrIN=(${filename//_/ }) # climate_, XXXX.nc
  echo "arrIN: $arrIN"
  year=(${arrIN[1]//./ }) # XXXX.nc, 
  echo "year: $year"
  new_filename=${arrIN[0]}_${sitename}_${arrIN[1]} 

  echo "$filename -> $new_filename"
  if [ -f $new_filename ];
  then
	echo "file found, skip to next iteration..."
        continue
  fi

  cdo remapcon,${new_icongrid} $filename $new_filename
done

cdo remapcon,${new_icongrid} $bc_land_frac bc_land_frac_${sitename}.nc
cdo remapcon,${new_icongrid} $bc_land_phys bc_land_phys_${sitename}.nc
cdo remapcon,${new_icongrid} $bc_land_soil bc_land_soil_${sitename}.nc
cdo remapcon,${new_icongrid} $bc_land_sso bc_land_sso_${sitename}.nc
cdo remapcon,${new_icongrid} $bc_quincy_soil bc_quincy_soil_${sitename}.nc
cdo remapcon,${new_icongrid} $ic_land_soil ic_land_soil_${sitename}.nc

# remove soft links
rm -f bc_land_frac.nc bc_land_phys.nc bc_land_soil.nc bc_land_sso.nc bc_quincy_soil.nc ic_land_soil.nc

# recreate soft links
ln -s bc_land_frac_${sitename}.nc bc_land_frac.nc
ln -s bc_land_phys_${sitename}.nc bc_land_phys.nc
ln -s bc_land_soil_${sitename}.nc bc_land_soil.nc
ln -s bc_land_sso_${sitename}.nc bc_land_sso.nc
ln -s bc_quincy_soil_${sitename}.nc bc_quincy_soil.nc
ln -s ic_land_soil_${sitename}.nc ic_land_soil.nc
