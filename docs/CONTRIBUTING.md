# Contribution Guidelines

Thank you for your interest in contributing to the GCP Generative AI ADK Scaffold! We welcome contributions from the community. By contributing, you agree to abide by the project's Code of Conduct.

## How to Contribute

1.  **Get Access:** Obtain access to the private GitLab repository.
2.  **Clone the Repository:** Clone the repository to your local machine.
    ```bash
    git clone YOUR_GITLAB_REPOSITORY_URL
    cd gcp-genai-adk-scaffold # Adjust directory name if different
    ```
3.  **Set up the Development Environment:**
    *   Ensure you have Python 3.8+ and Poetry installed.
    *   Install project dependencies, including development dependencies:
        ```bash
        poetry install
        ```
    *   Set up the pre-commit hooks:
        ```bash
        poetry run pre-commit install
        ```
    *   Ensure you have the Google Cloud SDK and Docker installed if you plan to work on deployment or provisioning features.
4.  **Create a Branch:** Create a new branch for your contribution. Use a descriptive name (e.g., `feat/add-new-tool`, `fix/cloud-run-bug`).
    ```bash
    git checkout -b your-feature-branch-name
    ```
5.  **Make Your Changes:** Implement your feature or bug fix.
    *   Follow the project's code style (enforced by pre-commit hooks).
    *   Write tests for your changes.
    *   Update documentation as necessary (README, ADRs, feature cards, etc.).
6.  **Run Tests:** Ensure all tests pass before committing.
    ```bash
        poetry run cli test
    ```
7.  **Commit Your Changes:** Commit your changes with clear and concise commit messages. Pre-commit hooks will run automatically to check code quality.
    ```bash
    git add .
    git commit -m "feat: Add a new awesome feature"
    ```
8.  **Push Your Branch:** Push your branch to the GitLab repository.
    ```bash
    git push origin your-feature-branch-name
    ```
9.  **Create a Merge Request:** Open a Merge Request from your branch to the main branch in the GitLab UI.
    *   Provide a clear title and description for your Merge Request, explaining the changes and why they are necessary.
    *   Reference any related issues.
    *   Ensure all automated checks (CI/CD, if configured) pass on your Merge Request.

## Code Style

We use `black` for code formatting, `isort` for sorting imports, and `flake8` for linting. These are enforced by pre-commit hooks. Simply commit your code, and pre-commit will automatically format and check it.

## Testing

All new code should have appropriate unit and/or integration tests written using `pytest`. Run tests locally using `poetry run cli test`.

## Documentation

*   **ADRs:** For significant architectural decisions, propose an Architecture Decision Record in the `docs/adrs/` directory.
*   **Feature Cards:** For new features, create or update a feature card in the `docs/features/` directory.
*   **README:** Update the main `README.md` with any relevant information for users.
*   **Other Docs:** Update the detailed plan, glossary, troubleshooting guide, or maintenance strategy as needed.

## Code of Conduct

Please review and abide by the project's Code of Conduct (link to CODE_OF_CONDUCT.md if it exists, otherwise state that contributors are expected to treat each other with respect).

By following these guidelines, you help ensure a smooth and collaborative contribution process. Thank you for contributing!
