# Repository instructions

Keep the website build portable. Do not add absolute machine paths to scripts or documentation. Resolve Kujo, SSG, and SiteKit through `workspace-dependencies.json`; use the documented environment variables only for a differently located checkout at the pinned revision.

Before changing vendored build or design-system artifacts, run `./scripts/sync_dependencies.sh --dry-run`. After a deliberate sync, run `./scripts/sync_dependencies.sh --check`, `./scripts/build.sh`, and `python3 scripts/validate_site.py output`.

`output/` is generated and must not be committed. Python site tooling requires the pinned dependency in `requirements.txt`.
