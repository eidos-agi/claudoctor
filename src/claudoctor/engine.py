"""Check engine — discovers, runs, and collects diagnostic checks."""

from __future__ import annotations

from claudoctor.models import Finding, SectionResult, Severity


class Check:
    """Base class for all diagnostic checks.

    Subclasses must set section and implement run().
    """

    section: str = ""  # e.g., "Installation", "MCP Servers"

    def run(self) -> list[Finding]:
        """Run the check and return findings."""
        raise NotImplementedError

    def passed(self, check_id: str, message: str, value: str = "") -> Finding:
        return Finding(
            check_id=check_id,
            severity=Severity.INFO,
            message=message,
            value=value,
        )

    def warn(
        self,
        check_id: str,
        message: str,
        detail: str = "",
        fix_command: str | None = None,
        fix_description: str | None = None,
        value: str | None = None,
    ) -> Finding:
        return Finding(
            check_id=check_id,
            severity=Severity.WARN,
            message=message,
            detail=detail,
            fix_command=fix_command,
            fix_description=fix_description,
            value=value,
        )

    def error(
        self,
        check_id: str,
        message: str,
        detail: str = "",
        fix_command: str | None = None,
        fix_description: str | None = None,
        value: str | None = None,
    ) -> Finding:
        return Finding(
            check_id=check_id,
            severity=Severity.ERROR,
            message=message,
            detail=detail,
            fix_command=fix_command,
            fix_description=fix_description,
            value=value,
        )


class CheckRunner:
    """Discovers and runs all registered checks."""

    def __init__(self) -> None:
        self._checks: list[Check] = []

    def register(self, check: Check) -> None:
        self._checks.append(check)

    def run_all(self) -> list[SectionResult]:
        sections: dict[str, SectionResult] = {}

        for check in self._checks:
            section_name = check.section
            if section_name not in sections:
                sections[section_name] = SectionResult(name=section_name)

            try:
                findings = check.run()
                sections[section_name].findings.extend(findings)
            except Exception as e:
                sections[section_name].findings.append(
                    Finding(
                        check_id=f"{section_name}-ERR",
                        severity=Severity.ERROR,
                        message=f"Check crashed: {type(e).__name__}: {e}",
                    )
                )

        # Return in registration order
        seen = []
        ordered = []
        for check in self._checks:
            if check.section not in seen:
                seen.append(check.section)
                ordered.append(sections[check.section])
        return ordered

    def run_section(self, section_name: str) -> SectionResult | None:
        result = SectionResult(name=section_name)
        found = False

        for check in self._checks:
            if check.section.lower() == section_name.lower():
                found = True
                try:
                    findings = check.run()
                    result.findings.extend(findings)
                except Exception as e:
                    result.findings.append(
                        Finding(
                            check_id=f"{section_name}-ERR",
                            severity=Severity.ERROR,
                            message=f"Check crashed: {type(e).__name__}: {e}",
                        )
                    )

        return result if found else None
