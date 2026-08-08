# RobertDeVore.com

Robert DeVore's personal publishing site, built with [Kujo SSG](https://github.com/kujolang/ssg) and [SiteKit](https://github.com/kujolang/site-kit).

Current site release: **v1.0.1**.

## Local build

The pinned local workspace is recorded in [workspace-dependencies.json](workspace-dependencies.json). Its paths are relative to this repository; set `KUJO_ROOT`, `SSG_ROOT`, or `SITEKIT_ROOT` when the repositories live elsewhere. Overrides must be at the pinned revisions so a build remains reproducible.

```bash
python3 -m pip install -r requirements.txt
python3 scripts/workspace.py doctor --json
./scripts/sync_dependencies.sh --check
python3 scripts/bundle_css.py --check
./scripts/build.sh
python3 scripts/validate_site.py output
python3 -m http.server 4173 --bind 127.0.0.1 --directory output
```

`./scripts/sync_dependencies.sh --dry-run` lists its pinned writes without changing files. Run the command with no arguments to update the vendored SSG/SiteKit artifacts, then use `--check` to verify their hashes. `scripts/build.sh` resolves the pinned Kujo binary through the manifest and refuses to build if the runtime revision does not match.

Pushes to `main` deploy through [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml). The workflow builds the pinned Kujo runtime, generates and validates `output/`, and publishes that artifact directly to GitHub Pages without Jekyll.

Authored sources live in `content/`, `templates/`, and `assets/`. `output/` is generated and must not be edited or committed. Dependency distribution files are intentionally synced into `assets/css/sitekit/`, `assets/fonts/`, and `build.kujo` so the published site remains self-contained.

The release stylesheet at `assets/css/site.bundle.css` combines the pinned SiteKit layers and `assets/css/site.css` into one request. The generated `assets/css/site.critical.css` keeps the initial viewport styled while that complete bundle loads asynchronously. After changing CSS or `VERSION`, regenerate both with `python3 scripts/bundle_css.py`; builds reject stale bundles and inject the critical CSS into generated HTML.

See [docs/dependencies.md](docs/dependencies.md), [docs/architecture.md](docs/architecture.md), [docs/content-migration.csv](docs/content-migration.csv), and [docs/verification.md](docs/verification.md).
