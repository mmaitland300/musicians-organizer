# Roadmap

This roadmap keeps the public direction realistic. Musicians Organizer is a local-first desktop app for managing audio libraries, not a cloud cataloging service or a general DAW automation platform.

## Current Focus

- Keep setup reproducible with direct runtime/dev dependency files and constraints.
- Improve confidence around scanning, database updates, duplicate review, and feature extraction.
- Make the README and screenshots accurately show the current desktop workflow.
- Preserve safe local behavior around file paths, delete flows, and user media.

## Near-Term Work

- Add clearer progress/error feedback for long scans and analysis jobs.
- Expand tests around duplicate handling, filtering, tagging, and similarity queries.
- Improve documentation for database path configuration and migration behavior.
- Continue reducing scoped flake8 lint debt without mixing it into feature changes.
- Document more manual UI workflows with screenshots where helpful.

## Packaging And Distribution

- Explore a repeatable packaging path for non-developer users.
- Document platform-specific setup issues for PyQt5, audio backends, and scientific packages.
- Keep installer/build artifacts out of git unless there is a deliberate release process.

## Audio Workflow Improvements

- Improve metadata quality checks for key, BPM, tags, and extracted features.
- Make heuristic auto-tagging limits clearer in the UI and docs.
- Refine similarity recommendations using available feature coverage.
- Keep "Send to Cubase" narrow and explicit unless a broader integration is designed separately.

## Not Planned Right Now

- Cloud sync or hosted multi-user library management
- Uploading user audio libraries to the repository or a service
- Broad DAW automation beyond the current Cubase-oriented path
- Replacing manual review with fully trusted auto-tagging

## Contribution Fit

Issues and pull requests are most useful when they are small, reproducible, and tied to the existing local desktop workflow. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and verification steps.
