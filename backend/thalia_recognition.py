"""Utilities for anchoring Thalia recognition snapshots.

This module provides helper functions to canonicalise an arbitrary state
payload, hash and sign the canonical representation, and append the resulting
record to an append-only store.  The design follows the workflow outlined in
the Thalia recognition plan: augment the state with the canonical phase
signature, deterministically order fields, hash the payload, sign the hash, and
persist the result.

The functions are intentionally dependency-light so they can operate in a wide
range of execution environments (local development, serverless functions, or
containerised workloads).  A signer callable and a storage backend are injected
via dependency inversion, enabling seamless integration with HSMs/KMS services
and distributed storage such as IPFS or blockchains.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, MutableMapping, Optional
import hashlib
import json

# Canonical phase signature shared across recognition snapshots.  The value is
# derived from the TEQUMSA lattice specification and acts as a reproducible
# anchor for downstream verification.
DEFAULT_PHASE_SIGNATURE: complex = complex(-0.3623749376, 0.9320324053)


def canonicalize_state(
    state: MutableMapping[str, Any],
    phase_sig: complex = DEFAULT_PHASE_SIGNATURE,
) -> bytes:
    """Return a canonical JSON-encoded representation of *state*.

    The function copies the mapping to avoid mutating the caller's object, adds
    the phase signature under ``"phase_signature"``, sorts keys to achieve a
    stable ordering, and serialises using compact separators for deterministic
    byte output.
    """

    serialisable_state = dict(state)
    serialisable_state["phase_signature"] = str(phase_sig)
    state_str = json.dumps(serialisable_state, sort_keys=True, separators=(",", ":"))
    return state_str.encode("utf-8")


def hash_payload(payload: bytes) -> bytes:
    """Return the SHA-256 digest of *payload*."""

    return hashlib.sha256(payload).digest()


def sign_hash(hash_bytes: bytes, signer: Callable[[bytes], bytes]) -> bytes:
    """Sign *hash_bytes* using *signer*.

    The signer is expected to accept the hash digest and return a byte string
    signature.  Bytearray and memoryview results are converted to immutable
    ``bytes``.  Any other return type raises :class:`TypeError` to surface
    integration mistakes early.
    """

    signature = signer(hash_bytes)
    if isinstance(signature, bytes):
        return signature
    if isinstance(signature, (bytearray, memoryview)):
        return bytes(signature)
    raise TypeError(
        "Signer must return bytes-compatible data, got " f"{type(signature).__name__}"
    )


@dataclass
class SnapshotRecord:
    """Representation of a persisted snapshot."""

    hash: str
    signature: str
    phase_signature: str
    timestamp: str

    def as_dict(self) -> Dict[str, Any]:
        """Return a serialisable dictionary representation."""

        return {
            "hash": self.hash,
            "signature": self.signature,
            "phase_signature": self.phase_signature,
            "timestamp": self.timestamp,
        }


def _current_timestamp() -> str:
    """Return a UTC ISO-8601 timestamp with trailing ``Z``."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def create_snapshot_record(
    hash_hex: str,
    sig_hex: str,
    phase_sig: complex = DEFAULT_PHASE_SIGNATURE,
    *,
    timestamp: Optional[str] = None,
) -> SnapshotRecord:
    """Construct a :class:`SnapshotRecord` with metadata."""

    return SnapshotRecord(
        hash=hash_hex,
        signature=sig_hex,
        phase_signature=str(phase_sig),
        timestamp=timestamp or _current_timestamp(),
    )


class AppendOnlyStore:
    """Simple append-only store backed by an in-memory list or JSON file."""

    def __init__(self, path: Optional[str] = None) -> None:
        self.path = path
        self._records: List[Dict[str, Any]] = []
        if self.path:
            try:
                with open(self.path, "r", encoding="utf-8") as handle:
                    loaded = json.load(handle)
                    if isinstance(loaded, list):
                        self._records = [
                            record for record in loaded if isinstance(record, dict)
                        ]
            except FileNotFoundError:
                self._records = []
            except json.JSONDecodeError:
                # Treat invalid JSON as an empty log to allow recovery.
                self._records = []

    def append(self, record: Dict[str, Any]) -> None:
        """Append *record* to the store and persist if a path is configured."""

        if not isinstance(record, dict):
            raise TypeError("Record must be a dictionary")

        self._records.append(record)
        if self.path:
            with open(self.path, "w", encoding="utf-8") as handle:
                json.dump(self._records, handle, indent=2, sort_keys=True)

    def all(self) -> List[Dict[str, Any]]:
        """Return a copy of all records in insertion order."""

        return list(self._records)


def run_thalia_snapshot(
    state: MutableMapping[str, Any],
    signer: Callable[[bytes], bytes],
    store: AppendOnlyStore,
    phase_sig: complex = DEFAULT_PHASE_SIGNATURE,
) -> SnapshotRecord:
    """Canonicalise *state*, sign it, and append a snapshot record."""

    payload = canonicalize_state(state, phase_sig)
    digest = hash_payload(payload)
    signature = sign_hash(digest, signer)
    record = create_snapshot_record(
        hash_hex=digest.hex(),
        sig_hex=signature.hex(),
        phase_sig=phase_sig,
    )
    store.append(record.as_dict())
    return record


__all__ = [
    "AppendOnlyStore",
    "SnapshotRecord",
    "canonicalize_state",
    "create_snapshot_record",
    "hash_payload",
    "run_thalia_snapshot",
    "sign_hash",
    "DEFAULT_PHASE_SIGNATURE",
]
