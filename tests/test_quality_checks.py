"""Tests for data quality checks."""

from __future__ import annotations

import pytest


def test_test_suite_runs() -> None:
    assert True


@pytest.mark.skip(reason="not implemented yet")
def test_find_missing_values() -> None:
    raise NotImplementedError


@pytest.mark.skip(reason="not implemented yet")
def test_find_duplicate_reporting_keys() -> None:
    raise NotImplementedError


@pytest.mark.skip(reason="not implemented yet")
def test_find_out_of_range_values() -> None:
    raise NotImplementedError
