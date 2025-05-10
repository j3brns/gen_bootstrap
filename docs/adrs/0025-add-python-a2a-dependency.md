# ADR 0025: Add `python-a2a` Dependency

**Status:** Superseded
**Reason:** A2A functionality and general agent tool use are now intended to be handled via the `google-adk` dependency.

**Date:** 2025-04-22

**Context:**

The project aims to implement tool-use capabilities for its generative AI agent (ADR-0014). The Google A2A (Ask-Anything Augmentation) library (`github.com/google/A2A`) was considered as a potential component for facilitating this. Initial attempts to add A2A directly via its Git URL using `poetry add git+https://github.com/google/A2A` failed because the repository lacks standard Python packaging files (`pyproject.toml` or `setup.py`) at its root.

A package named `python-a2a` exists on PyPI (`https://pypi.org/project/python-a2a/`). While its direct lineage to `google/A2A` requires verification during implementation, it presents a potentially installable alternative via standard package management.

**Decision:**

We decided to add the `python-a2a` package from PyPI as a dependency to the project using Poetry. The command `poetry add python-a2a` was executed successfully, adding `python-a2a = "^0.4.0"` to the `[tool.poetry.dependencies]` section in `pyproject.toml` and updating `poetry.lock`.

**Consequences:**

*   **Positive:**
    *   Successfully adds a potential A2A library implementation to the project environment.
    *   Maintains dependency management consistency using Poetry.
*   **Neutral:**
    *   Adds another dependency to the project.
    *   The exact functionality and origin alignment of `python-a2a` compared to `google/A2A` needs confirmation during development/integration.
*   **Negative:**
    *   If `python-a2a` is not the intended library or has issues, it may need to be replaced or removed later.
