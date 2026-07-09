import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from pathlib import Path

# 1. Load your clean dataset containing the SMILES
INPUT_DIR  = Path("/home/maksym/lupinus_analysis/ADMET_inputs")
OUTPUT_DIR = Path("/home/maksym/lupinus_analysis/Docking_inputs")
combined_path = INPUT_DIR / "optimised_peptides_for_admet_metadata.csv"
df = pd.read_csv(combined_path, dtype=str)

# Create an elegant RDKit writer for a 3D Master SDF file
writer = Chem.SDWriter(OUTPUT_DIR / "all_peptides_3D.sdf")

success_count = 0

print("Starting 3D Conformer Generation...")

for idx, row in df.iterrows():
    sequence = row['Sequence']
    smiles = row['smiles']
    
    # Generate molecule object from SMILES
    mol = Chem.MolFromSmiles(smiles)
    
    if mol:
        # A. Explicit Hydrogens are REQUIRED for 3D embedding and docking
        mol = Chem.AddHs(mol)
        
        # B. Generate 3D Coordinates using ETKDG v3 (state-of-the-art for small molecules)
        params = AllChem.ETKDGv3()
        params.randomSeed = 42 # Ensures reproducible shapes
        embed_status = AllChem.EmbedMolecule(mol, params)
        
        if embed_status == 0:  # 0 means successful embedding
            # C. Clean up geometry using MMFF94 force field optimization
            AllChem.MMFFOptimizeMolecule(mol)
            
            # D. Save valuable metadata back into the 3D file
            mol.SetProp("_Name", f"Peptide_{sequence}")
            mol.SetProp("Sequence", str(sequence))
            mol.SetProp("Activity", str(row['Activity']))
            
            # Write to the master 3D file
            writer.write(mol)
            success_count += 1
        else:
            print(f" ✗ Failed to embed 3D coordinates for: {sequence}")
            
writer.close()
print(f"\nFinished! Successfully generated 3D structures for {success_count}/{len(df)} peptides.")
