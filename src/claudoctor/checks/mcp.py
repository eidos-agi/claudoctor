"""MCP server checks — config, health, security, context budget."""

from __future__ import annotations

import json
import os
import subprocess

from claudoctor.engine import Check
from claudoctor.models import Finding

TOKENS_PER_SERVER = 5000  # Rough estimate of schema token overhead per server


class McpChecks(Check):
    section = "MCP Servers"

    def run(self) -> list[Finding]:
        findings = []

        # Load MCP configs
        configs = self._load_mcp_configs()
        if configs is None:
            findings.append(self.passed("MCP-001", "No .mcp.json found"))
            findings.append(self._check_mcp_in_wrong_file())
            return findings

        findings.append(self.passed("MCP-001", ".mcp.json is valid JSON"))
        findings.append(self._check_mcp_in_wrong_file())

        servers = configs.get("mcpServers", {})
        if not servers:
            findings.append(self.passed("MCP-007", "No MCP servers configured"))
            return findings

        # Server count and token overhead
        findings.append(self._check_server_count(servers))

        # Per-server checks
        for name, config in servers.items():
            findings.extend(self._check_server(name, config))

        # Security audit
        findings.append(self._check_security())

        return findings

    def _load_mcp_configs(self) -> dict | None:
        for path in [".mcp.json", os.path.expanduser("~/.claude/.mcp.json")]:
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        return json.load(f)
                except json.JSONDecodeError:
                    return None  # Will be caught by validator
        return None

    def _check_mcp_in_wrong_file(self) -> Finding:
        wrong_files = [
            (".claude/settings.json", "project settings"),
            (os.path.expanduser("~/.claude/settings.json"), "global settings"),
            (os.path.expanduser("~/.claude.json"), "~/.claude.json"),
        ]

        for path, label in wrong_files:
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        data = json.load(f)
                    if "mcpServers" in data:
                        return self.warn(
                            "MCP-002",
                            f"MCP server config found in {label} instead of .mcp.json",
                            detail=f"File: {path}\nMCP servers should be defined in .mcp.json",
                            fix_description="Move mcpServers section to .mcp.json",
                        )
                except (json.JSONDecodeError, OSError):
                    pass

        return self.passed("MCP-002", "No MCP config in wrong files")

    def _check_server_count(self, servers: dict) -> Finding:
        count = len(servers)
        estimated_tokens = count * TOKENS_PER_SERVER

        if count > 20:
            return self.warn(
                "MCP-007",
                f"{count} MCP servers — estimated ~{estimated_tokens:,} tokens of context overhead",
                detail="Each server injects its full tool schema into every message. Consider disabling unused servers.",
                value=f"{count} servers, ~{estimated_tokens:,} tokens",
            )
        if count > 10:
            return self.passed(
                "MCP-007",
                f"{count} MCP servers (~{estimated_tokens:,} tokens overhead)",
                value=f"{count} servers",
            )
        return self.passed("MCP-007", f"{count} MCP servers", value=f"~{estimated_tokens:,} tokens overhead")

    def _check_server(self, name: str, config: dict) -> list[Finding]:
        findings = []
        command = config.get("command", "")
        args = config.get("args", [])
        env = config.get("env", {})

        # Check command binary exists
        if command:
            import shutil

            if not shutil.which(command):
                # Maybe it's a path
                if not os.path.exists(command):
                    findings.append(self.error(
                        "MCP-003",
                        f"[{name}] Command not found: {command}",
                        fix_description=f"Install {command} or fix the path in .mcp.json",
                    ))
                elif not os.access(command, os.X_OK):
                    findings.append(self.error(
                        "MCP-003",
                        f"[{name}] Command not executable: {command}",
                        fix_command=f"chmod +x {command}",
                    ))

        # Check for hardcoded user paths
        all_args = " ".join(str(a) for a in args) + " " + command
        if "/Users/" in all_args or "/home/" in all_args:
            findings.append(self.warn(
                "MCP-005",
                f"[{name}] Hardcoded user path detected",
                detail="Hardcoded paths break on other machines",
                fix_description="Use relative paths or environment variables",
            ))

        # Check referenced script files exist
        for arg in args:
            if isinstance(arg, str) and (arg.endswith(".py") or arg.endswith(".js") or arg.endswith(".ts")):
                if not os.path.exists(arg) and not os.path.exists(os.path.expanduser(arg)):
                    findings.append(self.error(
                        "MCP-004",
                        f"[{name}] Script file not found: {arg}",
                    ))

        # Check env vars are set
        for var_name, var_value in env.items():
            if var_value and var_value.startswith("${") and var_value.endswith("}"):
                # Reference to env var
                ref = var_value[2:-1]
                if not os.environ.get(ref):
                    findings.append(self.warn(
                        "MCP-006",
                        f"[{name}] Env var not set: {ref}",
                        detail=f"Referenced as {var_name} in server config",
                    ))

        return findings

    def _check_security(self) -> Finding:
        # Check if project .mcp.json exists and we're in someone else's repo
        if not os.path.exists(".mcp.json"):
            return self.passed("MCP-013", "No project .mcp.json (no security concern)")

        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True, text=True, timeout=5,
            )
            remote = result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            remote = ""

        try:
            result = subprocess.run(
                ["git", "config", "user.email"],
                capture_output=True, text=True, timeout=5,
            )
            user_email = result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            user_email = ""

        # If the remote doesn't match common user patterns, warn
        if remote and user_email:
            # Extract org/user from remote
            remote_lower = remote.lower()
            email_user = user_email.split("@")[0].lower()
            if email_user not in remote_lower:
                return self.warn(
                    "MCP-013",
                    "Project .mcp.json exists in a repo you may not own",
                    detail=f"Remote: {remote}\nUser: {user_email}\n"
                           "Malicious .mcp.json can execute arbitrary code (CVE-2025-59536)",
                    fix_description="Review .mcp.json commands before running Claude Code in cloned repos",
                )

        return self.passed("MCP-013", "Project .mcp.json security check passed")
