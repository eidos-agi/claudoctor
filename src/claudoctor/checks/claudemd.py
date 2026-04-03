"""CLAUDE.md quality checks — token budget, missing ops, bloat, scope."""

from __future__ import annotations

import os

from claudoctor.engine import Check
from claudoctor.models import Finding

# Rough token estimation: ~4 chars per token for English text
CHARS_PER_TOKEN = 4
GLOBAL_TOKEN_BUDGET = 4000
PROJECT_TOKEN_BUDGET = 8000

# Patterns that suggest duplicated config
DUPLICATED_PATTERNS = [
    ("tsconfig", "tsconfig.json content duplicated in CLAUDE.md"),
    ("eslint", "ESLint config duplicated in CLAUDE.md"),
    ('"scripts":', "package.json scripts duplicated in CLAUDE.md"),
    ('"dependencies":', "package.json dependencies duplicated in CLAUDE.md"),
    (".prettierrc", "Prettier config duplicated in CLAUDE.md"),
]

# Patterns that suggest missing ops config
OPS_KEYWORDS = ["build", "test", "lint", "dev server", "npm run", "yarn", "pnpm", "pip install", "make"]


class ClaudeMdChecks(Check):
    section = "CLAUDE.md"

    def run(self) -> list[Finding]:
        findings = []
        findings.extend(self._check_global_claudemd())
        findings.extend(self._check_project_claudemd())
        return findings

    def _check_global_claudemd(self) -> list[Finding]:
        path = os.path.expanduser("~/.claude/CLAUDE.md")
        if not os.path.exists(path):
            return [self.passed("CLAUDEMD-001", "No global CLAUDE.md")]

        with open(path) as f:
            content = f.read()

        findings = []
        tokens = len(content) // CHARS_PER_TOKEN

        if tokens > GLOBAL_TOKEN_BUDGET:
            findings.append(self.warn(
                "CLAUDEMD-001",
                f"Global CLAUDE.md is ~{tokens:,} tokens (budget: {GLOBAL_TOKEN_BUDGET:,})",
                detail="This loads into every conversation across all projects",
                fix_description="Move project-specific rules to project CLAUDE.md or skills",
                value=f"{len(content):,} chars, ~{tokens:,} tokens",
            ))
        else:
            findings.append(self.passed(
                "CLAUDEMD-001",
                f"Global CLAUDE.md token count OK",
                value=f"~{tokens:,} tokens (budget: {GLOBAL_TOKEN_BUDGET:,})",
            ))

        # Check for project-specific content in global
        project_indicators = [
            "package.json", "tsconfig", "Cargo.toml", "pyproject.toml",
            "src/", "components/", "migrations/",
        ]
        found = [p for p in project_indicators if p in content]
        if found:
            findings.append(self.warn(
                "CLAUDEMD-006",
                "Global CLAUDE.md may contain project-specific references",
                detail=f"Found: {', '.join(found[:5])}",
                fix_description="Move project-specific rules to project-level CLAUDE.md",
            ))

        return findings

    def _check_project_claudemd(self) -> list[Finding]:
        path = "CLAUDE.md"
        if not os.path.exists(path):
            return [self.passed("CLAUDEMD-002", "No project CLAUDE.md (checked in Project section)")]

        with open(path) as f:
            content = f.read()

        findings = []
        tokens = len(content) // CHARS_PER_TOKEN

        if tokens > PROJECT_TOKEN_BUDGET:
            findings.append(self.warn(
                "CLAUDEMD-002",
                f"Project CLAUDE.md is ~{tokens:,} tokens (budget: {PROJECT_TOKEN_BUDGET:,})",
                detail="Large CLAUDE.md dilutes attention — consider extracting to skills",
                value=f"{len(content):,} chars, ~{tokens:,} tokens",
            ))
        else:
            findings.append(self.passed(
                "CLAUDEMD-002",
                f"Project CLAUDE.md token count OK",
                value=f"~{tokens:,} tokens (budget: {PROJECT_TOKEN_BUDGET:,})",
            ))

        # Check for duplicated config
        for pattern, message in DUPLICATED_PATTERNS:
            if pattern in content.lower():
                findings.append(self.warn(
                    "CLAUDEMD-005",
                    message,
                    detail="Duplicating config files wastes context — Claude can read the originals",
                ))
                break  # One warning is enough

        # Check for missing ops config
        content_lower = content.lower()
        has_ops = any(kw in content_lower for kw in OPS_KEYWORDS)
        if not has_ops:
            findings.append(self.warn(
                "CLAUDEMD-004",
                "CLAUDE.md missing core ops config (build, test, lint commands)",
                detail="Without these, Claude Code has to guess how to build and test your project",
                fix_description="Add a section with build/test/lint/dev-server commands",
            ))

        # Check if content should be skills
        lines = content.split("\n")
        if len(lines) > 200:
            findings.append(self.warn(
                "CLAUDEMD-007",
                f"CLAUDE.md is {len(lines)} lines — consider extracting to skills",
                detail="Long policies and workflows work better as .claude/skills/ files",
                fix_description="Move workflow sections to .claude/skills/<name>/skill.md",
            ))

        return findings
