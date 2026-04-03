"""Disk checks — ~/.claude/ size, session debris, log rotation."""

from __future__ import annotations

import os

from claudoctor.engine import Check
from claudoctor.models import Finding


def _dir_size_and_count(path: str) -> tuple[int, int]:
    """Return (total_bytes, file_count) for a directory."""
    total = 0
    count = 0
    try:
        for dirpath, _dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(fp)
                    count += 1
                except OSError:
                    pass
    except OSError:
        pass
    return total, count


def _human_size(size_bytes: int) -> str:
    """Format bytes as human-readable."""
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


class DiskChecks(Check):
    section = "Disk"

    def run(self) -> list[Finding]:
        findings = []
        claude_dir = os.path.expanduser("~/.claude")

        if not os.path.isdir(claude_dir):
            findings.append(self.passed("DISK-001", "No ~/.claude/ directory"))
            return findings

        # Total size
        total_size, total_count = _dir_size_and_count(claude_dir)
        findings.append(self.passed(
            "DISK-001",
            f"~/.claude/ total size: {_human_size(total_size)}",
            value=f"{_human_size(total_size)}, {total_count:,} files",
        ))

        # Check key subdirectories
        subdirs = {
            "projects": ("DISK-002", 2 * 1024**3, "Session data accumulates here"),
            "resume-summaries": ("DISK-003", 500 * 1024**2, "One per session, never pruned"),
            "session-cache": ("DISK-004", 500 * 1024**2, "Grows unbounded"),
        }

        for dirname, (check_id, warn_threshold, detail) in subdirs.items():
            dirpath = os.path.join(claude_dir, dirname)
            if os.path.isdir(dirpath):
                size, count = _dir_size_and_count(dirpath)
                if size > warn_threshold:
                    findings.append(self.warn(
                        check_id,
                        f"~/.claude/{dirname}/ is {_human_size(size)} ({count:,} files)",
                        detail=detail,
                        fix_command=f"find {dirpath} -mtime +30 -delete",
                        fix_description=f"Delete files older than 30 days from {dirname}/",
                        value=f"{_human_size(size)}, {count:,} files",
                    ))
                else:
                    findings.append(self.passed(
                        check_id,
                        f"~/.claude/{dirname}/ OK",
                        value=f"{_human_size(size)}, {count:,} files",
                    ))

        # Check daemon log
        daemon_log = os.path.join(claude_dir, "daemon-stderr.log")
        if os.path.exists(daemon_log):
            log_size = os.path.getsize(daemon_log)
            if log_size > 100 * 1024 * 1024:  # 100MB
                findings.append(self.warn(
                    "DISK-005",
                    f"daemon-stderr.log is {_human_size(log_size)} (no rotation)",
                    fix_command=f"truncate -s 0 {daemon_log}",
                    fix_description="Truncate the daemon log",
                ))
            else:
                findings.append(self.passed(
                    "DISK-005",
                    f"daemon-stderr.log OK",
                    value=_human_size(log_size),
                ))

        return findings
