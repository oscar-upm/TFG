# Linker backbone generation with RFdiffusion

This folder contains the scripts used to generate the D1K1 and D1K2 linker sets using RFdiffusion. 


## Generation of D1K1 and D1K2 linker backbones

Scripts `D1K1_20-60.slurm` and `D1K2_20-60.slurm` were used to instruct the cluster to run RFdiffusion and generate 101 linker backbones for D1K1 and D1K2. These are SLURM scripts that can be run using the sbatch command. SLURM is a workload manager commonly used in HPC (High Performance Computing) clusters to distribute jobs between computing nodes ("individual computers").

The scripts ran RFdiffusion on a node with an NVIDIA A100 GPU with 40GB of memory. Despite its computing power, generating the linker backbones took 3 days, running both scripts simultaneously.

The output was a folder containing pdb and trb files named like this:

- `[LINKER SET]_20-60_[LINKER NUMBER].pdb`
- `[LINKER SET]_20-60_[LINKER NUMBER].trb`

For example: `D1K1_20-60_43.pdb` and `D1K1_20-60_43.trb`.

The pdb files contained the fixed backbones of the D, K and G subunits, together with the newly generated linker backbone joining the D and K subunits. The trb files are binary files containing metadata about the generation process.


## Extracting linker residue positions

For the next steps, it was necessary to identify the linker portion in the generated pdb files. `linker_residues.py` extracts the residue positions that make up the linker for a given RFdiffusion model using information from the trb file. 


## Rename pdb files

For convenience, the information about the linker residues was directly encoded in the pdb file names of the RFdiffusion models. The `rename_linkers.py` script uses the `linker_residues.py` module to get the linker start residue and length, then adds them as fields to the pdb filename folowing the format `[START]#[LENGTH]`.

Example: `D1K1_20-60_43.pdb` -> `D1K1_20-60_516#23_43.pdb`