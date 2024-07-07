import glob
import re
import os

# ------------
# Extract the sequence with the best global_score from a ProteinMPNN fasta file.
# ------------

# Regular expression to target the global_score field in the fasta sequence name.
expr = r'global_score=(.*?),'

input_dir = 'seqs/'
output_dir = 'best_seqs/'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for file_path in glob.glob(os.path.join(input_dir, "*.fa")):
    with open(file_path) as file:
        lines = file.readlines()

    entries = list(filter(lambda line: line.startswith('>'), lines))
    seqs = list(filter(lambda line: not line.startswith('>'), lines))

    # Take the entry with the lowest global score:
    min_score = float('inf')
    min_index = -1
    for i, entry in enumerate(entries):
        match = re.search(expr, entry)
        if match is None:
            print(f"No se encontro la expresion {expr} en una secuencia.")
        else:
            score = float(match.group(1))
            if score < min_score:
                min_score = score
                min_index = i
    
    with open(os.path.join(output_dir, os.path.basename(file_path)), 'w') as out_file:
        # Add name to the entry:
        basename = os.path.splitext(os.path.basename(file_path))[0]
        print(min_index)
        entry = f'>{basename}, ' + entries[min_index][1:]
        out_file.write(entry)
        out_file.write(seqs[min_index])
