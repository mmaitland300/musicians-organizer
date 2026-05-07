# README Visual Assets

This folder stores the screenshots embedded in the root README.

The screenshots are generated from temporary demo audio and seeded metadata, not
from a private sample library. Regenerate them from the repository root with:

```powershell
.\.venv\Scripts\python.exe scripts\capture_readme_screenshots.py
```

The script opens real Qt widgets, captures PNGs, and discards the temporary audio
fixtures after capture.
