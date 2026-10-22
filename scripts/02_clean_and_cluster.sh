#!/usr/bin/env bash
# Step 2: merge, remove duplicates, filter, shorten IDs, cluster with CD-HIT.
set -euo pipefail
cd "$(dirname "$0")/.."

cat data/prok_piwi_raw.fasta data/ref_pago.fasta data/euk_ago_sub.fasta > data/all_raw.fasta

# identical sequences -> keep one
seqkit rmdup -s data/all_raw.fasta -o data/all_nodup.fasta

# length 400-1500 aa, drop sequences with ambiguous/non-standard residues
seqkit seq -m 400 -M 1500 data/all_nodup.fasta \
  | seqkit grep -s -v -r -p "X|B|Z|U|O" -o data/all_clean.fasta

# keep only the UniProt accession as the sequence ID
seqkit replace -p '^(sp|tr)\|([^|]+)\|(\S+).*' -r '${2}' data/all_clean.fasta -o data/all_clean_ids.fasta

# cluster at 70% identity (-n 5 is required for thresholds 0.7-1.0)
cd-hit -i data/all_clean_ids.fasta -o data/all_cdhit70.fasta -c 0.70 -n 5 -T 4 -M 4000

# final metadata table for the clustered set
seqkit seq -n -i data/all_cdhit70.fasta > data/final_ids.txt
head -1 data/prok_piwi_meta.tsv > data/final_meta.tsv
grep -F -w -f data/final_ids.txt data/prok_piwi_meta.tsv >> data/final_meta.tsv

# TtAgo is used only as a numbering ruler for the catalytic tetrad (step 4)
seqkit grep -r -p "Q746M7" data/ref_pago.fasta \
  | seqkit replace -p '^(sp|tr)\|([^|]+)\|(\S+).*' -r '${2}' > data/ttago.fasta

seqkit stats data/all_clean_ids.fasta data/all_cdhit70.fasta
