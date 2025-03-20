#!/bin/sh

set -eux

ext=".nc"

for file in quincy_standalone_R2B4_land-C-S0-1901-2019-gswp3_lnd_basic_ml_*0101T000000Z.nc; do
    file_name="$(basename "$file" "$ext")"
    file_name_ext="${file_name}_t63.nc"
    cdo remapcon,t63grid ${file} ${file_name_ext}
done


#cdo remapcon,t63 quincy_standalone_R2B4_land-C-S0-1901-2019-gswp3_lnd_basic_ml_19010101T000000Z.nc
