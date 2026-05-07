"""Capture README screenshots from real Qt widgets with generated demo data."""

from __future__ import annotations

import datetime as dt
import logging
import math
import sys
import tempfile
from pathlib import Path
from typing import Any, cast

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
logging.disable(logging.INFO)

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
from PyQt5 import QtCore, QtGui, QtWidgets  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402

from services.database_manager import DatabaseManager  # noqa: E402
from services.schema import metadata  # noqa: E402
from ui.dialogs.duplicate_manager_dialog import DuplicateManagerDialog  # noqa: E402
from ui.dialogs.feature_view_dialog import FeatureViewDialog  # noqa: E402
from ui.dialogs.spectrogram_dialog import SpectrogramDialog  # noqa: E402
from ui.main_window import MainWindow  # noqa: E402

OUTPUT_DIR = Path("docs/readme")
SAMPLE_RATE = 44_100


def _write_demo_tone(path: Path, frequency: float, seconds: float = 1.0) -> None:
    """Write a tiny stereo tone so plot dialogs render real audio content."""
    samples = int(SAMPLE_RATE * seconds)
    timeline = np.linspace(0, seconds, samples, endpoint=False)
    envelope = np.exp(-4 * timeline)
    signal = 0.35 * np.sin(2 * math.pi * frequency * timeline) * envelope
    stereo = np.column_stack([signal, signal])
    sf.write(path, stereo, SAMPLE_RATE)


def _demo_records(audio_dir: Path) -> list[dict[str, Any]]:
    names = [
        ("Kick_124_C_punchy_loop.wav", 62.0, 124, "C", "KICK", "PUNCHY", False),
        ("Snare_124_C_crisp_oneshot.wav", 185.0, 124, "C", "SNARE", "CRISP", True),
        ("Hat_124_C_bright_loop.wav", 420.0, 124, "C", "HAT", "BRIGHT", False),
        ("Kick_124_C_punchy_loop_copy.wav", 62.0, 124, "C", "KICK", "PUNCHY", False),
        ("Bass_096_Am_warm_loop.wav", 110.0, 96, "Am", "BASS", "WARM", False),
        ("Vocal_100_G_dry_phrase.wav", 310.0, 100, "G", "VOCAL", "DRY", True),
    ]

    records: list[dict[str, Any]] = []
    base_time = dt.datetime(2026, 5, 7, 14, 30)
    for index, (name, freq, bpm, key, instrument, character, used) in enumerate(names):
        path = audio_dir / name
        _write_demo_tone(path, freq)
        hash_value = (
            "demo-duplicate-hash-kick"
            if name.startswith("Kick_124_C_punchy")
            else f"demo-hash-{index}"
        )
        record = {
            "path": str(path),
            "size": path.stat().st_size,
            "mod_time": base_time + dt.timedelta(minutes=index * 7),
            "duration": 1.0,
            "bpm": bpm,
            "key": key,
            "used": used,
            "samplerate": SAMPLE_RATE,
            "channels": 2,
            "tags": {
                "instrument": [instrument],
                "type": ["LOOP" if "loop" in name.lower() else "ONE-SHOT"],
                "character": [character],
            },
            "hash": hash_value,
            "brightness": 1700.0 + index * 125.0,
            "loudness_rms": 0.18 + index * 0.015,
            "zcr_mean": 0.04 + index * 0.006,
            "spectral_contrast_mean": 19.0 + index,
            "bit_depth": 24,
            "loudness_lufs": -13.5 - index,
            "pitch_hz": freq,
            "attack_time": 0.012 + index * 0.004,
        }
        for mfcc_index in range(1, 14):
            record[f"mfcc{mfcc_index}_mean"] = round(
                (index + 1) * 0.1 + mfcc_index * 0.03,
                4,
            )
        records.append(record)
    return records


def _process_events(app: QtWidgets.QApplication, wait_ms: int = 150) -> None:
    app.processEvents()
    QtCore.QThread.msleep(wait_ms)
    app.processEvents(QtCore.QEventLoop.AllEvents, wait_ms)


def _save_widget(
    app: QtWidgets.QApplication,
    widget: QtWidgets.QWidget,
    output_path: Path,
) -> None:
    widget.show()
    widget.raise_()
    _process_events(app)
    widget.repaint()
    _process_events(app)
    pixmap = QtGui.QPixmap(widget.size())
    pixmap.fill(QtGui.QColor("white"))
    widget.render(pixmap)
    if pixmap.isNull():
        raise RuntimeError(f"Could not capture screenshot for {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not pixmap.save(str(output_path)):
        raise RuntimeError(f"Could not save screenshot to {output_path}")


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    app_instance = QtWidgets.QApplication.instance()
    app = (
        cast(QtWidgets.QApplication, app_instance)
        if app_instance is not None
        else QtWidgets.QApplication([])
    )
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Arial", 10))

    with tempfile.TemporaryDirectory(prefix="musicians-organizer-demo-") as tmp:
        audio_dir = Path(tmp) / "Demo Sample Pack"
        audio_dir.mkdir(parents=True)
        records = _demo_records(audio_dir)

        engine = create_engine("sqlite:///:memory:", echo=False)
        metadata.create_all(engine)
        db_manager = DatabaseManager(engine=engine)

        window = MainWindow(db_manager=db_manager)
        window.setTheme("light", save=False)
        window.resize(1280, 820)
        window.onScanFinished(records)
        if window.txtFilter is not None:
            window.txtFilter.setText("kick OR snare")
            window.on_name_filter_apply()
        if window.txtTagTextFilter is not None:
            window.txtTagTextFilter.setText("LOOP")
            window.on_tag_text_filter_apply()
        window.updateSummaryLabel()
        window.tableView.resizeColumnsToContents()
        window.tableView.selectRow(0)
        window.statusBar().showMessage("Demo library loaded from generated fixtures.")
        _save_widget(app, window, OUTPUT_DIR / "library-view.png")

        duplicate_dialog = DuplicateManagerDialog(
            [[records[0], records[3]]],
            size_unit="KB",
            use_recycle_bin=True,
        )
        duplicate_dialog.resize(1000, 520)
        duplicate_dialog.tree.setColumnWidth(0, 520)
        duplicate_dialog.tree.setColumnWidth(1, 100)
        duplicate_dialog.tree.setColumnWidth(2, 180)
        duplicate_dialog.tree.topLevelItem(0).child(1).setCheckState(
            0,
            QtCore.Qt.Checked,
        )
        _save_widget(app, duplicate_dialog, OUTPUT_DIR / "duplicate-manager.png")

        feature_dialog = FeatureViewDialog(records[0])
        feature_dialog.resize(560, 620)
        _save_widget(app, feature_dialog, OUTPUT_DIR / "feature-details.png")

        spectrogram_dialog = SpectrogramDialog(records[0]["path"], theme="light")
        spectrogram_dialog.resize(920, 560)
        _save_widget(app, spectrogram_dialog, OUTPUT_DIR / "spectrogram-view.png")

        window.close()
        duplicate_dialog.close()
        feature_dialog.close()
        spectrogram_dialog.close()
        engine.dispose()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
