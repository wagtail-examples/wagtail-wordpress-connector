# Changelog

All notable changes to the WordPress to Wagtail Connector will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Complete documentation including setup guide, field mapping guide, and troubleshooting guide
- Make commands for simplifying project setup and management
- Project structure documentation

### Changed

- Updated documentation to use make commands instead of uv run commands
- Improved field processor for handling richtext content

### Fixed

- Fixed typos and inconsistencies in documentation
- Fixed page hierarchy issues with better parent-child relationship handling

## [0.1.0] - 2025-05-21

### Added

- Initial release with basic WordPress to Wagtail migration functionality
- Support for posts, pages, authors, categories, tags, and comments
- Django admin interface for managing imports
- Wagtail integration for viewing imported content
- Docker setup for WordPress test instance
