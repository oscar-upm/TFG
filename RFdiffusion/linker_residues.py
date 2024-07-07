import pickle
import argparse
import sys

# Determines the residues that conform the linker from the trb file of an RFdiffusion output.
#   - trb_file: path to the trb file
def get_linker_from_trb(trb_file : str):
    with open(trb_file, "rb") as file:
        data = pickle.load(file)

    # Get the residues in the A chain that are fixed (D and K subunits)
    fixed_residues = [pos for chain, pos in data['con_hal_pdb_idx'] if chain == 'A'] 
    if len(fixed_residues) == 0:
        print("The PDB does not have a fixed A chain", file=sys.stderr)
        exit(253)

    # The rest of the residues conform the newly generated linker backbone
    linker = [x for x in range(1,fixed_residues[-1]+1) if x not in fixed_residues]
    
    return linker

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='Linker residues',
                    description='Determines the residues that conform the linker from the trb of an RFDiffusion output.')
    parser.add_argument('trb_file')
    parser.add_argument('-l', '--length', 
                        action='store_true',
                        help='Outputs the linker length instead of the residues that conform it.')
    
    args = parser.parse_args()

    # Get the linker residues
    try:
        linker = get_linker_from_trb(args.trb_file)
        if not args.length:
            print(" ".join(str(x) for x in linker))
        else:
            print(len(linker))
    except FileNotFoundError:
        print("The file provided does not exist.", file=sys.stderr)
        exit(255)
    except (pickle.UnpicklingError, KeyError):
        print("The file is not a valid RFDiffusion TRB.", file=sys.stderr)
        exit(254)
