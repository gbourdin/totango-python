
Changelog
=========

0.4.1 (2026-02-17)
-----------------------------------------

* Lowered support floor to Python 3.10+.
* Added tox environments for Python 3.10 through 3.15.
* Added a GitHub Actions matrix to run tests across supported Python versions.
* Added coverage report generation in test jobs and Codecov upload integration.
* Updated Ruff and Ty target versions to enforce Python 3.10 compatibility.

0.4.0 (2026-02-17)
-----------------------------------------

* Added Python 3 compatibility fixes and typed public APIs.
* Fixed payload construction for per-call ``user_id`` overrides.
* Added integration tests covering payload shape and HTTP error handling.
* Migrated packaging metadata to ``pyproject.toml``.
* Added ``ruff`` and ``ty`` configuration for linting and type checks.

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
