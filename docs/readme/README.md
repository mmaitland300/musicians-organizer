# README Visual Assets

This folder stores the screenshots embedded in the root README.

The current README screenshots are curated dark-mode captures from the desktop
UI. They are image-only proof assets; audio files and local media libraries are
not committed.

If manual captures need a safe fixture-based replacement, generate synthetic
screenshots from the repository root with:

```powershell
.\.venv\Scripts\python.exe scripts\capture_readme_screenshots.py
```

The script opens real Qt widgets, captures PNGs under `docs/readme/generated/`,
and discards the temporary audio fixtures after capture.
