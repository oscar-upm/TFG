# Sequence prediction using ProteinMPNN

This folder contains the code to design the sequence for the AnfDK fusions with linker prototypes, using ProteinMPNN.

## Handling missing residues

The script `add_missing_aa.py` changes the sequence of the first two residues of each linker, and the last one, to the missing residues of the D and K subunits in PDB ID: 8BOQ.

## Parse pdb files

PDB files have to be parsed into a single file before they can be fed to ProteinMPNN. `parse_chains.sh` is a bash script where a ProteinMPNN util script is called to parse the linker prototype pdb files.

## Fix non-linker residues sequence

The sequences of all non-linker residues in the pdb files have to be fixed, so that ProteinMPNN only models the linker sequence. Using script `make_fixed_fromname.py`, a json file containing all residues positions that should have their sequence fixed was generated, to use as input for ProteinMPNN. 

## Run ProteinMPNN

ProteinMPNN was run in a GPU node in the HPC cluster using `run.slurm` script. It took as input the parsed pdb files and the fixed residues, and generated fasta files containing 100 predicted sequences for each prototype. Finally, the sequences with the best global_score were extracted with `extract_best_sequences.py`. The global score of ProteinMPNN is a negative log probability, so the sequence with the lowest global_score is the best (it is more probable).