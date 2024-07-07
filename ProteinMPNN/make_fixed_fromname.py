import pickle
import sys
import argparse
from pathlib import Path
import json
import numpy as np

# --------
# Makes a dictionary with fixed residue positions for ProteinMPNN. 
# AnfD, AnfK and AnfG sequences are fixed, only the linker sequence is allowed to be modeled.
# --------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Make fixed positions for ProteinMPNN',
                    description='Makes the fixed positions dictionary for ProteinMPNN, fixing all residues but the linker.')
    parser.add_argument("--parsed_pdbs", type=str, help="Path to the jsonl parsed pdbs from ProteinMPNN.")
    parser.add_argument("-o", "--output", type=str, help="Path to the output file.")
    args = parser.parse_args()

    with open(args.parsed_pdbs, "r") as json_file:
        json_list = list(json_file)

    my_dict = {}
    # For each structure in the parsed pdbs file:
    for json_str in json_list:
        result = json.loads(json_str)
        # Get the chains that it has:
        all_chain_list = [item[-1:] for item in list(result) if item[:9]=='seq_chain']
	    
        # Extract linker residues from name:
        start, length = [int(i) for i in result['name'].split('_')[2].split('#')]
        linker_residues = list(range(start, start+length))

        fixed_position_dict = {}

        # Fix chain A (AnfD-linker-AnfK), except for the linker residues: 
        seq_length = len(result[f'seq_chain_A'])
        all_residue_list = (np.arange(seq_length)+1).tolist()
        fixed_position_dict['A'] = list(set(all_residue_list) - set(linker_residues))

        # Fix the rest of the chains (AnfG)
        all_chain_list.remove('A')
        for chain in all_chain_list:
            seq_length = len(result[f'seq_chain_{chain}'])
            all_residue_list = (np.arange(seq_length)+1).tolist()
            fixed_position_dict[chain] = all_residue_list

        my_dict[result['name']] = fixed_position_dict

    # Write the fixed positions dictionary to a file for later use as input to ProteinMPNN
    with open(args.output, "w") as f:
        f.write(json.dumps(my_dict) + '\n')