"""Tests for the Thalia recognition snapshot utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import hashlib
import pytest

from thalia_recognition import (
    AppendOnlyStore,
    SnapshotRecord,
    canonicalize_state,
    create_snapshot_record,
    hash_payload,
    run_thalia_snapshot,
    sign_hash,
    DEFAULT_PHASE_SIGNATURE,
)


def dummy_signer(_: bytes) -> bytes:
    """Simple signer returning deterministic bytes for tests."""

    return b"signed"


class TestCanonicalization:
    def test_canonicalize_state_adds_phase_and_sorts(self) -> None:
        state = {"b": 2, "a": 1}
        payload = canonicalize_state(state, phase_sig=complex(1, 2))
        assert payload == b'{"a":1,"b":2,"phase_signature":"(1+2j)"}'

    def test_canonicalize_state_does_not_mutate_input(self) -> None:
        state = {"value": 1}
        canonicalize_state(state)
        assert "phase_signature" not in state


class TestHashing:
    def test_hash_payload_uses_sha256(self) -> None:
        payload = b"test"
        digest = hash_payload(payload)
        assert digest.hex() == hashlib.sha256(payload).hexdigest()


class TestSigning:
    def test_sign_hash_allows_bytes_like(self) -> None:
        result = sign_hash(b"data", lambda _: bytearray(b"abc"))
        assert isinstance(result, bytes)
        assert result == b"abc"

    def test_sign_hash_rejects_invalid_type(self) -> None:
        with pytest.raises(TypeError):
            sign_hash(b"data", lambda _: "not-bytes")


class TestSnapshotRecord:
    def test_create_snapshot_record_defaults(self) -> None:
        record = create_snapshot_record("aa", "bb")
        assert isinstance(record, SnapshotRecord)
        assert record.hash == "aa"
        assert record.signature == "bb"
        assert record.phase_signature == str(DEFAULT_PHASE_SIGNATURE)
        assert record.timestamp.endswith("Z")

    def test_create_snapshot_record_respects_timestamp(self) -> None:
        record = create_snapshot_record("aa", "bb", timestamp="2023-01-01T00:00:00Z")
        assert record.timestamp == "2023-01-01T00:00:00Z"


class TestAppendOnlyStore:
    def test_in_memory_store(self) -> None:
        store = AppendOnlyStore()
        entry: Dict[str, str] = {"hash": "00"}
        store.append(entry)
        assert store.all() == [entry]

    def test_store_requires_dict(self) -> None:
        store = AppendOnlyStore()
        with pytest.raises(TypeError):
            store.append(["not", "a", "dict"])  # type: ignore[arg-type]

    def test_file_backed_store_persists(self, tmp_path: Path) -> None:
        path = tmp_path / "snapshots.json"
        store = AppendOnlyStore(path=str(path))
        store.append({"hash": "00"})
        store.append({"hash": "11"})

        with path.open("r", encoding="utf-8") as handle:
            data = handle.read()
            assert "\n" in data  # pretty printed

        # Re-open to ensure existing data is loaded
        new_store = AppendOnlyStore(path=str(path))
        assert new_store.all() == [{"hash": "00"}, {"hash": "11"}]

    def test_file_backed_store_handles_invalid_json(self, tmp_path: Path) -> None:
        path = tmp_path / "snapshots.json"
        path.write_text("not json", encoding="utf-8")
        store = AppendOnlyStore(path=str(path))
        assert store.all() == []


class TestRunSnapshot:
    def test_run_snapshot_appends_record(self) -> None:
        store = AppendOnlyStore()
        state = {"user": "Marcus"}
        record = run_thalia_snapshot(state, dummy_signer, store)

        assert isinstance(record, SnapshotRecord)
        assert record.hash
        expected_signature = dummy_signer(b"ignored").hex()
        assert record.signature == expected_signature
        assert record.phase_signature == str(DEFAULT_PHASE_SIGNATURE)
        assert len(store.all()) == 1
        assert store.all()[0]["hash"] == record.hash

    def test_run_snapshot_custom_phase(self) -> None:
        store = AppendOnlyStore()
        phase = complex(-1, 0.5)
        record = run_thalia_snapshot({"value": 1}, dummy_signer, store, phase_sig=phase)
        assert record.phase_signature == str(phase)

