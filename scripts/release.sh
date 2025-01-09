#!/bin/bash

# Exit on error
set -e

# Get the new version
if [ -z "$1" ]; then
    echo "Please provide a version number (e.g. 0.1.0)"
    exit 1
fi
VERSION=$1

# Update version in version.py
echo "Updating version to $VERSION"
echo "__version__ = \"$VERSION\"" > intelliagent/version.py

# Update CHANGELOG.md
echo "Please update CHANGELOG.md and press enter"
read

# Create git tag
git add intelliagent/version.py CHANGELOG.md
git commit -m "Release version $VERSION"
git tag -a "v$VERSION" -m "Version $VERSION"

# Build distribution
echo "Building distribution..."
python -m build

# Upload to PyPI
echo "Uploading to PyPI..."
python -m twine upload dist/*

echo "Release $VERSION completed!"
