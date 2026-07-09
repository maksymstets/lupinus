import os
import shutil
import pandas as pd
from pathlib import Path

# 1. Define paths (Adjust CSV name if yours is slightly different)
INPUT_FILE = Path("/home/maksym/biopep-automation/Excel tables results/optimised_peptides_for_admet_metadata.csv")
SOURCE_DIR = Path("/home/maksym/biopep-automation/Excel tables results/prepared_peptides_pdbqt")

# 2. Define the three target subfolders
BASE_OUTPUT_DIR = Path("/home/maksym/biopep-automation/Excel tables results/sorted_peptides")
ace_only_dir = os.path.join(BASE_OUTPUT_DIR, "ACE_only")
dpp_only_dir = os.path.join(BASE_OUTPUT_DIR, "DPP_only")
dual_dir = os.path.join(BASE_OUTPUT_DIR, "Dual_activity")

# Create the folders if they don't exist yet
for folder in [ace_only_dir, dpp_only_dir, dual_dir]:
    os.makedirs(folder, exist_ok=True)

# 3. Load the dataset
df = pd.read_csv(INPUT_FILE)

counts = {"ACE_only": 0, "DPP_only": 0, "Dual_activity": 0, "Missing": 0}

print("Starting file organization...")

for idx, row in df.iterrows():
    sequence = row['Sequence']
    activity = row['Activity']
    
    # Based on our previous script, the files are named "Peptide_SEQUENCE.pdbqt"
    filename = f"Peptide_{sequence}.pdbqt"
    source_file_path = os.path.join(SOURCE_DIR, filename)
    
    # Check if the file actually exists before trying to move it
    if not os.path.exists(source_file_path):
        counts["Missing"] += 1
        continue
        
    # 4. Classification Logic
    # Check if it has BOTH activities listed in the string
    if "ACE inhibitor" in activity and "dipeptidyl peptidase IV inhibitor" in activity:
        target_dir = dual_dir
        counts["Dual_activity"] += 1
        
    # Check if it is exclusively ACE
    elif "ACE inhibitor" in activity:
        target_dir = ace_only_dir
        counts["ACE_only"] += 1
        
    # Check if it is exclusively DPP
    elif "dipeptidyl peptidase IV inhibitor" in activity:
        target_dir = dpp_only_dir
        counts["DPP_only"] += 1
        
    else:
        print(f"⚠️ Unrecognized activity pattern for {sequence}: {row['Activity']}")
        continue

    # 5. Copy the file into its corresponding functional folder
    shutil.copy(source_file_path, os.path.join(target_dir, filename))

print("\n--- Sorting Complete! ---")
print(f"Copied to ACE_only:      {counts['ACE_only']} files")
print(f"Copied to DPP_only:      {counts['DPP_only']} files")
print(f"Copied to Dual_activity: {counts['Dual_activity']} files")
if counts["Missing"] > 0:
    print(f"⚠️ Note: {counts['Missing']} peptides from CSV were not found as .pdbqt files.")
