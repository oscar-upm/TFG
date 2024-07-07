#!/bin/bash
#SBATCH -p gpu
#SBATCH --time=01:00:00        # total run time limit in HH:MM:SS
#SBATCH -c 2
#SBATCH --output=run.out

# Local ProteinMPNN git repository:
root_folder="/home/oscarp/ProteinMPNN"

output_dir="./output"
if [ ! -d $output_dir ]
then
    mkdir -p $output_dir
fi

# Files generated using scripts parse_chains.sh and make_fixed_fromname.py
path_for_parsed_chains=$output_dir"/parsed_pdbs.jsonl"
path_for_fixed_positions=$output_dir"/fixed_positions.jsonl"

# Run the inference
python $root_folder/protein_mpnn_run.py \
        --jsonl_path $path_for_parsed_chains \
        --out_folder $output_dir \
	--model_name v_48_020 \
        --fixed_positions_jsonl $path_for_fixed_positions \
        --num_seq_per_target 100 \
        --sampling_temp "0.1" \
        --seed 37 \
        --batch_size 10
