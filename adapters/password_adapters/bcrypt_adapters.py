import bcrypt

from domain_layer.abstractions.password_manager_interface import IPasswordHandler


class PasswordHandler(IPasswordHandler):
    """
    Implementation of IPasswordManager interface
    """
    def hash_password(self, password: str) -> str:
        """
        Function to hash a password
        Args:
            password: string to hash

        Returns:
            str: hashed password

        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Function to verify a hashed password
        Args:
            password:
            hashed_password:

        Returns:
            bool: True if the hashed password is correct, False otherwise

        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
