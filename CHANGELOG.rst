
Changelog
=========

0.6.0 (2026-02-17)
-----------------------------------------

* Added ``system_version`` support (maps to ``sdr_p``).
* Added ``raw_opts`` support for additional API fields.
* Added fallback so ``account_name`` populates ``sdr_o`` when ``account_id`` is unset.
* Added integration tests covering the above API-documented payload fields.

0.5.0 (2026-02-17)
-----------------------------------------

* Added ``TotangoTracker`` with JS tracker-style methods.
* Added US/EU region endpoint selection.
* Added optional API token headers for tracker requests.
* Added behavior tests for JS parity method mapping.

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
