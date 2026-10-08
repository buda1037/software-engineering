"""Unit tests for the hello-world greeting functions."""

from hello_world import get_hello_world, print_hello_world


def test_get_hello_world():
    assert get_hello_world() == "Hello World"


def test_print_hello_world(capsys):
    print_hello_world()
    assert capsys.readouterr().out == "Hello World\n"
