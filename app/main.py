import string
import secrets
import sys

from P4 import P4, P4Exception

p4 = P4()


class P4PasswordException(P4Exception):
    pass


def main(username: str) -> None:
    init()
    print(f"Resetting password for {username}")
    new_password = set_temporary_password(username)
    print()
    print(f"----------------------------------")
    print(f"Username: {username}")
    print(f"Password: {new_password}")
    print(f"----------------------------------")


def set_temporary_password(user: str) -> str:
    new_password = generate_password(10)
    print(f"Setting new password: {new_password}")
    p4.input = new_password
    res = p4.run("passwd", user)
    res += p4.run("admin", "resetpassword", "-u", user)
    print(f"{res}")
    return new_password


def generate_password(length: int) -> str:
    """Generate password with at least one of each: lowercase, uppercase, digit."""
    alphabet = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alphabet) for i in range(length))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
        ):
            return password


def disconnect() -> None:
    if p4.connected():
        p4.disconnect()


def init(username=None, port=None, password=None):
    if port and p4.port != port:
        disconnect()
        p4.port = port or p4.port
    p4.user = username or p4.user
    if not p4.connected():
        p4.connect()
    try:
        p4.run_login("-s")
    except P4Exception as e:
        if not password:
            raise e
        # If not logged in already, try with the password.
        p4.password = password
        try:
            p4.run_login()
        except P4Exception as e:
            if "invalid or unset" in e.errors[0]:
                raise e
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: p4-reset-user-password <username>")
        sys.exit(1)
    main(sys.argv[1])
    disconnect()
