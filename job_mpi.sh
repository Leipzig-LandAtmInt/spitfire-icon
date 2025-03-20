#!/bin/bash
#SBATCH --job-name=IQuincy_testing
#SBATCH --partition=compute
##SBATCH -n 4
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=4
##SBATCH --exclusive
#SBATCH --time=03:30:00
#SBATCH --account=ka1125
#SBATCH --output=my_job.%j.out

# limit stacksize ... adjust to your programs need
# and core file size
set -eux
ulimit -s unlimited 

# Replace this block according to https://docs.dkrz.de/doc/levante/running-jobs/runtime-settings.html#mpi-runtime-settings
#echo "Replace this block according to  https://docs.dkrz.de/doc/levante/running-jobs/runtime-settings.html#mpi-runtime-settings"
#exit 23
# End of block to replace

# Use srun (not mpirun or mpiexec) command to launch
# programs compiled with any MPI library
#srun -l --cpu_bind=verbose --hint=nomultithread \
#  --distribution=block:cyclic ./../../bin/icon

export OMP_NUM_THREADS=8
export ICON_THREADS=1
export OMP_SCHEDULE=dynamic,1
export OMP_DYNAMIC="false"
export OMP_STACKSIZE=200M

: ${no_of_nodes:=${SLURM_JOB_NUM_NODES:=1}} ${mpi_procs_pernode:=$(( 4 * 1))}
export no_of_nodes
export mpi_procs_pernode
((mpi_total_procs=no_of_nodes * mpi_procs_pernode))
export no_of_nodes mpi_procs_pernode mpi_total_procs

unset OMPI_MCA_coll_fca_enable
unset OMPI_MCA_coll_fca_priority

# environment variables for the experiment and the target system
# --------------------------------------------------------------
export EXPNAME="quincy_standalone_R2B4_land-C-S0-1901-1905-gswp3"
export MALLOC_TRIM_THRESHOLD_="-1"
export SLURM_DIST_PLANESIZE="32"
export OMPI_MCA_btl="self"
export OMPI_MCA_coll="^ml,hcoll"
export OMPI_MCA_io="romio321"
export OMPI_MCA_osc="ucx"
export OMPI_MCA_pml="ucx"
export UCX_HANDLE_ERRORS="bt"
export UCX_TLS="shm,dc_mlx5,dc_x,self"
export UCX_UNIFIED_MODE="y"

time srun -l --kill-on-bad-exit=1 --nodes=${SLURM_JOB_NUM_NODES:-1} --distribution=plane --hint=nomultithread --ntasks=$((no_of_nodes * mpi_procs_pernode)) --ntasks-per-node=${mpi_procs_pernode} --cpus-per-task=${OMP_NUM_THREADS} ./../../bin/icon
