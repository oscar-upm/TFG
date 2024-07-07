import pymol
import re

pymol.finish_launching()

# Creates a single selection (selection_name) with the linker residues of the provided models (models)
def select_linkers(selection_name, models):
    selection_list = []
    for model in models:
        start, length = [int(x) for x in model.split("_")[2:4]]
        selection_list.append(f'({model} and chain A and resi {start}-{start+length-1})')
    selection_string = ' or '.join(selection_list)
    pymol.cmd.select(selection_name, selection_string)

pymol.cmd.extend('select_linkers', select_linkers)