# Changelog

All notable changes to this project are written here. The release workflow copies the
section of the version being released into the GitHub release notes, so each release
needs its own `## [x.y.z]` heading.

## [Unreleased]

## [1.0.0] - 2026-10-24

### Added
- Expense API with `/health`, `/expenses`, `/summary` and `/version` endpoints
- Dockerfile and docker-compose setup, data kept in a named volume
- Pipeline that lints, tests, builds the image and smoke tests the running container
- Tagged releases publish the image to GitHub Container Registry and create a GitHub release
  with these notes
