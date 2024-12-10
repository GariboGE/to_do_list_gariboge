from conftest import *

def test_password_hash():
    password = "SuperSecret"
    hashed_password = generate_password_hash(password)
    assert password != hashed_password
    assert hashed_password.startswith('scrypt:')
