from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class RequirementEntry:
    identifier: str
    text: str
    section: str


@dataclass
class UseCaseEntry:
    identifier: str
    title: str
    main_flow_steps: list[str]
    exception_flow_steps: list[str]


@dataclass
class ParsedDocument:
    path: Path
    case_id: str
    title: str
    document: dict[str, Any]
    requirements: list[RequirementEntry] = field(default_factory=list)
    use_cases: list[UseCaseEntry] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
