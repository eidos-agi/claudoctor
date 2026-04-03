"""Output formatters — summary, verbose, and JSON modes."""

from __future__ import annotations

import json
from typing import TextIO

import click

from claudoctor.models import Finding, SectionResult, Severity, Status


def _severity_color(severity: Severity) -> str:
    return {"error": "red", "warn": "yellow", "info": "green"}[severity.value]


def _status_icon(status: Status) -> tuple[str, str]:
    """Return (icon, color) for a status."""
    return {
        Status.PASS: ("✓", "green"),
        Status.WARN: ("!", "yellow"),
        Status.FAIL: ("✗", "red"),
        Status.SKIP: ("-", "dim"),
    }[status]


def print_summary(sections: list[SectionResult], verbose: bool = False) -> None:
    """Print flutter-doctor-style summary."""
    from claudoctor import __version__

    click.echo(f"\nclaudoctor v{__version__}\n")

    total_errors = 0
    total_warnings = 0
    total_passed = 0

    for section in sections:
        icon, color = _status_icon(section.status)

        # Summary line
        label = f"[{icon}] {section.name}"
        dots = "." * max(1, 40 - len(label))
        summary = f"{section.passed}/{section.total} passed"

        extras = []
        if section.errors > 0:
            extras.append(click.style(f"{section.errors} error{'s' if section.errors > 1 else ''}", fg="red"))
        if section.warnings > 0:
            extras.append(click.style(f"{section.warnings} warning{'s' if section.warnings > 1 else ''}", fg="yellow"))
        if extras:
            summary += f" ({', '.join(extras)})"

        click.echo(f"  {click.style(f'[{icon}]', fg=color)} {section.name} {click.style(dots, dim=True)} {summary}")

        # Verbose: show each finding
        if verbose:
            for finding in section.findings:
                f_icon, f_color = _status_icon(finding.status)
                prefix = click.style(f"    [{f_icon}]", fg=f_color)
                click.echo(f"{prefix} {finding.check_id}: {finding.message}")

                if finding.value:
                    click.echo(click.style(f"        Value: {finding.value}", dim=True))
                if finding.detail:
                    click.echo(click.style(f"        {finding.detail}", dim=True))
                if finding.fix_command:
                    click.echo(f"        Fix: {click.style(finding.fix_command, fg='cyan')}")
                    if finding.fix_description:
                        click.echo(click.style(f"        ({finding.fix_description})", dim=True))
            click.echo()

        total_errors += section.errors
        total_warnings += section.warnings
        total_passed += section.passed

    # Score
    total_checks = sum(s.total for s in sections)
    score = round((total_passed / total_checks * 100)) if total_checks > 0 else 0

    click.echo()
    parts = [f"Score: {score}/100"]
    if total_errors > 0:
        parts.append(click.style(f"{total_errors} error{'s' if total_errors > 1 else ''}", fg="red"))
    if total_warnings > 0:
        parts.append(click.style(f"{total_warnings} warning{'s' if total_warnings > 1 else ''}", fg="yellow"))
    if not verbose and (total_errors > 0 or total_warnings > 0):
        parts.append("Run claudoctor -v for details")

    click.echo(f"  {' | '.join(parts)}")
    click.echo()


def print_json(sections: list[SectionResult], output: TextIO | None = None) -> None:
    """Print machine-readable JSON output."""
    data = {
        "version": "0.1.0",
        "sections": [],
        "summary": {
            "total": 0,
            "passed": 0,
            "warnings": 0,
            "errors": 0,
            "score": 0,
        },
    }

    for section in sections:
        section_data = {
            "name": section.name,
            "status": section.status.value,
            "findings": [],
        }
        for finding in section.findings:
            finding_data = {
                "check_id": finding.check_id,
                "severity": finding.severity.value,
                "status": finding.status.value,
                "message": finding.message,
            }
            if finding.detail:
                finding_data["detail"] = finding.detail
            if finding.fix_command:
                finding_data["fix_command"] = finding.fix_command
            if finding.value:
                finding_data["value"] = finding.value
            section_data["findings"].append(finding_data)

        data["sections"].append(section_data)
        data["summary"]["total"] += section.total
        data["summary"]["passed"] += section.passed
        data["summary"]["warnings"] += section.warnings
        data["summary"]["errors"] += section.errors

    total = data["summary"]["total"]
    data["summary"]["score"] = round((data["summary"]["passed"] / total * 100)) if total > 0 else 0

    result = json.dumps(data, indent=2)
    if output:
        output.write(result)
    else:
        click.echo(result)
