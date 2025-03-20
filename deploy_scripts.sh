#!/bin/bash

echo "Deploying auxiliary scripts into the current folder..."

ICON_PATH=/work/mj0143/b301060/build_run/iq_2024-02-16_testrun
SCRIPTS_PATH=${ICON_PATH}/scripts/spitfire-icon

ln -s ${SCRIPTS_PATH}/plot_outputs.py .
ln -s ${SCRIPTS_PATH}/clean_exp.sh .
ln -s ${SCRIPTS_PATH}/job_mpi.sh . 
ln -s ${SCRIPTS_PATH}/outputs_grid_icon_to_t63.sh . 
ln -s ${SCRIPTS_PATH}/env_outputs_setup.sh .
ln -s ${SCRIPTS_PATH}/forcings_global_to_site.sh .
echo "done :-)"
