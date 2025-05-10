# 21. Use Poetry for Packaging

## Status

Accepted

## Context

To deploy the application to Cloud Run via a Docker container, the project code and its dependencies need to be packaged in a way that can be easily installed within the container image. We need a defined strategy for creating this distributable package.

## Decision

We will use Poetry's built-in packaging capabilities to create standard Python distributions (specifically wheels) that will be installed within the Docker container during the image build process.

## Consequences

*   **Benefits:**
    *   Leverages Poetry's existing functionality, aligning with our chosen dependency manager.
    *   Creates standard Python package formats (wheels) that are efficient to install.
    *   Simplifies the Dockerfile, as `poetry install` can install the project directly from the source code copied into the container.
    *   No need for separate packaging tools like `setup.py` or `setup.cfg`.
*   **Drawbacks:**
    *   Requires Poetry to be installed within the Docker build environment.
    *   Users who want to publish reusable components from their project to PyPI or other repositories would still need to use Poetry's publishing features or potentially tools like `twine` (though this is outside the scope of the scaffold's core lifecycle).
*   **Impact on Plan:**
    *   The `Dockerfile` will include steps to install Poetry and then install the project and its dependencies using `poetry install --no-dev`.
    *   The `pyproject.toml` file defines the project metadata necessary for packaging.
    *   The CLI `deploy` command orchestrates the Docker build process which includes this packaging and installation step.
    *   Documentation will explain that Poetry handles the packaging for deployment.
