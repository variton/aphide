"""Unit tests for environment variable loading."""

import pytest

from xphide.envvar_loader import load


@pytest.mark.parametrize("explicit_none", [False, True])
def test_load_default_variable(monkeypatch, explicit_none):
    """Use SJWTK when the argument is omitted or explicitly None."""
    monkeypatch.setenv("SJWTK", "default-secret")

    assert (load(None) if explicit_none else load()) == "default-secret"


def test_load_custom_variable(monkeypatch):
    """Use the requested variable even when SJWTK is also present."""
    monkeypatch.setenv("SJWTK", "default-secret")
    monkeypatch.setenv("XPHIDE_TEST_SECRET", "custom-secret")

    assert load("XPHIDE_TEST_SECRET") == "custom-secret"


@pytest.mark.parametrize("envvar", [None, "XPHIDE_TEST_SECRET"])
def test_load_missing_variable(monkeypatch, envvar):
    """Return None when the requested variable is absent."""
    monkeypatch.setenv("SJWTK", "default-secret")
    monkeypatch.delenv(envvar if envvar is not None else "SJWTK", raising=False)

    assert load(envvar) is None


@pytest.mark.parametrize("envvar", [None, "XPHIDE_TEST_SECRET"])
def test_load_empty_variable(monkeypatch, envvar):
    """Preserve an empty value instead of treating it as missing."""
    monkeypatch.setenv(envvar if envvar is not None else "SJWTK", "")

    assert load(envvar) == ""
