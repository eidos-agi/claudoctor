"""Installation checks — binary, version, Node, npm permissions."""

from __future__ import annotations

import os
import shutil
import subprocess

from claudoctor.engine import Check
from claudoctor.models import Finding


class InstallChecks(Check):
    section = "Installation"

    def run(self) -> list[Finding]:
        findings = []
        findings.append(self._check_binary())
        findings.append(self._check_version())
        findings.append(self._check_node_version())
        findings.append(self._check_npm_permissions())
        findings.append(self._check_multiple_installs())
        return findings

    def _check_binary(self) -> Finding:
        path = shutil.which("claude")
        if path:
            return self.passed("INSTALL-001", "Claude Code binary found", value=path)
        return self.error(
            "INSTALL-001",
            "Claude Code binary not found on PATH",
            fix_command="npm install -g @anthropic-ai/claude-code",
            fix_description="Install Claude Code globally",
        )

    def _check_version(self) -> Finding:
        try:
            result = subprocess.run(
                ["claude", "--version"], capture_output=True, text=True, timeout=10
            )
            version = result.stdout.strip()
            if version:
                return self.passed("INSTALL-002", "Claude Code version", value=version)
            return self.warn("INSTALL-002", "Could not determine Claude Code version")
        except FileNotFoundError:
            return self.warn("INSTALL-002", "Claude Code not installed, skipping version check")
        except subprocess.TimeoutExpired:
            return self.warn("INSTALL-002", "Version check timed out")

    def _check_node_version(self) -> Finding:
        try:
            result = subprocess.run(
                ["node", "--version"], capture_output=True, text=True, timeout=5
            )
            version = result.stdout.strip()
            if not version:
                return self.warn("INSTALL-003", "Could not determine Node.js version")

            # Extract major version
            major = int(version.lstrip("v").split(".")[0])
            if major < 18:
                return self.error(
                    "INSTALL-003",
                    f"Node.js {version} is too old (minimum 18)",
                    fix_command="nvm install 20 && nvm use 20",
                )
            if major > 22:
                return self.warn(
                    "INSTALL-003",
                    f"Node.js {version} may cause issues — Node 20 is recommended",
                    detail="Some users report latency and jank with newer Node versions",
                    fix_command="nvm install 20 && nvm use 20",
                )
            return self.passed("INSTALL-003", f"Node.js version OK", value=version)
        except FileNotFoundError:
            return self.error("INSTALL-003", "Node.js not found on PATH")
        except (subprocess.TimeoutExpired, ValueError):
            return self.warn("INSTALL-003", "Could not check Node.js version")

    def _check_npm_permissions(self) -> Finding:
        npm_prefix = os.environ.get("NPM_CONFIG_PREFIX", "")
        if npm_prefix and os.access(npm_prefix, os.W_OK):
            return self.passed("INSTALL-004", "npm prefix is writable", value=npm_prefix)

        try:
            result = subprocess.run(
                ["npm", "config", "get", "prefix"], capture_output=True, text=True, timeout=5
            )
            prefix = result.stdout.strip()
            if prefix and os.access(prefix, os.W_OK):
                return self.passed("INSTALL-004", "npm global prefix is writable", value=prefix)
            if prefix:
                return self.warn(
                    "INSTALL-004",
                    f"npm global prefix not writable: {prefix}",
                    detail="May need sudo to install/update global packages (EACCES)",
                    fix_command=f"sudo chown -R $(whoami) {prefix}",
                    fix_description="Fix npm global directory permissions",
                )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return self.passed("INSTALL-004", "npm permissions (unable to verify, assuming OK)")

    def _check_multiple_installs(self) -> Finding:
        try:
            result = subprocess.run(
                ["which", "-a", "claude"], capture_output=True, text=True, timeout=5
            )
            paths = [p.strip() for p in result.stdout.strip().split("\n") if p.strip()]
            if len(paths) > 1:
                return self.error(
                    "INSTALL-005",
                    f"Multiple Claude Code installations found ({len(paths)})",
                    detail="\n".join(paths),
                    fix_description="Remove duplicate installations to avoid conflicts",
                )
            if len(paths) == 1:
                return self.passed("INSTALL-005", "Single installation", value=paths[0])
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return self.passed("INSTALL-005", "Installation check (unable to verify)")
