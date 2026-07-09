#!/bin/bash

# Define where everything lives
PEPTIDES_DIR="/home/maksym/biopep-automation/Excel tables results/sorted_peptides"
RESULTS_DIR="/home/maksym/biopep-automation/docking_results"

CONFIG_ACE="/home/maksym/biopep-automation/config_ACE.txt"
CONFIG_DPP="/home/maksym/biopep-automation/config_DPP.txt"

# Create clean output folders for the results
mkdir -p "$RESULTS_DIR/ACE_results"
mkdir -p "$RESULTS_DIR/DPP_results"

# Function to run Vina and keep the terminal clean
run_vina() {
    local ligand="$1"
    local config="$2"
    local out_dir="$3"
    local base_name=$(basename "$ligand" .pdbqt)
    
    echo "Running Vina for: $base_name"
    vina --config "$config" --ligand "$ligand" --out "$out_dir/${base_name}_out.pdbqt" > "$out_dir/${base_name}_log.txt"
}

echo "--- STARTING DOCKING PIPELINE ---"

# 1. ACE Only
echo "Processing ACE_only folder (50 files)..."
for pep in "$PEPTIDES_DIR/ACE_only"/*.pdbqt; do
    [ -e "$pep" ] && run_vina "$pep" "$CONFIG_ACE" "$RESULTS_DIR/ACE_results"
done

# 2. DPP Only
echo "Processing DPP_only folder (86 files)..."
for pep in "$PEPTIDES_DIR/DPP_only"/*.pdbqt; do
    [ -e "$pep" ] && run_vina "$pep" "$CONFIG_DPP" "$RESULTS_DIR/DPP_results"
done

# 3. Dual Activity (Docks against BOTH enzymes)
echo "Processing Dual_activity folder (69 files x 2 targets)..."
for pep in "$PEPTIDES_DIR/Dual_activity"/*.pdbqt; do
    if [ -e "$pep" ]; then
        echo "--> Dual docking for $(basename "$pep" .pdbqt)"
        run_vina "$pep" "$CONFIG_ACE" "$RESULTS_DIR/ACE_results"
        run_vina "$pep" "$CONFIG_DPP" "$RESULTS_DIR/DPP_results"
    fi
done

echo "--- ALL 274 DOCKING SIMULATIONS COMPLETE! ---"
echo "Check $RESULTS_DIR for your output poses and energy logs."
