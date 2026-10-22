#!/usr/bin/env bash
# Step 1: download sequences and metadata from the UniProt REST API.
# Run from anywhere; paths are relative to the repository root.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data results/aln results/tree

# Prokaryotic Piwi-domain proteins (Pfam PF02171), Bacteria (2) + Archaea (2157)
Q='(xref:pfam-PF02171) AND (taxonomy_id:2 OR taxonomy_id:2157) AND (length:[400 TO 1500]) AND (fragment:false)'

curl -G "https://rest.uniprot.org/uniprotkb/stream" \
  --data-urlencode "query=${Q}" --data-urlencode "format=fasta" \
  -o data/prok_piwi_raw.fasta

curl -G "https://rest.uniprot.org/uniprotkb/stream" \
  --data-urlencode "query=${Q}" --data-urlencode "format=tsv" \
  --data-urlencode "fields=accession,id,protein_name,organism_name,organism_id,length,lineage,reviewed" \
  -o data/prok_piwi_meta.tsv

# Reference pAgo: TtAgo (Q746M7, Thermus thermophilus, 685 aa, PDB 3DLH) and PfAgo (Q8U3D2)
for acc in Q746M7 Q8U3D2; do
  curl -s "https://rest.uniprot.org/uniprotkb/${acc}.fasta"
done > data/ref_pago.fasta

# Optional: eukaryotic AGO as a candidate outgroup (they were NOT present in the final tree;
# the published tree is midpoint-rooted). Set INCLUDE_EUK=0 to skip.
if [ "${INCLUDE_EUK:-1}" = "1" ]; then
  curl -G "https://rest.uniprot.org/uniprotkb/stream" \
    --data-urlencode "query=(xref:pfam-PF02171) AND (taxonomy_id:2759) AND (reviewed:true) AND (length:[700 TO 1200])" \
    --data-urlencode "format=fasta" -o data/euk_ago_all.fasta
  seqkit sample -n 8 -s 42 data/euk_ago_all.fasta -o data/euk_ago_sub.fasta
else
  : > data/euk_ago_sub.fasta
fi

seqkit stats data/*.fasta
