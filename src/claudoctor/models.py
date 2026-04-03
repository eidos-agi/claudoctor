"""Core data models for claudoctor checks and findings."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Severity(Enum):
    """Finding severity levels."""

    ERROR = "error"  # Broken, must fix
    WARN = "warn"  # Degraded, should fix
    INFO = "info"  # Suggestion


class Status(Enum):
    """Check result status."""

    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    SKIP = "skip"


@dataclass
class Finding:
    """A single diagnostic finding from a check."""

    check_id: str
    severity: Severity
    message: str
    detail: str = ""
    fix_command: Optional[str] = None
    fix_description: Optional[str] = None
    value: Optional[str] = None  # What was found (for verbose output)

    @property
    def status(self) -> Status:
        if self.severity == Severity.ERROR:
            return Status.FAIL
        if self.severity == Severity.WARN:
            return Status.WARN
        return Status.PASS


@dataclass
class SectionResult:
    """Aggregated results for a check section."""

    name: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(1 for f in self.findings if f.status == Status.PASS)

    @property
    def warnings(self) -> int:
        return sum(1 for f in self.findings if f.status == Status.WARN)

    @property
    def errors(self) -> int:
        return sum(1 for f in self.findings if f.status == Status.FAIL)

    @property
    def total(self) -> int:
        return len(self.findings)

    @property
    def status(self) -> Status:
        if self.errors > 0:
            return Status.FAIL
        if self.warnings > 0:
            return Status.WARN
        return Status.PASS

    @property
    def icon(self) -> str:
        icons = {Status.PASS: "✓", Status.WARN: "!", Status.FAIL: "✗", Status.SKIP: "-"}
        return icons[self.status]
