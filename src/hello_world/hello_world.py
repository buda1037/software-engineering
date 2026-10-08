"""Hello-world greeting functions."""


def get_hello_world() -> str:
    """Return the greeting."""
    return "Hello World"


def print_hello_world() -> None:
    """Print the greeting."""
    print(get_hello_world())


def main() -> None:
    """Run the program."""
    print_hello_world()
