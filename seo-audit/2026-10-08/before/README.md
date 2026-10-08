# Immutable baseline files

Generated HTML/discovery snapshots are packaged in `generated-baseline.zip` because the repository ignores directories named `output/`. Extract this archive **inside this before directory** to restore the exact original `output/...` paths named in `sha256.json`. Other hashed files are tracked directly. The archive preserves the original snapshot bytes and the original SHA-256 manifest without modification.

Baseline deployment/build provenance is recorded in provenance.json. Production response snapshots are separate in live/.
