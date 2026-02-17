
Changelog
=========

0.5.0 (2026-02-17)
-----------------------------------------

* Added ``TotangoTracker`` with JS tracker-style methods.
* Added US/EU region endpoint selection.
* Added optional API token headers for tracker requests.
* Added behavior tests for JS parity method mapping.

0.4.0 (2026-02-17)
-----------------------------------------

* Added official support for Python 3.10+ (through 3.15 in CI matrix validation).
* Migrated packaging metadata to ``pyproject.toml`` with modern build configuration.
* Added Python 3 compatibility fixes and typed public APIs.
* Fixed payload construction for per-call ``user_id`` overrides.
* Added behavior-focused integration tests for payload generation and HTTP error handling.
* Added ``ruff`` and ``ty`` configuration and aligned tooling to Python 3.10 compatibility.
* Added ``tox`` environments for Python 3.10 through 3.15 plus lint/type checks.
* Added GitHub Actions CI matrix, coverage report generation, and Codecov uploads.
* Added tag-triggered release workflow to create GitHub Releases and publish to PyPI.

0.3.2 (2017-06-1)
-----------------------------------------

* Updates to the setup script so that requests doesn't need to be installed
  manually

0.3.1 (2017-06-1)
-----------------------------------------

* Licensing and ownership change

0.3.0 (2014-05-02)
-----------------------------------------

* Set the user agent correctly when sending data to totango

0.2 (2014-04-30)
-----------------------------------------

* Fixed some typos in payload keys

0.1 (2014-04-30)
-----------------------------------------

* Initial Release
