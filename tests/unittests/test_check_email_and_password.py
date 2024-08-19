import pytest
import bcrypt
from abc import ABC, abstractmethod

"""
Function Id: 53
Function to check if email exists in Database and compare password with the hashed password in Database
"""


def is_email_valid(email: str, db_email: str) -> bool:
    # check if email doesn't exist in database  
    if db_email == "":
        return True
    # check if input email and database email doesn't match
    elif db_email != email:
        return True
    # check if input email and database email is same 
    elif db_email == email:
        return False
    else:
        return False


# abstract method for password hash
class PasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def check_password(self, password: str, hashed: str) -> bool:
        pass


# implement abstract methods
class BcryptPasswordHasher(PasswordHasher):
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def check_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


# Fixtures for testing
@pytest.fixture
def password():
    return "mysecretpassword"


@pytest.fixture
def password_hasher():
    return BcryptPasswordHasher()


@pytest.fixture
def hashed_password(password, password_hasher):
    return password_hasher.hash_password(password)


class TestCheckEmailAndPassword:
    # mock input for email
    def test_check_if_email_is_empty(self):
        assert is_email_valid("test@example.com", "") is True

    def test_check_if_email_is_not_same_as_input(self):
        assert is_email_valid("test@example.com", "test1@gmail.com") is True

    def test_check_if_email_is_same_as_input(self):
        assert is_email_valid("test@example.com", "test@example.com") is False

    # mock input for password
    def test_password_match(self, password, hashed_password, password_hasher):
        assert password_hasher.check_password(password, hashed_password) is True, "The password should match the hash."

    def test_password_does_not_match(self, password, hashed_password, password_hasher):
        wrong_password = "wrongpassword"
        assert password_hasher.check_password(wrong_password,
                                              hashed_password) is False, "The password should not match the hash."
