import argparse
import glob
from linker_residues import *
import os

# ------------
# This script renames linker pdb files to add the start and exact length of the linker to the name
# ------------

# Adds the length found in the trb file to the pdbs name. It is assumed the trb and pdb are named the same.
def add_length_to_pdb_name(trb_file):
    dir = os.path.dirname(trb_file)
    old_name = os.path.splitext(os.path.basename(trb_file))[0]
    pdb_file = os.path.join(dir, f"{old_name}.pdb")

    # Check that both the trb and pdb files exist before continuing:
    if not os.path.isfile(trb_file):
        raise Exception(f"{trb_file} does not exist.")
    if not os.path.isfile(pdb_file):
        raise Exception(f"{pdb_file} does not exist.")

    # -- Construct the new name from the old_name and the start and length of the linker --ç
    # Get linker residues using linker_residues module
    linker = get_linker_from_trb(trb_file)
    spliced_name = old_name.split('_')
    linker_field = f"{linker[0]}#{len(linker)}"

    # Check that the length field has not been added already.
    if linker_field in spliced_name:
        print(f"{old_name} already has a length field. Omitting.")
        return

    # Add the length field to the old name to form the new name.
    spliced_name.insert(2, linker_field)
    new_name = "_".join(spliced_name)
    
    # Rename pdb and trb files
    os.rename(
        pdb_file,
        os.path.join(dir, f"{new_name}.pdb")
    )
    print(pdb_file, os.path.join(dir, f"{new_name}.pdb"))
    os.rename(
        trb_file,
        os.path.join(dir, f"{new_name}.trb")
    )
    print(trb_file, os.path.join(dir, f"{new_name}.trb"))

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid directory")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='Rename linkers',
                    description='This script renames linker pdb files to add the start and exact length of the linker to the name')
    parser.add_argument('pdb_folder', type=dir_path, help='Path to the folder containing the trb and pdb files')

    args = parser.parse_args()

    for file in glob.glob(os.path.join(args.pdb_folder, "*.trb")):
       try:
           add_length_to_pdb_name(file)
       except Exception as e:
           print(e)
           exit(1)

