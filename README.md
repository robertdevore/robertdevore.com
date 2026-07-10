# RobertDeVore.com

Robert DeVore's personal publishing site, built with [Kujo SSG](https://github.com/kujolang/ssg) and [SiteKit](https://github.com/kujolang/site-kit).

```bash
./scripts/sync_dependencies.sh
./scripts/build.sh
python3 scripts/validate_site.py output
python3 -m http.server 4173 --bind 127.0.0.1 --directory output
```

Authored sources live in `content/`, `templates/`, and `assets/`. `output/` is generated and must not be edited or committed. Dependency distribution files are intentionally synced into `assets/css/sitekit/`, `assets/fonts/`, and `build.kujo` so the published site remains self-contained.

See [docs/architecture.md](docs/architecture.md), [docs/content-migration.csv](docs/content-migration.csv), and [docs/verification.md](docs/verification.md).
