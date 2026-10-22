#!/usr/bin/env python3
"""Step 6: flag candidate horizontal gene transfers.
A leaf is flagged if at least MIN_AGREE of its N_NEIGHBORS nearest leaves (patristic distance)
belong to one other phylum. This is a screening heuristic, NOT proof of HGT.
Run from the repository root.
"""
import csv, re, collections
from Bio import Phylo

N_NEIGHBORS, MIN_AGREE = 5, 4

ph = {}
for r in csv.DictReader(open("data/final_meta.tsv"), delimiter="\t"):
    m = re.search(r"([^,]+?) \(phylum\)", r["Taxonomic lineage"])
    ph[r["Entry"]] = m.group(1).strip() if m else "Unknown"

t = Phylo.read("results/tree/pago.treefile", "newick")
leaves = [l for l in t.get_terminals() if l.name in ph]

out = []
for a in leaves:
    d = sorted((t.distance(a, b), b.name) for b in leaves if b is not a)[:N_NEIGHBORS]
    nb = [ph[n] for _, n in d]
    maj, cnt = collections.Counter(nb).most_common(1)[0]
    if maj != ph[a.name] and cnt >= MIN_AGREE:
        out.append((a.name, ph[a.name], maj, cnt))

with open("results/hgt_candidates.tsv", "w") as f:
    f.write("leaf\town_phylum\tneighbors_phylum\tn_of_5\n")
    for o in out:
        f.write("\t".join(map(str, o)) + "\n")
print(len(out), "candidates")
for o in out:
    print(*o, sep="\t")
