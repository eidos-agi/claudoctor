"""Memory checks — MEMORY.md health, truncation, stale entries."""

from __future__ import annotations

import os
import re

from claudoctor.engine import Check
from claudoctor.models import Finding

MEMORY_LINE_LIMIT = 200
MEMORY_WARN_THRESHOLD = 180


class MemoryChecks(Check):
    section = "Memory"

    def run(self) -> list[Finding]:
        findings = []
        findings.extend(self._check_memory_md(
            os.path.expanduser("~/.claude/MEMORY.md"), "Global", "MEMORY-001"
        ))

        # Check project memory
        project_memory = self._find_project_memory()
        if project_memory:
            findings.extend(self._check_memory_md(project_memory, "Project", "MEMORY-002"))

        findings.extend(self._check_memory_files())
        return findings

    def _find_project_memory(self) -> str | None:
        # Project memory is at ~/.claude/projects/<path-hash>/memory/MEMORY.md
        # Try to find it based on cwd
        cwd = os.getcwd()
        projects_dir = os.path.expanduser("~/.claude/projects")
        if not os.path.isdir(projects_dir):
            return None

        # The path is mangled: /Users/foo/bar -> -Users-foo-bar
        mangled = cwd.replace("/", "-")
        project_dir = os.path.join(projects_dir, mangled, "memory", "MEMORY.md")
        if os.path.exists(project_dir):
            return project_dir

        return None

    def _check_memory_md(self, path: str, scope: str, check_id: str) -> list[Finding]:
        if not os.path.exists(path):
            return [self.passed(check_id, f"No {scope} MEMORY.md")]

        with open(path) as f:
            lines = f.readlines()

        findings = []
        line_count = len(lines)

        if line_count >= MEMORY_LINE_LIMIT:
            findings.append(self.warn(
                check_id,
                f"{scope} MEMORY.md is {line_count} lines — TRUNCATED at {MEMORY_LINE_LIMIT}",
                detail=f"Lines after {MEMORY_LINE_LIMIT} are silently ignored by Claude Code",
                fix_description="Consolidate entries, remove stale items, move detail to separate files",
                value=f"{line_count} lines (limit: {MEMORY_LINE_LIMIT})",
            ))
        elif line_count >= MEMORY_WARN_THRESHOLD:
            findings.append(self.warn(
                check_id,
                f"{scope} MEMORY.md is {line_count}/{MEMORY_LINE_LIMIT} lines — approaching truncation",
                fix_description="Prune stale entries before hitting the limit",
                value=f"{line_count} lines",
            ))
        else:
            findings.append(self.passed(
                check_id,
                f"{scope} MEMORY.md line count OK",
                value=f"{line_count}/{MEMORY_LINE_LIMIT} lines",
            ))

        # Check for stale entries (relative timestamps)
        content = "".join(lines)
        stale_patterns = [
            r"\byesterday\b", r"\blast week\b", r"\btoday\b",
            r"\bjust now\b", r"\brecently\b", r"\bthis morning\b",
        ]
        stale_found = []
        for pattern in stale_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                stale_found.append(pattern.strip(r"\b"))

        if stale_found:
            findings.append(self.warn(
                "MEMORY-003",
                f"MEMORY.md contains relative timestamps: {', '.join(stale_found)}",
                detail="Relative timestamps become meaningless over time — use absolute dates",
            ))

        return findings

    def _check_memory_files(self) -> list[Finding]:
        # Check if MEMORY.md references files that don't exist
        findings = []
        cwd = os.getcwd()
        projects_dir = os.path.expanduser("~/.claude/projects")
        mangled = cwd.replace("/", "-")
        memory_dir = os.path.join(projects_dir, mangled, "memory")

        if not os.path.isdir(memory_dir):
            return [self.passed("MEMORY-005", "No project memory directory")]

        memory_md = os.path.join(memory_dir, "MEMORY.md")
        if not os.path.exists(memory_md):
            return [self.passed("MEMORY-005", "No MEMORY.md to check links")]

        with open(memory_md) as f:
            content = f.read()

        # Find markdown links [text](file.md)
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')
        broken_links = []
        for _text, link in link_pattern.findall(content):
            link_path = os.path.join(memory_dir, link)
            if not os.path.exists(link_path):
                broken_links.append(link)

        if broken_links:
            findings.append(self.error(
                "MEMORY-005",
                f"MEMORY.md references {len(broken_links)} missing files",
                detail="\n".join(f"  - {l}" for l in broken_links[:10]),
                fix_description="Remove broken links or recreate missing memory files",
            ))
        else:
            findings.append(self.passed("MEMORY-005", "All MEMORY.md links resolve"))

        # Check for orphaned memory files
        if os.path.isdir(memory_dir):
            memory_files = {f for f in os.listdir(memory_dir) if f.endswith(".md") and f != "MEMORY.md"}
            referenced = set(link for _, link in link_pattern.findall(content))
            orphans = memory_files - referenced
            if orphans:
                findings.append(self.passed(
                    "MEMORY-006",
                    f"{len(orphans)} memory files not linked from MEMORY.md",
                    value=", ".join(sorted(orphans)[:5]),
                ))

        return findings
