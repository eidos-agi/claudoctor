"""Authentication checks — API key, OAuth, cloud providers."""

from __future__ import annotations

import os
import stat
import subprocess

from claudoctor.engine import Check
from claudoctor.models import Finding


class AuthChecks(Check):
    section = "Authentication"

    def run(self) -> list[Finding]:
        findings = []
        findings.append(self._check_api_key())
        findings.append(self._check_cloud_providers())
        findings.append(self._check_api_key_helper())
        return findings

    def _check_api_key(self) -> Finding:
        key = os.environ.get("ANTHROPIC_API_KEY")
        if key:
            masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"
            return self.passed("AUTH-001", "ANTHROPIC_API_KEY is set", value=masked)

        # Check if it's in shell config but not exported
        shell_configs = [
            os.path.expanduser("~/.bashrc"),
            os.path.expanduser("~/.zshrc"),
            os.path.expanduser("~/.bash_profile"),
            os.path.expanduser("~/.zprofile"),
        ]
        for config in shell_configs:
            if os.path.exists(config):
                try:
                    with open(config) as f:
                        content = f.read()
                    if "ANTHROPIC_API_KEY" in content:
                        return self.error(
                            "AUTH-001",
                            f"ANTHROPIC_API_KEY found in {config} but not in current environment",
                            detail="Key is defined in shell config but not exported to this session",
                            fix_command=f"source {config}",
                            fix_description="Source your shell config to export the key",
                        )
                except PermissionError:
                    pass

        # Not an error if using OAuth or cloud providers
        if os.environ.get("CLAUDE_CODE_USE_BEDROCK") or os.environ.get("CLAUDE_CODE_USE_VERTEX"):
            return self.passed("AUTH-001", "No API key (using cloud provider auth)")

        return self.warn(
            "AUTH-001",
            "ANTHROPIC_API_KEY not set",
            detail="May be using OAuth or cloud provider auth instead",
        )

    def _check_cloud_providers(self) -> Finding:
        bedrock = os.environ.get("CLAUDE_CODE_USE_BEDROCK")
        vertex = os.environ.get("CLAUDE_CODE_USE_VERTEX")

        if not bedrock and not vertex:
            return self.passed("AUTH-004", "No cloud provider flags set (using direct API)")

        issues = []
        if bedrock:
            if not os.environ.get("AWS_REGION") and not os.environ.get("AWS_DEFAULT_REGION"):
                issues.append("CLAUDE_CODE_USE_BEDROCK set but no AWS_REGION/AWS_DEFAULT_REGION")
            if not os.environ.get("AWS_ACCESS_KEY_ID") and not os.environ.get("AWS_PROFILE"):
                issues.append("No AWS_ACCESS_KEY_ID or AWS_PROFILE for Bedrock auth")

        if vertex:
            if not os.environ.get("CLOUD_ML_REGION") and not os.environ.get("GOOGLE_CLOUD_REGION"):
                issues.append("CLAUDE_CODE_USE_VERTEX set but no region configured")
            if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
                issues.append("No GOOGLE_APPLICATION_CREDENTIALS for Vertex auth")

        if issues:
            return self.error(
                "AUTH-004",
                "Cloud provider flags set but credentials incomplete",
                detail="\n".join(f"  - {i}" for i in issues),
            )

        provider = "Bedrock" if bedrock else "Vertex"
        return self.passed("AUTH-004", f"Cloud provider configured: {provider}")

    def _check_api_key_helper(self) -> Finding:
        # Check settings for apiKeyHelper
        settings_paths = [
            os.path.expanduser("~/.claude/settings.json"),
            os.path.expanduser("~/.claude.json"),
        ]

        for path in settings_paths:
            if os.path.exists(path):
                try:
                    import json

                    with open(path) as f:
                        settings = json.load(f)
                    helper = settings.get("apiKeyHelper")
                    if helper:
                        # Check if it's executable
                        helper_path = helper.split()[0] if isinstance(helper, str) else None
                        if helper_path and os.path.exists(helper_path):
                            mode = os.stat(helper_path).st_mode
                            if not (mode & stat.S_IXUSR):
                                return self.error(
                                    "AUTH-005",
                                    f"apiKeyHelper script not executable: {helper_path}",
                                    fix_command=f"chmod +x {helper_path}",
                                )
                        return self.passed("AUTH-005", "apiKeyHelper configured", value=str(helper))
                except (json.JSONDecodeError, KeyError, TypeError):
                    pass

        return self.passed("AUTH-005", "No apiKeyHelper configured (using env var or OAuth)")
