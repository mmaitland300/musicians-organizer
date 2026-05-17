from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import Mock

from services.database_manager import DatabaseManager
from services.file_scanner import FileScannerService


class FakeCacheManager:
    def __init__(self) -> None:
        self.updated: list[tuple[str, float, int, dict[str, Any]]] = []
        self.flushed = False

    def needs_update(self, file_path: str, mod_time: float, size: int) -> bool:
        return True

    def get(self, file_path: str, mod_time: float, size: int) -> dict[str, Any]:
        return {}

    def update(
        self, file_path: str, mod_time: float, size: int, data: dict[str, Any]
    ) -> None:
        self.updated.append((file_path, mod_time, size, data))

    def flush(self) -> None:
        self.flushed = True


class FakeDatabaseManager:
    def __init__(self, existing_records: list[dict[str, Any]] | None = None) -> None:
        self.engine = object()
        self.existing_records = existing_records or []
        self.folder_queries: list[str] = []
        self.saved_records: list[dict[str, Any]] = []
        self.deleted_paths: list[str] = []

    def get_files_in_folder(self, folder_path: str) -> list[dict[str, Any]]:
        self.folder_queries.append(folder_path)
        return self.existing_records

    def save_file_records(self, records: list[dict[str, Any]]) -> None:
        self.saved_records.extend(records)

    def delete_file_record(self, file_path: str) -> None:
        self.deleted_paths.append(file_path)


def test_scan_collects_audio_metadata_and_saves_new_records(
    tmp_path: Path, monkeypatch
) -> None:
    audio_path = tmp_path / "sample.wav"
    audio_path.write_bytes(b"\x00" * 1024)

    cache = FakeCacheManager()
    monkeypatch.setattr("services.file_scanner.CacheManager", lambda: cache)

    tag = SimpleNamespace(duration=100.0, samplerate=44100, channels=2)
    tiny_tag_get = Mock(return_value=tag)
    monkeypatch.setattr("services.file_scanner.TinyTag.get", tiny_tag_get)

    db = FakeDatabaseManager()
    scanner = FileScannerService(
        root_path=str(tmp_path), db_manager=cast(DatabaseManager, db)
    )

    finished_payloads: list[list[dict[str, Any]]] = []
    progress_events: list[tuple[int, int]] = []
    scanner.finished.connect(finished_payloads.append)
    scanner.progress.connect(
        lambda current, total: progress_events.append((current, total))
    )

    scanner.run()

    assert len(finished_payloads) == 1
    files_info = finished_payloads[0]
    assert len(files_info) == 1

    file_info = files_info[0]
    assert file_info["path"] == str(audio_path)
    assert file_info["size"] == 1024
    assert file_info["duration"] == 100.0
    assert file_info["samplerate"] == 44100
    assert file_info["channels"] == 2
    assert file_info["tags"] == {"filetype": [".wav"]}

    assert db.folder_queries == [str(tmp_path)]
    assert db.saved_records == files_info
    assert db.deleted_paths == []
    assert cache.flushed is True
    assert len(cache.updated) == 1
    assert progress_events[-1] == (1, 1)
    tiny_tag_get.assert_called_once_with(str(audio_path))


def test_scan_deletes_database_records_missing_from_folder(
    tmp_path: Path, monkeypatch
) -> None:
    live_path = tmp_path / "live.wav"
    live_path.write_bytes(b"\x00" * 32)
    orphan_path = str(tmp_path / "removed.wav")

    cache = FakeCacheManager()
    monkeypatch.setattr("services.file_scanner.CacheManager", lambda: cache)

    monkeypatch.setattr(
        "services.file_scanner.TinyTag.get",
        Mock(
            return_value=SimpleNamespace(duration=None, samplerate=None, channels=None)
        ),
    )

    db = FakeDatabaseManager(existing_records=[{"path": orphan_path}])
    scanner = FileScannerService(
        root_path=str(tmp_path), db_manager=cast(DatabaseManager, db)
    )

    scanner.run()

    assert db.deleted_paths == [orphan_path]
