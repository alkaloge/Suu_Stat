#!/bin/bash

# List of years to clean and copy
years=("UL2018" "UL2017" "UL2016" "UL2016APV")
dir="/uscms_data/d3/alkaloge/MetStudies/nAOD/Suu/new/SuuToTU_TToBLNu_SUNY"

# Remove existing directories
for year in "${years[@]}"; do
    rm -fr "$year"
done

# Copy each directory from source
for year in "${years[@]}"; do
    echo "Copying $year"
    cp -r "${dir}/${year}" .
done





