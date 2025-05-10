# Maintenance Strategy

This document outlines the strategy for maintaining the GCP Generative AI ADK Scaffold and how users of the scaffold can keep their projects updated with the latest improvements and dependency versions.

## Scaffold Maintenance (by Scaffold Maintainers)

The core scaffold and its dependencies will be maintained in a central source repository (e.g., a Git repository). Maintenance activities include:

1.  **Dependency Updates:** Periodically updating project dependencies (Google Cloud SDKs, `token_count_trim`, frameworks, development tools, etc.) using Poetry commands (`poetry update`, `poetry add <package>@latest`).
2.  **SDK Wrapper Maintenance:** Reviewing release notes for core dependencies, especially Google Cloud SDKs. Updating the wrapper functions in the `utils/` module as needed to ensure compatibility with newer SDK versions, expose new features, or address breaking changes.
3.  **Bug Fixes and Improvements:** Addressing bugs and implementing new features or refinements to the scaffold structure, CLI, utilities, and documentation.
4.  **Code Quality:** Ensuring code quality standards are maintained using pre-commit hooks, testing, and code reviews.
5.  **Documentation Updates:** Keeping the project documentation (plan, ADRs, feature cards, usage guides) up-to-date with changes.
6.  **Version Tagging:** Tagging significant releases or versions of the scaffold in the source repository.

## User Update Strategy

Since the scaffold is intended as a starter kit or template rather than a library dependency, users will update their projects by pulling changes from the scaffold's source repository into their own project repository.

1.  **Initial Project Setup:** Users clone or copy the scaffold repository to start their project. They initialize their own Git repository for their project.
2.  **Pulling Updates:** Periodically, users will fetch and merge changes from the scaffold's source repository into their project's repository. This can be done using standard Git commands:
    ```bash
    # In the user's project directory
    git remote add scaffold <scaffold_repository_url> # Add the scaffold repo as a remote (one-time)
    git fetch scaffold # Fetch the latest changes from the scaffold remote
    git merge scaffold/main # Merge changes from the scaffold's main branch (or relevant branch/tag)
    ```
3.  **Resolving Merge Conflicts:** Users will need to manually resolve any merge conflicts that arise if they have customized files that have also been changed in the scaffold.
4.  **Installing Updated Dependencies:** After merging changes that include updates to `pyproject.toml` or `poetry.lock`, users must run `poetry install` in their project directory to install the new dependency versions.
5.  **Reviewing Changes:** Users should review the scaffold's release notes or commit history to understand the changes they are pulling and any potential impact on their project.

## Dependency Management (Poetry and Git)

*   **`pyproject.toml`:** Defines the project's direct dependencies and metadata. Scaffold maintainers update this file. Users get updates by merging.
*   **`poetry.lock`:** Pins the exact versions of all dependencies for reproducible builds. Scaffold maintainers update this file using `poetry update` or `poetry add`. Users get updates by merging and then running `poetry install`.
*   **Git:** Used by both maintainers to track scaffold evolution and by users to pull updates into their projects.

## SDK Wrapper Maintenance Strategy

The `utils/` module acts as a wrapper layer over the Google Cloud SDKs.

1.  **Scaffold Maintainers' Role:** Maintainers monitor updates to the core Google Cloud SDKs used by the scaffold. They update the SDK versions in `pyproject.toml` and `poetry.lock`. They review SDK release notes and test/update the wrapper functions in `utils/` to ensure compatibility and expose relevant new features.
2.  **Users' Benefit:** By pulling updates from the scaffold, users automatically receive the latest compatible SDK versions (via `poetry install`) and the updated `utils/` wrappers that work with those versions. This shields users from needing to directly track and adapt to all underlying SDK changes themselves, as the scaffold maintainers handle the initial compatibility work in the wrappers.

## Challenges

*   Merging changes from the scaffold into a customized user project can require manual conflict resolution.
*   Users need to be proactive in pulling updates from the scaffold repository.

This strategy aims to provide a clear process for maintaining the scaffold and enabling users to incorporate updates into their projects, leveraging Poetry and Git for dependency and code management.
