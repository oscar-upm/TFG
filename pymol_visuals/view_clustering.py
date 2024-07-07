import pymol
import json
import numpy as np

# A python script to ease the visualization of clusterings in PyMOL.
# It requires as input the json file coming from the hierarchical clustering (clustering_file),
# which must contain three lists in order:
# - The RFdiffusion model names.
# - Their corresponding cluster number.
# - The selected prototypes

# Create a selection for each cluster of linkers
def select_all_clusters(selection_prefix, clustering_file):
    with open(clustering_file) as file:
        names, cl = json.load(file)
    for n in np.unique(cl):
        selection_name = f'{selection_prefix}{n}'
        print(selection_name, [name for i, name in enumerate(names) if cl[i] == n])
        selection_string = ' or '.join([name for i, name in enumerate(names) if cl[i] == n])
        pymol.cmd.select(name=selection_name, selection=selection_string)

# Create a selection for each prototype linker
def select_prototypes(selection_prefix, clustering_file):
    with open(clustering_file) as file:
        names, cl, prototypes = json.load(file)
    for n, prototype in enumerate(prototypes):
        selection_name = f'{selection_prefix}{n}'
        print(f"{selection_name}: {prototype}")
        pymol.cmd.select(name=selection_name, selection=prototype)

pymol.cmd.extend('select_all_clusters', select_all_clusters)
pymol.cmd.extend('select_prototypes', select_prototypes)
