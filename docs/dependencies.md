# Workspace dependencies

`workspace-dependencies.json` is the provenance lock for the local Kujo runtime, Kujo SSG source, SiteKit source, and every synced artifact consumed by this site. It records repository URLs, immutable revisions, default paths relative to the site checkout, and SHA-256 hashes before and after the one required SiteKit font-path transformation.

Run the doctor before building or syncing:

```bash
python3 scripts/workspace.py doctor --json
```

It exits non-zero when a required checkout, Git revision, Kujo binary, Python prerequisite, BeautifulSoup install, source artifact, or synced artifact does not match the manifest. The text form is suitable for local diagnosis; `--json` is stable machine-readable output.

The default workspace layout keeps the sibling sources at the relative locations in the manifest. A different layout may set `KUJO_ROOT`, `SSG_ROOT`, and `SITEKIT_ROOT`; the doctor still requires the pinned revision and hashes. `KUJO_BIN` is an optional one-off build override, but it does not change recorded provenance.

## Dependency sync contract

```bash
./scripts/sync_dependencies.sh --dry-run  # validate sources and print planned writes
./scripts/sync_dependencies.sh            # atomically write pinned artifacts
./scripts/sync_dependencies.sh --check    # validate sources and installed artifact hashes
```

The sync implementation uses Python path and file APIs rather than platform-specific `sed -i` behavior. It refuses to copy from a checkout or artifact that differs from the lock. Updating SSG or SiteKit is therefore an intentional lockfile update: review the source revision and each artifact hash, update the manifest, sync, and verify the target build.

## Python validation tools

Both `scripts/validate_site.py` and `scripts/migrate_legacy.py` import BeautifulSoup. Install the exact declared package before running them:

```bash
python3 -m pip install -r requirements.txt
```

The lock records `beautifulsoup4==4.14.3`, the version used for this remediation. A fully hermetic Python wheelhouse is intentionally out of scope; pip resolves its transitive dependencies from the configured package index.
