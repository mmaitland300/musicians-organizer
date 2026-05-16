# Contributing

Thanks for taking a look at Musicians Organizer. This is a personal desktop app project, but focused bug reports, docs improvements, small workflow fixes, and platform notes are welcome.

## Good First Contributions

- Reproducible bug reports with OS, Python version, and steps
- Docs fixes for setup, screenshots, or workflow descriptions
- Small tests around scanning, filtering, duplicate detection, or database behavior
- Platform compatibility notes for Windows, macOS, or Linux
- Narrow UI polish that does not rewrite the main workflow

Please avoid broad rewrites, new product directions, or DAW integrations without opening an issue first. The app is intentionally local-first and focused on sample-library organization.

## Local Setup

Target runtime is Python 3.11. CI currently checks Python 3.10 and 3.11.

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the app from the repository root:

```bash
python main.py
```

## Verification

Before opening a pull request, run the same blocking checks used by CI:

```bash
python -m black --check .
python -m isort --check-only .
python -m flake8 config services models utils main.py
python -m mypy .
python -m pytest -q --maxfail=1 --disable-warnings
```

Flake8 is currently scoped to maintained core modules. The scoped check is
blocking in CI.

If your change touches UI behavior, please also describe the manual flow you tested. Screenshots are helpful for visual changes.

## Dependency Policy

- Keep direct runtime dependencies in `requirements.txt`.
- Keep development and CI tools in `requirements-dev.txt`.
- Keep known-good transitive pins in `constraints.txt`.
- Do not add generated media, local databases, local project plans, or personal sample files to the repository.

## Pull Request Guidelines

- Keep changes focused and reviewable.
- Include what changed, why it changed, and how you tested it.
- Preserve local-first behavior; media files should remain on the user's machine.
- Avoid changing migration history after it has been published.
- Do not include private file paths, audio libraries, customer/client material, or API keys.

## Issue Reports

For bugs, include:

- Operating system and version
- Python version
- Install method and dependency command used
- Steps to reproduce
- Expected behavior
- Actual behavior
- Any relevant traceback or log snippet

For security-sensitive reports, use [SECURITY.md](SECURITY.md) instead of opening a public issue.
