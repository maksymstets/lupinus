import pandas as pd

from pathlib import Path

import re


# ── Configuration ─────────────────────────────────────────────────────────────

INPUT_DIR = Path("/home/maksym/lupinus_analysis/BIOPEP_results/BIOPEP_Batch_Outputs_Combined")


# Expected data columns starting at row 4 (0-indexed row 3)

DATA_COLUMNS = [

    "NO", "Peptide ID", "Sequence", "Location",

    "Name", "Function", "Activity", "Monoisotopic mass", "Chemical mass"

]



def extract_protein_name(filename: str) -> str:

    """

    Extract protein name from filename — two patterns:


    Pattern A (enzyme-specific):

        cong_beta_1_1_11___chymotrypsin_(A)___EC_3.4.21.1_ActiveFragments.xlsx

        → protein = everything before '___', i.e. 'cong_beta_1_1_11'

        


    Pattern B (GID):

        cong_beta_1_1_GID_ActiveFragments.xlsx

        → strip '_GID_ActiveFragments' → 'cong_beta_1_1'

    """

    stem = Path(filename).stem   # drop .xlsx


    # Pattern B: Simultaneous files

    if "_GID_ActiveFragments" in stem:

        return stem.replace("_GID_ActiveFragments", "")


    # Pattern A: enzyme-specific files (contain '___')

    if "___" in stem:

        protein = stem.split("___")[0]          # e.g. 'cong_beta_1_1_11'

        # Strip the trailing numeric enzyme-ID suffix (_<digits> at the end)

        protein = re.sub(r"_\d+$", "", protein)  # → 'cong_beta_1_1'

        return protein


    # Fallback: strip known suffixes

    stem = re.sub(r"_ActiveFragments$", "", stem)

    return stem

def parse_single_file(filepath: Path) -> pd.DataFrame:
    """
    Parse one BIOPEP ActiveFragments Excel file and return a clean DataFrame.
    """
    # Read everything as raw strings so we can inspect header rows safely
    raw = pd.read_excel(filepath, header=None, dtype=str)

    # ── Extract Enzyme ID from row 3 (0-indexed row 2) ───────────────────────
    enzyme_id = None
    for row_idx in range(min(5, len(raw))):
        row_vals = raw.iloc[row_idx].dropna().tolist()
        row_str  = " ".join(str(v) for v in row_vals).lower()
        if "enzyme" in row_str and "id" in row_str:
            for col_idx, val in enumerate(raw.iloc[row_idx]):
                if pd.notna(val) and "enzyme" not in str(val).lower():
                    enzyme_id = str(val).strip()
                    break
            break

    if enzyme_id is None:
        stem = filepath.stem
        if "_GID_ActiveFragments" in stem:
            enzyme_id = "GID"
        elif "___" in stem:
            parts = stem.split("___")
            num_match = re.search(r"_(\d+)$", parts[0])
            num_prefix = num_match.group(1) + "|" if num_match else ""
            enzyme_name = parts[1].replace("_", " ").strip() if len(parts) > 1 else ""
            ec_part     = parts[2].split("_Active")[0].replace("_", ".").strip() if len(parts) > 2 else ""
            enzyme_id   = f"{num_prefix}{enzyme_name}|{ec_part}"
        else:
            enzyme_id = "unknown"

    # ── Find the data header row (the row containing "NO") ───────────────────
    header_row_idx = None
    for row_idx in range(len(raw)):
        first_cell = str(raw.iloc[row_idx, 0]).strip()
        if first_cell == "NO":
            header_row_idx = row_idx
            break

    if header_row_idx is None:
        raise ValueError(f"Could not find data header row in {filepath.name}")

    # ── READ ACTUAL DATA WITH THE NA-FIX APPLIED ────────────────────────────
    data_df = pd.read_excel(
        filepath,
        header=header_row_idx,     
        dtype=str,
        keep_default_na=False      # <--- ADD THIS LINE HERE
    )

    # Keep only the expected columns (ignore any extras / unnamed cols)
    existing_cols = [c for c in DATA_COLUMNS if c in data_df.columns]
    data_df = data_df[existing_cols].copy()

    # Drop completely empty rows
    data_df.dropna(how="all", inplace=True)
    data_df.reset_index(drop=True, inplace=True)

    # ── Add Protein name, Enzyme ID and source file columns on the left ─────────
    protein_name = extract_protein_name(filepath.name)
    data_df.insert(0, "Protein name", protein_name)
    data_df.insert(1, "Enzyme ID",    enzyme_id)
    data_df.insert(2, "Source file",  filepath.name)

    return data_df


def natural_sort_key(path: Path) -> list:

    """Sort key that orders numbers numerically, not alphabetically.

    e.g. cong_beta_1_1, cong_beta_1_2, ..., cong_beta_1_11  (not _1, _11, _2)

    """

    return [int(c) if c.isdigit() else c.lower()

            for c in re.split(r"(\d+)", path.name)]



def parse_all_files(input_dir: Path) -> pd.DataFrame:

    """

    Iterate over all *_ActiveFragments.xlsx files, parse each, concatenate.

    """

    files = sorted(input_dir.glob("*_ActiveFragments.xlsx"), key=natural_sort_key)

    if not files:

        raise FileNotFoundError(

            f"No *_ActiveFragments.xlsx files found in {input_dir}"

        )


    frames = []

    for fp in files:

        try:

            df = parse_single_file(fp)

            frames.append(df)

            print(f"  ✓  {fp.name}  →  {len(df)} rows")

        except Exception as e:

            print(f"  ✗  {fp.name}  →  ERROR: {e}")


    if not frames:

        raise RuntimeError("No files were successfully parsed.")


    combined = pd.concat(frames, ignore_index=True)


  

    mask = combined["Source file"].str.contains("GID", case=False, na=False)

    combined.loc[mask, "Enzyme ID"] = "GID"


    return combined



# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print(f"Scanning: {INPUT_DIR}\n")

    df = parse_all_files(INPUT_DIR)


    print(f"\nFinal DataFrame shape: {df.shape}")

    print(df.head(10).to_string())


    # Optional: save combined result

    out_path = Path("/home/maksym/lupinus_analysis/BIOPEP_results/combined_active_fragments.xlsx")

    df.to_excel(out_path, index=False)

    print(f"\nSaved → {out_path}") 
