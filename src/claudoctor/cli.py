"""claudoctor CLI — the definitive diagnostic tool for Claude Code."""

from __future__ import annotations

import sys

import click

from claudoctor import __version__


@click.command()
@click.version_option(__version__, prog_name="claudoctor")
@click.option("-v", "--verbose", is_flag=True, help="Show detailed sub-check results")
@click.option("--json", "json_output", is_flag=True, help="Machine-readable JSON output")
@click.option("--fix", is_flag=True, help="Apply safe, reversible auto-fixes")
@click.option(
    "--section",
    type=str,
    default=None,
    help="Run only a specific section (e.g., mcp, hooks, disk)",
)
@click.option(
    "--project",
    type=click.Path(exists=True),
    default=".",
    help="Project directory to diagnose (default: current directory)",
)
def main(verbose: bool, json_output: bool, fix: bool, section: str | None, project: str) -> None:
    """The definitive diagnostic tool for Claude Code.

    Finds what's slowing you down and fixes it.
    """
    from claudoctor.registry import build_runner
    from claudoctor.output import print_summary, print_json

    runner = build_runner()

    if section:
        result = runner.run_section(section)
        if result is None:
            click.echo(f"Unknown section: {section}", err=True)
            click.echo("Available sections: install, auth, project, settings, permissions, "
                       "claudemd, skills, mcp, hooks, memory, disk, processes", err=True)
            sys.exit(2)
        sections = [result]
    else:
        sections = runner.run_all()

    if json_output:
        print_json(sections)
    else:
        print_summary(sections, verbose=verbose)

    # Exit code: 1 if any errors
    has_errors = any(s.errors > 0 for s in sections)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
