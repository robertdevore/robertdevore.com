# RobertDeVore.com

Robert DeVore's personal publishing site, built with [Kujo SSG](https://github.com/kujolang/ssg) and [SiteKit](https://github.com/kujolang/site-kit).

## Local build

The pinned local workspace is recorded in [workspace-dependencies.json](workspace-dependencies.json). Its paths are relative to this repository; set `KUJO_ROOT`, `SSG_ROOT`, or `SITEKIT_ROOT` when the repositories live elsewhere. Overrides must be at the pinned revisions so a build remains reproducible.

```bash
python3 -m pip install -r requirements.txt
python3 scripts/workspace.py doctor --json
./scripts/sync_dependencies.sh --check
./scripts/build.sh
python3 scripts/validate_site.py output
python3 -m http.server 4173 --bind 127.0.0.1 --directory output
```

`./scripts/sync_dependencies.sh --dry-run` lists its pinned writes without changing files. Run the command with no arguments to update the vendored SSG/SiteKit artifacts, then use `--check` to verify their hashes. `scripts/build.sh` resolves the pinned Kujo binary through the manifest and refuses to build if the runtime revision does not match.

Authored sources live in `content/`, `templates/`, and `assets/`. `output/` is generated and must not be edited or committed. Dependency distribution files are intentionally synced into `assets/css/sitekit/`, `assets/fonts/`, and `build.kujo` so the published site remains self-contained.

See [docs/dependencies.md](docs/dependencies.md), [docs/architecture.md](docs/architecture.md), [docs/content-migration.csv](docs/content-migration.csv), and [docs/verification.md](docs/verification.md).
