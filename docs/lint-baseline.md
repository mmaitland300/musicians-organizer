# Historical Flake8 Baseline Snapshot

This historical baseline captures the state of the scoped CI Flake8 target
before the cleanup passes that made the scoped check blocking in CI.

Current policy is recorded in [lint-execution-policy.md](lint-execution-policy.md).
As of that policy, the scoped command below is expected to pass and CI treats it
as a required check.

## Runtime and Policy

- Local interpreter: `.\.venv\Scripts\python.exe` (Python 3.11.4)
- Scoped command:
  - `.\.venv\Scripts\python.exe -m flake8 config services models utils main.py`
- Flake8 policy source: `.flake8`
  - `max-line-length = 88`
  - `extend-ignore = E203, W503`
- CI matrix note: CI still runs Python 3.10 and 3.11; this baseline is local 3.11.

## Baseline Totals

- Total findings: `149`

### Findings by Code

- `E501`: 149

### Top Files by Count

1. `services/database_manager.py`: 53
2. `models/file_model.py`: 51
3. `services/analysis_engine.py`: 12
4. `services/file_scanner.py`: 8
5. `services/spectrogram_service.py`: 7
6. `services/auto_tagger.py`: 4
7. `services/spectrogram_plotter.py`: 3
8. `config/settings.py`: 3
9. `services/advanced_analysis_worker.py`: 3
10. `services/hash_worker.py`: 2

## Historical Cleanup Notes

- Non-`E501` findings were zero in the scoped command at baseline time.
- Highest-churn files were `services/database_manager.py` and `models/file_model.py`,
  which is why they were split into dedicated cleanup passes.

## Non-E501 Final Pass Check

- Branch: `lint/non-e501-final-pass`
- Command:
  - `.\.venv\Scripts\python.exe -m flake8 config services models utils main.py`
- Result:
  - `NON_E501=0`
