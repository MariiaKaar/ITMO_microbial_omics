#!/usr/bin/env python3
"""Step 5: iTOL annotation files (phylum, long/short) and the phylum x type x tetrad table.
long/short is approximated by protein length (< 600 aa = short). Run from the repository root.
"""
import csv, re, random, collections

META = "data/final_meta.tsv"
SHORT_CUTOFF = 600

rows = list(csv.DictReader(open(META), delimiter="\t"))

def phylum(lineage):
    m = re.search(r"([^,]+?) \(phylum\)", lineage)
    return m.group(1).strip() if m else "Unknown"

# --- phylum colour strip ---
random.seed(1)
ph = {r["Entry"]: phylum(r["Taxonomic lineage"]) for r in rows}
uniq = sorted(set(ph.values()))
colors = {p: "#%06x" % random.randint(0x303030, 0xE0E0E0) for p in uniq}
with open("results/tree/itol_phylum.txt", "w") as out:
    out.write("DATASET_COLORSTRIP\nSEPARATOR TAB\nDATASET_LABEL\tPhylum\nCOLOR\t#ff0000\n"
              "LEGEND_TITLE\tPhylum\nLEGEND_SHAPES\t" + "\t".join("1" for _ in uniq) + "\n"
              "LEGEND_COLORS\t" + "\t".join(colors[p] for p in uniq) + "\n"
              "LEGEND_LABELS\t" + "\t".join(uniq) + "\nDATA\n")
    for acc, p in ph.items():
        out.write(f"{acc}\t{colors[p]}\t{p}\n")

# --- long/short colour strip ---
typ = {r["Entry"]: ("short" if int(r["Length"]) < SHORT_CUTOFF else "long") for r in rows}
with open("results/tree/itol_type.txt", "w") as out:
    out.write("DATASET_COLORSTRIP\nSEPARATOR TAB\nDATASET_LABEL\tpAgo type\nCOLOR\t#000000\n"
              "LEGEND_TITLE\tpAgo type\nLEGEND_SHAPES\t1\t1\nLEGEND_COLORS\t#1f77b4\t#ff7f0e\n"
              "LEGEND_LABELS\tlong\tshort\nDATA\n")
    for acc, t in typ.items():
        out.write(f"{acc}\t{'#ff7f0e' if t == 'short' else '#1f77b4'}\t{t}\n")

# --- phylum x type x tetrad table ---
tet = {l.split("\t")[0]: l.split("\t")[5] for l in open("results/tetrad.tsv").read().splitlines()[1:]}
c = collections.Counter((ph[a], typ[a], tet.get(a, "NA")) for a in ph)
with open("results/table_phylum_type_tetrad.tsv", "w") as f:
    f.write("phylum\ttype\ttetrad\tcount\n")
    for k, v in sorted(c.items(), key=lambda x: -x[1]):
        f.write("\t".join(k) + f"\t{v}\n")
print(len(ph), "sequences with taxonomy;", len(uniq), "phyla")
print(collections.Counter(typ.values()))
