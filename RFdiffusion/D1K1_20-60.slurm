#!/bin/bash
#SBATCH -c 1								# Number of CPUs to use
#SBATCH --mem=4GB							# Maximum RAM to use
#SBATCH -N 1								# Number of nodes to use
#SBATCH --output=./log/D1K1_20-60_%j.out 	# STDOUT file, %j for job id
#SBATCH --partition=gpu						# Run in GPU node
#SBATCH --time=3-00:00:00          			# total run time limit in DD-HH:MM:SS

#-------------------
# This script creates 101 new linkers between 20 and 60 aa long from D1 to K1, in the presence of the full GDK structure. 
#-------------------

# Load cluster modules required to run the RFdiffusion model
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all
ml libffi/3.4.4-GCCcore-12.2.0
ml OpenSSL/1.1
ml CUDA/11.1.1-GCC-10.2.0
ml CUDAcore/11.1.1
ml GDRCopy/2.1-GCCcore-10.2.0-CUDA-11.1.1
ml NCCL/2.8.3-GCCcore-10.2.0-CUDA-11.1.1
ml UCX/1.9.0-GCCcore-10.2.0-CUDA-11.1.1
ml cuDNN/8.0.4.30-CUDA-11.1.1

# Path to the RFdiffusion cloned git repository
RFDIR=$HOME/rfdiffusion

# Run RFDiffusion in the GPU node of the cluster
# We give it as input the 8BOQ pdb and instruct to generate linkers with the contig [A2-516/20-60/B2-462/0 C14-132]
srun python $RFDIR/RFdiffusion/scripts/run_inference.py 'contigmap.contigs=[A2-516/20-60/B2-462/0 C14-132]' \
	inference.model_directory_path=$HOME/rfdiffusion/RFdiffusion/models \
	inference.output_prefix=./outputs/D1K1_20-60 \
	inference.input_pdb=$RFDIR/design_linkers/inputs/8BOQ.pdb \
	inference.num_designs=101
