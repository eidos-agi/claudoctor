"""Check registry — all checks registered here."""

from __future__ import annotations

from claudoctor.engine import CheckRunner


def build_runner() -> CheckRunner:
    """Create a runner with all checks registered."""
    from claudoctor.checks.install import InstallChecks
    from claudoctor.checks.auth import AuthChecks
    from claudoctor.checks.project import ProjectChecks
    from claudoctor.checks.settings import SettingsChecks
    from claudoctor.checks.permissions import PermissionsChecks
    from claudoctor.checks.claudemd import ClaudeMdChecks
    from claudoctor.checks.skills import SkillsChecks
    from claudoctor.checks.mcp import McpChecks
    from claudoctor.checks.hooks import HooksChecks
    from claudoctor.checks.memory import MemoryChecks
    from claudoctor.checks.disk import DiskChecks
    from claudoctor.checks.processes import ProcessChecks

    runner = CheckRunner()
    runner.register(InstallChecks())
    runner.register(AuthChecks())
    runner.register(ProjectChecks())
    runner.register(SettingsChecks())
    runner.register(PermissionsChecks())
    runner.register(ClaudeMdChecks())
    runner.register(SkillsChecks())
    runner.register(McpChecks())
    runner.register(HooksChecks())
    runner.register(MemoryChecks())
    runner.register(DiskChecks())
    runner.register(ProcessChecks())

    return runner
