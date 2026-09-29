"""Generate a password hash for the ADMIN_PASSWORD_HASH environment variable.

Usage:
    python scripts/hash_password.py "your-chosen-password"
"""
import sys

from werkzeug.security import generate_password_hash

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/hash_password.py <password>")
        sys.exit(1)

    print(generate_password_hash(sys.argv[1]))
