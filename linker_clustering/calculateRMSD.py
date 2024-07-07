import pymol
import itertools
import json

# ------------
# PyMOL script that aligns all possible pairs of RFdiffusion models and calculates the RMSD between them.
# ------------

pymol.finish_launching()

# We filter the pymol objects that we want to align.
all_structures = list(filter(lambda x: x.startswith("D1K"), cmd.get_object_list()))

# Dictionary to store the RMSD result between models.
# n_atoms is used to store the number of atoms that were used for the RMSD calculation,
# just to check that all RMSDs were calculated with a representative number of atoms.
rmsd = {}
n_atoms = {}

# We initialize the dictionaries with all model names as keys:
all_combinations = list(itertools.combinations(all_structures, 2))
for i in all_structures[:-1]:
    rmsd[i] = {}
    n_atoms[i] = {}

# For all possible pairs (combinations) we calculate the RMSD between models
# and store the results in the dictionaries.
total = len(all_combinations)
i = 0
for comb in all_combinations:
    result = pymol.cmd.align(comb[0], comb[1], transform=0)

    rmsd[comb[0]][comb[1]] = result[3]
    n_atoms[comb[0]][comb[1]] = result[4]

    i+=1
    print(f"{i}/{total}\t{comb}")

# We write a json file containing the results:
json_dict = {"rmsd": rmsd, "n_atoms": n_atoms}

with open("rmsd_linkers.json", "w") as outfile:
    json.dump(json_dict, outfile, indent=4)