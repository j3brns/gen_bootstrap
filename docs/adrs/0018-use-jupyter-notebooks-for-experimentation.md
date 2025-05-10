# 18. Use Jupyter Notebooks for Experimentation

## Status

Accepted

## Context

Experimentation is a critical part of developing generative AI applications, involving exploring data, testing models, prototyping prompts, and trying out different agent behaviors. We need a flexible and interactive environment that facilitates this process.

## Decision

We will include Jupyter Notebooks in the project scaffold as the primary environment for interactive experimentation and prototyping.

## Consequences

*   **Benefits:**
    *   Provides an interactive environment for step-by-step code execution and visualization.
    *   Excellent for data exploration, model interaction, and prompt prototyping.
    *   Widely used and familiar tool in the AI/ML community.
    *   Allows for combining code, output, and markdown documentation.
*   **Drawbacks:**
    *   Notebooks can sometimes lead to less structured code compared to standard Python scripts.
    *   Managing dependencies within notebooks requires care (addressed by using the Poetry environment).
    *   Large outputs can clutter the notebook files (addressed by `nbstripout` pre-commit hook).
*   **Impact on Plan:**
    *   A `notebooks/` directory will be included in the project structure.
    *   `jupyterlab` or `notebook` will be included as development dependencies in `pyproject.toml`.
    *   The CLI `init` command will guide users to install dev dependencies.
    *   A pre-commit hook (`nbstripout`) will be configured to clean notebook outputs before commits.
    *   Documentation will provide guidance on organizing notebooks and running them within the Poetry environment.
    *   Notebooks will be used to demonstrate using `utils/` functions, interacting with models/prompts, and prototyping tools.
