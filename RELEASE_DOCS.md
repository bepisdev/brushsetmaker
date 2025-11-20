# How to prepare a release

1. Commit all changes
2. Increment version in the following files
    - `pyproject.toml`
    - `brushsetmaker.dist-info/METADATA`
    - `brushsetmaker/__init__.py`
3. `make build`
4. `make package`
5. `create tag and release on github`
6. `upload .dmg to release`