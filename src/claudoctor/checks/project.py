"""Project root checks — directory, CLAUDE.md, .claudeignore."""

from __future__ import annotations

import os
import subprocess

from claudoctor.engine import Check
from claudoctor.models import Finding


RECOMMENDED_IGNORES = [
    "node_modules/",
    "dist/",
    "build/",
    ".next/",
    "__pycache__/",
    ".venv/",
    "*.lock",
]


class ProjectChecks(Check):
    section = "Project"

    def run(self) -> list[Finding]:
        findings = []
        findings.append(self._check_git_root())
        findings.append(self._check_claudemd_exists())
        findings.append(self._check_claudeignore_exists())
        findings.append(self._check_claudeignore_coverage())
        findings.append(self._check_nested_projects())
        return findings

    def _check_git_root(self) -> Finding:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, timeout=5,
            )
            git_root = result.stdout.strip()
            cwd = os.getcwd()
            if git_root and os.path.realpath(git_root) != os.path.realpath(cwd):
                return self.warn(
                    "PROJECT-001",
                    "Not at git repository root",
                    detail=f"cwd: {cwd}\ngit root: {git_root}",
                    fix_command=f"cd {git_root}",
                    fix_description="Run claudoctor from the git root for best results",
                )
            if git_root:
                return self.passed("PROJECT-001", "At git repository root", value=git_root)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return self.warn("PROJECT-001", "Not in a git repository")

    def _check_claudemd_exists(self) -> Finding:
        if os.path.exists("CLAUDE.md"):
            size = os.path.getsize("CLAUDE.md")
            return self.passed(
                "PROJECT-002", "CLAUDE.md found",
                value=f"{size:,} bytes",
            )
        return self.warn(
            "PROJECT-002",
            "No CLAUDE.md in project root",
            detail="Claude Code works better with project-specific instructions",
            fix_command="claude init",
            fix_description="Generate a CLAUDE.md for this project",
        )

    def _check_claudeignore_exists(self) -> Finding:
        if os.path.exists(".claudeignore"):
            return self.passed("PROJECT-003", ".claudeignore found")

        # Check for common large directories that should be ignored
        bloat_dirs = [d for d in ["node_modules", "dist", "build", ".next", "__pycache__", ".venv"]
                      if os.path.isdir(d)]
        if bloat_dirs:
            return self.warn(
                "PROJECT-003",
                f"No .claudeignore but found: {', '.join(bloat_dirs)}",
                detail="These directories inflate context scanning and burn tokens",
                fix_command=f"echo '{chr(10).join(RECOMMENDED_IGNORES)}' > .claudeignore",
                fix_description="Create .claudeignore with recommended patterns",
            )

        return self.passed("PROJECT-003", "No .claudeignore (no large directories detected)")

    def _check_claudeignore_coverage(self) -> Finding:
        if not os.path.exists(".claudeignore"):
            return self.passed("PROJECT-004", ".claudeignore coverage (no file)")

        with open(".claudeignore") as f:
            content = f.read()

        missing = []
        for pattern in RECOMMENDED_IGNORES:
            # Check if pattern or similar is covered
            base = pattern.rstrip("/").rstrip("*").rstrip(".")
            if base and base not in content:
                # Only flag if the directory actually exists
                if os.path.isdir(base) or (pattern.startswith("*") and True):
                    missing.append(pattern)

        if missing:
            return self.warn(
                "PROJECT-004",
                f".claudeignore missing {len(missing)} recommended patterns",
                detail="Missing: " + ", ".join(missing),
                fix_command=f"echo '{chr(10).join(missing)}' >> .claudeignore",
                fix_description="Append missing patterns to .claudeignore",
            )

        return self.passed("PROJECT-004", ".claudeignore covers recommended patterns")

    def _check_nested_projects(self) -> Finding:
        claude_mds = []
        for root, dirs, files in os.walk("."):
            # Don't walk into ignored dirs
            dirs[:] = [d for d in dirs if d not in {
                "node_modules", ".git", "dist", "build", ".venv", "__pycache__",
            }]
            if "CLAUDE.md" in files and root != ".":
                claude_mds.append(os.path.join(root, "CLAUDE.md"))
            if len(claude_mds) >= 10:
                break

        if claude_mds:
            return self.passed(
                "PROJECT-006",
                f"Nested CLAUDE.md files found ({len(claude_mds)})",
                value="\n".join(claude_mds[:5]),
            )

        return self.passed("PROJECT-006", "No nested CLAUDE.md files")
