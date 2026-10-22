# data/

Raw and intermediate files are not stored in the repository (see `.gitignore`).
Regenerate them with `scripts/01_download_data.sh` and `scripts/02_clean_and_cluster.sh`.

Files created there:

| File | Content |
|---|---|
| `prok_piwi_raw.fasta`, `prok_piwi_meta.tsv` | UniProt download (Piwi domain PF02171, Bacteria + Archaea) and its metadata |
| `ref_pago.fasta`, `ttago.fasta` | Reference pAgo (TtAgo Q746M7, PfAgo Q8U3D2); TtAgo is the numbering ruler |
| `all_cdhit70.fasta` | **Final dataset** after filtering and CD-HIT clustering at 70% identity (251 sequences) |
| `final_meta.tsv` | Taxonomy and annotation for the final dataset (242 of 251 sequences have UniProt taxonomy) |

Tip: commit `all_cdhit70.fasta` and `final_meta.tsv` after you run the pipeline, so others can
reproduce the tree without re-downloading.
