#!/usr/bin/env bash
# Records the date and tool versions into docs/versions.txt (run after activating the conda env).
cd "$(dirname "$0")/.."
mkdir -p docs
ver() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "== $1"; ( "$1" "$2" 2>&1 || true ) | head -n 2
  else
    echo "== $1: not found"
  fi
}
{
  echo "Date: $(date -I)"
  ver seqkit version
  ver cd-hit -h
  ver mafft --version
  ver trimal --version
  ver iqtree2 --version
  ver FastTree -help
  python3 -c "import Bio; print('== biopython', Bio.__version__)"
} > docs/versions.txt
cat docs/versions.txt
