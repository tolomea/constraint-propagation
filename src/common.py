import re


def get_user_input(prompt, pattern=None, convert=None):
    while True:
        value = input(f"{prompt}: ")
        if not value:
            continue
        if pattern:
            if not re.fullmatch(pattern, value):
                print(f"Does not match '{pattern}'")  # noqa: T201
                continue
        if convert:
            try:
                value = convert(value)
            except Exception as e:
                print(e)  # noqa: T201
                continue
        return value


def get_test_input(lines):
    lines = list(lines)

    def inner(prompt, pattern=None, convert=None):
        value = lines.pop(0)
        if pattern:
            assert re.fullmatch(pattern, value), (pattern, value)
        if convert:
            value = convert(value)
        return value