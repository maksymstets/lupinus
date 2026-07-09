import pandas as pd
from pathlib import Path

# ── Configuration ─────────────────────────────────────────────────────────────
# Path to the combined active fragments file
COMBINED_FRAGMENTS_PATH = Path("/home/maksym/lupinus_analysis/ADMET_results/GID_ADMET_combined_active_fragments.xlsx")
TOTAL_DENOMINATOR = 71

# 1. Load the dataset
print(f"Loading data from {COMBINED_FRAGMENTS_PATH.name}...")
if not COMBINED_FRAGMENTS_PATH.exists():
    raise FileNotFoundError(f"Could not find the file: {COMBINED_FRAGMENTS_PATH}")

df = pd.read_excel(COMBINED_FRAGMENTS_PATH, dtype=str)

# 2. Standardize string case and clear missing values
df['Sequence'] = df['Sequence'].fillna('').astype(str).str.upper().str.strip()
df['Protein name'] = df['Protein name'].fillna('').astype(str).str.upper().str.strip()

# 3. Apply the containment condition
# This checks if the 'Protein name' string is completely found within the 'Sequence' string.
# Example: Protein name = "VPF", Sequence = "VPF" -> True (Good)
# Example: Protein name = "VPF", Sequence = "VP"  -> False (Not good)
def check_containment(row):
    protein = row['Protein name']
    sequence = row['Sequence']
    if not protein or not sequence:
        return False
    return protein in sequence

df['Is_Match'] = df.apply(check_containment, axis=1)

# 4. Filter for entries that satisfy the condition
df_matches = df[df['Is_Match'] == True]

# 5. Keep only the UNIQUE sequences from the matching entries
unique_matching_sequences = df_matches['Sequence'].unique()
count_unique_matches = len(unique_matching_sequences)

# 6. Calculate percentage relative to the total of 71
percentage = (count_unique_matches / TOTAL_DENOMINATOR) * 100

# ── Display Results Summary ───────────────────────────────────────────────────
print("\n==================================================")
print("             MATCHING ANALYSIS REPORT             ")
print("==================================================")
print(f"Target Total Denominator:     {TOTAL_DENOMINATOR}")
print(f"Unique Matching Sequences:    {count_unique_matches}")
print(f"Percentage of Target Total:   {percentage:.2f}%")
print("==================================================\n")

print("List of Unique Matching Sequences:")
if count_unique_matches > 0:
    for idx, seq in enumerate(sorted(unique_matching_sequences), 1):
        print(f"  {idx}. {seq}")
else:
    print("  No sequences matched the containment criteria.")