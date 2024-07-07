import glob
import os
import numpy as np

# ---------
# Script that sets the sequence for the first two linker residues to VAL and GLY and 
# the sequence for the last linker residue to MET in the pdb file.
# ---------

# Input folder containing the prototype pdb files (coming from RFdiffusion). 
input_folder = 'prototypes'
# Output folder that will contain the new pdb files with the sequence changed.
output_folder = 'output'

N_term_residues = ['VAL', 'GLY']
C_term_residues = ['MET']

if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

for pdb_file in glob.glob(os.path.join(input_folder, '*.pdb')):
    with open(pdb_file) as file:
        data = file.readlines()

    name = os.path.splitext(os.path.basename(pdb_file))[0]
    # Extract linker location
    start, length = [int(x) for x in name.split('_')[2].split('#')]
    
    # Calculate residue positions
    residues = {}
    for i, res in enumerate(N_term_residues):
        residues[i+start] = res

    for i, res in enumerate(C_term_residues[::-1]):
        residues[start+length-1-i] = res

    # Change name to reflect the new linker bounds:
    new_start = start + len(N_term_residues)
    new_length = length - len(N_term_residues) - len(C_term_residues)
    linker = f'{new_start}#{new_length}'
    split_name = name.split('_')
    split_name[2] = linker
    new_name = '_'.join(split_name)

    # Substitute in pdb data and write the new pdb:
    with open(os.path.join(output_folder, f'{new_name}.pdb'), 'w') as file:
        for line in data:
            pos = int(line[22:26].strip(' '))
            if pos in residues.keys():
                line = line[:17] + residues[pos] + line[20:]
            
            file.write(line)