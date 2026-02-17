# Totango Python Modernization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Modernize the library for Python 3.14+, ship test coverage, and deliver three incremental pull requests.

**Architecture:** Keep the existing `Totango` class/API stable while incrementally adding capabilities. Use behavior-focused integration tests around HTTP payload generation and request transport, then layer parity helpers and API-surface expansions.

**Tech Stack:** Python 3.14+, setuptools/PEP 621 (`pyproject.toml`), `unittest`, `requests`, Ruff, Ty.

---

### Task 1: Pass 1 baseline modernization

**Files:**
- Modify: `totango/__init__.py`
- Create: `tests/test_totango.py`
- Create: `pyproject.toml`
- Modify: `setup.py`, `CHANGELOG.rst`, `README.rst`
- Create: `README.md`

**Steps:**
1. Write integration tests for payload formation and HTTP failures.
2. Run tests to observe Python 3 failures.
3. Implement Python 3-safe dict iteration and typed signatures.
4. Migrate packaging metadata to `pyproject.toml` with `setuptools` backend.
5. Update README installation/usage examples.
6. Verify tests and build metadata locally.

### Task 2: Pass 2 feature parity with JS tracker

**Files:**
- Modify: `totango/__init__.py`
- Modify: `tests/test_totango.py`
- Modify: `README.md`

**Steps:**
1. Add failing behavior tests for region selection, API token auth header, and parity helper methods.
2. Implement parity methods while preserving existing `track` and `send` behavior.
3. Re-run tests and refine naming/docs.

### Task 3: Pass 3 HTTP API coverage

**Files:**
- Modify: `totango/__init__.py`
- Modify: `tests/test_totango.py`
- Modify: `README.md`, `CHANGELOG.rst`

**Steps:**
1. Add failing tests for additional documented request fields/helpers.
2. Implement helper APIs for missing payload capabilities with backward compatibility.
3. Run full verification and prepare final PR branch.
