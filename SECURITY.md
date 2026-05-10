# Security Policy

Musicians Organizer is a local desktop application that scans and manages files selected by the user. Security reports are welcome, especially around file handling, delete behavior, local paths, and dependency/setup risks.

## Supported Scope

Please report issues related to the current `main` branch. Older branches and local development experiments are not separately supported.

## Please Report Privately

Do not open a public issue for vulnerabilities that could expose or destroy user data.

Examples worth reporting privately:

- Unsafe delete, recycle-bin, or duplicate-management behavior
- Path traversal or unintended file access outside the selected library
- Shell/process execution risks
- Local database corruption or unexpected writes outside the configured path
- Dependency or packaging issues that create realistic compromise risk
- Logs, screenshots, or docs that accidentally expose private paths or media metadata

## How To Report

Use a private channel available from the maintainer's GitHub profile or portfolio contact page. Include:

- A short description of the issue
- Steps to reproduce
- Affected operating system and Python version
- Expected impact
- Whether the report includes private paths, media names, or other sensitive local information

Please avoid including real private media files. If a reproduction needs sample files, use synthetic or public-domain test files whenever possible.

## Public Disclosure

Please give the maintainer time to confirm and fix the issue before public disclosure. Once fixed, a short public note or changelog entry may be added when useful.

## Non-Security Bugs

Normal crashes, UI bugs, setup problems, and feature requests can use GitHub Issues.
