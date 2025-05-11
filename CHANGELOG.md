# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (though not formally versioning releases yet).

## [Unreleased] - 2025-05-11

### Added
- **CLI Enhancements:**
    - `setup-gcp` command: Added interactive mode (`--interactive`) for step-by-step confirmations.
    - `deploy` command: Integrated optional pre-deployment test execution via `--run-tests` flag; deployment aborts on test failure.
    - New `monitoring` command group (`gen-bootstrap monitoring`):
        - `monitoring setup`: Verifies Cloud Monitoring API status and provides setup guidance.
        - Added stubs for future `monitoring dashboard` and `monitoring alerts` commands.
- **Testing:**
    - Comprehensive tests for the `gen-bootstrap test` CLI command, covering various options and scenarios (`tests/cli/test_main_cli.py`).
    - Tests for timezone support in the `get_current_time_async` tool (`tests/tools/test_example_tool.py`).
    - Tests for agent configuration (model and tools) in `adk/agent.py` (`tests/adk/test_agent.py`).

### Changed
- **CLI Enhancements:**
    - `setup-gcp` command: Now also grants the `roles/secretmanager.secretAccessor` IAM role to the default Compute Engine service account.
- **Dependency Management:**
    - `pyproject.toml`: Updated placeholder author details to actual maintainer. Removed several stale comments related to dependency versions.
- **Documentation:**
    - `README.md`: Updated the "Roadmap" section to more accurately reflect current project status (Beta phase, initial Gamma work) and next steps.
    - `docs/plan/detailed_plan.md`: Updated the "Current Status (May 2025)" summary and various `[TODO]`/`[IN PROGRESS]` markers to reflect completed and ongoing work.

### Fixed
- **Code Quality:**
    - Addressed Flake8 errors in `cli/main.py` following enhancements to `setup-gcp` and `deploy` commands.
    - Refactored duplicate code in `cli/tools_cli.py` by having `list_tools` utilize the `_discover_tools` helper function.
    - Resolved Flake8 errors in `cli/tools_cli.py` after refactoring.
    - Ensured new and modified CLI modules (`cli/monitoring_cli.py`) and test files are lint-free after creation/modification.
