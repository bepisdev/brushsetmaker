---
layout: page
title: Preparing a Release
toc: true
---

## Git Flow Release Workflow

This documentation outlines the process for preparing a release version using the Git Flow workflow.

### Overview

Git Flow is a branching model that defines a strict branching structure designed around project releases. The release workflow helps maintain clean, organized code while preparing for production deployments.

### Release Preparation Steps

1. **Start a Release Branch**
    ```bash
    git flow release start <version>
    ```
    Creates a new release branch from `develop`. Use semantic versioning (e.g., 1.2.0).

2. **Prepare Release Changes**
    - Update version numbers in the following files
        - `pyproject.toml` (lines `3` and `17`)
        - `src/brushsetmaker.dist-info/METADATA` (line `6`)
        - `src/brushsetmaker/__init__.py` (line `2`)

3. **Commit Release Changes**
    ```bash
    git add .
    git commit -m "Bump version to <version>"
    ```

4. **Finish the Release**
    ```bash
    git flow release finish <version>
    ```
    This will:
    - Merge the release branch into `main`
    - Tag the release with the version number
    - Merge back into `develop`
    - Delete the release branch

5. **Push Changes**
    ```bash
    git push origin main
    git push origin develop
    git push --tags
    ```

6. **Build the Release Package**
    ```bash
    make build
    make package
    ```
    This will:
    - Generate a `BrushsetMaker.app` in `build/brushsetmaker/macos/app/`
    - Generate a `BrushsetMaker-<version>.dmg` in `dist/`

7. **Create Release on Github**
    - Label the release as the version number
    - Fill out the release notes with the changelog
    - Upload the `.dmg` and a compressed version (`.zip`) of the `.app` to the release artifacts.

### Best Practices

- Keep release branches short-lived (hours to days, not weeks)
- Only fix critical bugs on release branches
- Never start new features on a release branch
- Always tag releases with semantic version numbers
- Update documentation before finishing the release