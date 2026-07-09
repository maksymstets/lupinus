import os
import glob

#small renaming script to include full enzyme names in filenames
# Set this to the folder containing your current files
TARGET_DIR = "/home/maksym/lupinus_analysis/BIOPEP_results/BIOPEP_Batch_Outputs_Sequential"

# Explicit mapping from the old short names to your new triple-underscore template names
mapping = {
    "pepsin_(pH___2)": "39___pepsin_(pH___2)___3.4.23.1",
    "trypsin": "12___trypsin___EC_3.4.21.4",
    "chymotrypsin_(A)": "11___chymotrypsin_(A)___EC_3.4.21.1",
    "papain": "24___papain___EC_3.4.22.2",
    "ficin": "25___ficin___EC_3.4.22.3",
    "Stem_bromelain": "30___Stem_bromelain___EC_3.4.22.32",
    "subtilisin": "41___subtilisin___EC_3.4.21.62",
    "pepsin_(pH_1.3)": "13___pepsin_(pH_1.3)___EC_3.4.23.1"
}

if not os.path.exists(TARGET_DIR):
    print(f"Directory not found: {TARGET_DIR}. Please double check your path string.")
    exit()

files = glob.glob(os.path.join(TARGET_DIR, "*.xlsx"))
print(f"Scanning folder... Found {len(files)} files to check.\n")

renamed_count = 0
for fpath in files:
    fname = os.path.basename(fpath)
    
    for old_token, new_token in mapping.items():
        # Handle ActiveFragments files
        if f"_{old_token}_ActiveFragments" in fname:
            new_name = fname.replace(f"_{old_token}_ActiveFragments", f"_{new_token}_ActiveFragments")
            os.rename(fpath, os.path.join(TARGET_DIR, new_name))
            print(f"✓ Renamed: {fname} -> {new_name}")
            renamed_count += 1
            break
        # Handle Calculations files
        elif f"_{old_token}_Calculations" in fname:
            new_name = fname.replace(f"_{old_token}_Calculations", f"_{new_token}_Calculations")
            os.rename(fpath, os.path.join(TARGET_DIR, new_name))
            print(f"✓ Renamed: {fname} -> {new_name}")
            renamed_count += 1
            break

print(f"\nTask complete. Successfully renamed {renamed_count} files.")