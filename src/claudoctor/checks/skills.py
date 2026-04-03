"""Skills checks — structure, collisions, import paths."""

from __future__ import annotations

import os

from claudoctor.engine import Check
from claudoctor.models import Finding


class SkillsChecks(Check):
    section = "Skills"

    def run(self) -> list[Finding]:
        findings = []
        findings.append(self._check_skills_structure())
        findings.append(self._check_name_collisions())
        return findings

    def _check_skills_structure(self) -> Finding:
        skills_dir = ".claude/skills"
        if not os.path.isdir(skills_dir):
            return self.passed("SKILLS-001", "No .claude/skills/ directory")

        issues = []
        skill_count = 0
        for entry in os.listdir(skills_dir):
            entry_path = os.path.join(skills_dir, entry)
            if not os.path.isdir(entry_path):
                continue
            skill_count += 1

            # Check for skill.md (preferred) or SKILL.md
            has_skill = (
                os.path.exists(os.path.join(entry_path, "skill.md"))
                or os.path.exists(os.path.join(entry_path, "SKILL.md"))
            )
            if not has_skill:
                issues.append(f"{entry}/ — missing skill.md")

        if issues:
            return self.warn(
                "SKILLS-001",
                f"Skills structure issues ({len(issues)})",
                detail="\n".join(f"  - {i}" for i in issues[:10]),
                fix_description="Each skill directory needs a skill.md file",
            )

        if skill_count > 0:
            return self.passed(
                "SKILLS-001",
                f"Skills structure OK",
                value=f"{skill_count} skills",
            )

        return self.passed("SKILLS-001", "Skills directory exists but empty")

    def _check_name_collisions(self) -> Finding:
        project_skills = set()
        user_skills = set()

        project_dir = ".claude/skills"
        user_dir = os.path.expanduser("~/.claude/skills")

        if os.path.isdir(project_dir):
            project_skills = {e for e in os.listdir(project_dir) if os.path.isdir(os.path.join(project_dir, e))}
        if os.path.isdir(user_dir):
            user_skills = {e for e in os.listdir(user_dir) if os.path.isdir(os.path.join(user_dir, e))}

        collisions = project_skills & user_skills
        if collisions:
            return self.warn(
                "SKILLS-002",
                f"Skill name collisions between user and project: {', '.join(sorted(collisions))}",
                detail="Project-level skills win — user-level skills with same name are shadowed",
            )

        return self.passed("SKILLS-002", "No skill name collisions")
