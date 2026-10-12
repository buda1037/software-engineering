"""Unit tests for the hello-world greeting functions."""

lazy import pytest

from hello_world import get_hello_world, print_hello_world


def test_get_hello_world() -> None:
    assert get_hello_world() == "Hello World"


def test_print_hello_world(capsys: pytest.CaptureFixture[str]) -> None:
    print_hello_world()
    assert capsys.readouterr().out == "Hello World\n"
