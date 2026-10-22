#!/usr/bin/env bash
# Step 3: alignment, trimming, ML tree (IQ-TREE), midpoint rooting, TtAgo added to the raw alignment.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results/aln results/tree
IQTREE="${IQTREE:-iqtree2}"   # name of the IQ-TREE binary (iqtree, iqtree2 or iqtree3)
THREADS="${THREADS:-4}"

mafft --auto --thread "$THREADS" --reorder data/all_cdhit70.fasta > results/aln/aln_raw.fasta

trimal -in results/aln/aln_raw.fasta -out results/aln/aln_trim.fasta -automated1 \
  -htmlout results/aln/trim_report.html
trimal -in results/aln/aln_trim.fasta -out results/aln/aln_final.fasta -resoverlap 0.5 -seqoverlap 50

seqkit stats results/aln/aln_raw.fasta results/aln/aln_trim.fasta results/aln/aln_final.fasta

# ML tree: ModelFinder restricted to a few protein models, 1000 UFBoot + 1000 SH-aLRT
"$IQTREE" -s results/aln/aln_final.fasta \
  -m MFP -mset LG,WAG,JTT,Q.pfam \
  -B 1000 -alrt 1000 -bnni \
  -T AUTO --threads-max "$THREADS" \
  --prefix results/tree/pago
grep "Best-fit model" results/tree/pago.iqtree

# no outgroup -> midpoint rooting
python3 - <<'PY'
from Bio import Phylo
t = Phylo.read("results/tree/pago.treefile", "newick")
t.root_at_midpoint()
Phylo.write(t, "results/tree/pago_midpoint.nwk", "newick")
PY

# add TtAgo to the RAW alignment (without --keeplength, which would delete TtAgo residues)
mafft --addfull data/ttago.fasta --thread "$THREADS" \
  results/aln/aln_raw.fasta > results/aln/aln_raw_withTt.fasta
