from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
PROFILES_ROOT = ROOT / "profiles"


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def load_case_profiles() -> dict[str, Any]:
    payload = _load_yaml(PROFILES_ROOT / "case_profiles.yaml")
    return payload["cases"]


@lru_cache(maxsize=None)
def load_review_overlay_profile() -> dict[str, Any]:
    return _load_yaml(PROFILES_ROOT / "review_overlay.yaml")


@lru_cache(maxsize=None)
def load_generic_case_profile() -> dict[str, Any]:
    return _load_yaml(PROFILES_ROOT / "generic_case_profile.yaml")


@lru_cache(maxsize=None)
def load_canonical_profiles() -> dict[str, Any]:
    payload = _load_yaml(PROFILES_ROOT / "canonical_profiles.yaml")
    return payload["profiles"]


def get_case_profile(case_id: str) -> dict[str, Any] | None:
    return load_case_profiles().get(case_id)


def get_canonical_profile(profile_id: str) -> dict[str, Any] | None:
    return load_canonical_profiles().get(profile_id)
