import os
import argparse
import requests
import glob
import json
import time
from Bio import SeqIO

# --------
# Script to model the ProteinMPNN-predicted sequence into the linker backbone using SWISS-MODEL
# homology modeling API
# --------

token = "[SWISS-MODEL USER TOKEN]"

# Extracts the sequences of the chains from a pdb file:
def extract_sequence_from_pdb(pdb_file):
    seqs = []
    for record in SeqIO.parse(pdb_file, "pdb-atom"):
        seqs.append(str(record.seq))
    return seqs

# Calls the SWISS-MODEL Modeling API to model a sequence
# using pdb_file as template (User Template modeling).
# Returns the project id from the API for output retrieval when the task completes.
def run_swissmodel_job(sequence, pdb_file):
    with open(pdb_file) as file:
        template_coordinates = file.read()

    url = "https://swissmodel.expasy.org/user_template"
    headers = { "Authorization": f"Token {token}"}
    payload = {
        "target_sequences": sequence,
        "template_coordinates": template_coordinates,
        "project_title": os.path.splitext(os.path.basename(pdb_file))[0]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code not in [200, 202]:
        print(f"RESPONSE {response.status_code} for pdb {pdb_file}.")
        print(sequence)
        return
    project_id = response.json()['project_id']
    return project_id

# Checks the SWISS-MODEL job with id project_id to see if it has finished.
def check_job(project_id):
    response = requests.get(
        f"https://swissmodel.expasy.org/project/{ project_id }/models/summary/", 
        headers={ "Authorization": f"Token {token}" })
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "UNREACHABLE"}

# Saves the output structure from SWISS-MODEL to a new pdb file.
def save_job(project_id, model_id, save_path):
    response = requests.get(
            f"https://swissmodel.expasy.org/project/{project_id}/models/{model_id}.pdb", 
            headers={ "Authorization": f"Token {token}" })

    with open(save_path, "wb") as file:
        file.write(response.content)

# Function that recursively checks the status of all launched SWISS-MODEL
# jobs and saves the resulting models to output_folder when they finish.
def retrieve_results(output_folder):
    # The job ids are retrieved from a previously saved json file: project_ids.json
    with open("project_ids.json") as file:
        project_ids, pdb_files = json.load(file)

    project_ids_original = project_ids.copy()

    # Repeatedly check for job completion and save the completed ones:
    while len(project_ids) > 0:
        project_list = [check_job(project_id) for project_id in project_ids]
        to_pop = []
        for i, job in enumerate(project_list):
            if job['status'] == 'COMPLETED':
                to_pop.append(i)
                pdb_file = pdb_files[i]
                project_id = project_ids[i]
                # Save job:
                save_path = os.path.join(output_folder, f"{job['project_title']}.pdb")
                save_job(project_id, job['models'][0]['model_id'], save_path)
                print(f"COMPLETED {save_path}")
            elif job['status'] == 'FAILED':
                to_pop.append(i)
                print(f"FAILED {save_path}")
        
        # Remove completed and failed jobs:
        project_ids = [project_id for i, project_id in enumerate(project_ids) if i not in to_pop]
        print('.', end="", flush=True)
        time.sleep(10)

    # Do a final request to get all the info for each modeling
    full_details = []
    for project_id in project_ids_original:
        response = requests.get(
            f"https://swissmodel.expasy.org/project/{project_id}/models/full-details", 
            headers={ "Authorization": f"Token {token}" })
        data = response.json()
        full_details.append(data)
    with open("modelling_results.json", "w") as file:
        json.dump(full_details, file, indent=4)


# input_folder: folder with all the pdb files to be used as templates
# output_folder: output folder to which modeled pdb files will be saved
# seqs: folder with all sequences to be modeled into the pdb templates
# Each sequence file must have the same name as the pdb template it will be modeled into.
def main(input_folder, output_folder, seqs):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    pdb_files = glob.glob(os.path.join(input_folder, "*.pdb"))

    # Start swissmodel jobs
    project_ids = []
    for pdb_path in pdb_files:
        # In case no sequence is provided for the pdb, extract the sequence from the pdb file.
        if seqs is None:
            sequence = extract_sequence_from_pdb(pdb_path)[0]
        else:
            # Else, use the sequence with the same name as the pdb file:
            with open(os.path.join(seqs, f'{os.path.splitext(os.path.basename(pdb_path))[0]}.fa')) as file:
                sequence = file.readlines()[1].strip('\n').split('/')[0]

        # Start a modeling job with the sequence and pdb template:
        project_id = run_swissmodel_job(sequence, pdb_path, output_folder)
        project_ids.append(project_id)

    # Write project ids to file, to avoid losing them:
    with open("project_ids.json", "w") as file:
        json.dump([project_ids, pdb_files], file)

    retrieve_results(output_folder)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SwissModel User-Template jobs for PDB files")
    parser.add_argument("input_folder", help="Folder containing PDB files")
    parser.add_argument("output_folder", help="Folder to save the resulting models")
    parser.add_argument("--seqs", help="Folder with the corresponding sequences")
    parser.add_argument("--resume", help="Retrieve results from project_ids.json", default=False, action='store_true')
    args = parser.parse_args()

    if args.resume:
        # To retrieve results if jobs have been started already
        retrieve_results(args.output_folder)
    else:
        main(args.input_folder, args.output_folder, args.seqs)
