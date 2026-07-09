import os
from pathlib import Path
from rdkit import Chem
from meeko import MoleculePreparation

# --- Paths ---

INPUT_FILE  = Path("/home/maksym/lupinus_analysis/Docking_inputs/all_peptides_3D.sdf")  
OUTPUT_DIR  = Path("/home/maksym/lupinus_analysis/DOcking_inputs/prepared_peptides_pdbqt")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Load input ---
supplier = Chem.SDMolSupplier(str(INPUT_FILE), removeHs=False)

preparer = MoleculePreparation()
success_count = 0

print("Beginning batch preparation of peptides...")

for mol in supplier:
    if mol is None:
        continue

    seq_name = mol.GetProp("_Name")

    try:
        preparer.prepare(mol)
        pdbqt_string = preparer.write_pdbqt_string()

        output_filename = OUTPUT_DIR / f"{seq_name}.pdbqt"
        with open(output_filename, "w") as f:
            f.write(pdbqt_string)

        success_count += 1

    except Exception as e:
        print(f" ✗ Error preparing {seq_name}: {e}")

print(f"\nDone! Prepared {success_count} peptides as .pdbqt files in '{OUTPUT_DIR}/'")
