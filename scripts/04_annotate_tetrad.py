#!/usr/bin/env python3
"""Step 4: read the DEDX catalytic tetrad from the alignment.

TtAgo (Q746M7) is the numbering ruler: D478, E512, D546, D660.
Status:
  active    - D, E, D at the first three positions and D/H/N/K at the fourth
  inactive  - tetrad region present but at least one position differs
  no_region - a gap at one of the four positions (typically short pAgo / fragments)
Run from the repository root.
"""
import sys
from collections import Counter
from Bio import SeqIO

ALN = "results/aln/aln_raw_withTt.fasta"
REF = "Q746M7"
TARGETS = {478: "D", 512: "E", 546: "D", 660: "D"}

aln = {r.id.split("|")[0]: str(r.seq) for r in SeqIO.parse(ALN, "fasta")}
ref = aln[REF]

cols, pos = {}, 0
for i, a in enumerate(ref):
    if a != "-":
        pos += 1
        if pos in TARGETS:
            cols[pos] = i

# sanity check: the ruler itself must carry D, E, D, D
bad = [p for p in TARGETS if ref[cols[p]] != TARGETS[p]]
for p in sorted(cols):
    print(f"TtAgo position {p}: {ref[cols[p]]} (expected {TARGETS[p]})")
if bad:
    sys.exit("TtAgo check FAILED - wrong accession or numbering; stopping.")

order = sorted(cols)
colors = {"active": "#2ca02c", "inactive": "#d62728", "no_region": "#bbbbbb"}
rows = []
for sid, s in aln.items():
    if sid == REF:
        continue
    res = [s[cols[p]] for p in order]
    if "-" in res:
        status = "no_region"
    elif res[0] == "D" and res[1] == "E" and res[2] == "D" and res[3] in "DHNK":
        status = "active"
    else:
        status = "inactive"
    rows.append((sid, res, status))

with open("results/tetrad.tsv", "w") as f:
    f.write("id\tD1\tE\tD2\tD3\tstatus\n")
    for sid, res, st in rows:
        f.write(f"{sid}\t" + "\t".join(res) + f"\t{st}\n")

with open("results/tree/itol_tetrad.txt", "w") as out:
    out.write("DATASET_COLORSTRIP\nSEPARATOR TAB\nDATASET_LABEL\tCatalytic tetrad\nCOLOR\t#000000\n"
              "LEGEND_TITLE\tCatalytic tetrad\nLEGEND_SHAPES\t1\t1\t1\n"
              "LEGEND_COLORS\t#2ca02c\t#d62728\t#bbbbbb\nLEGEND_LABELS\tactive\tinactive\tno region\nDATA\n")
    for sid, res, st in rows:
        out.write(f"{sid}\t{colors[st]}\t{st}\n")

print(Counter(st for _, _, st in rows))
