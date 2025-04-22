from abc import ABC, abstractmethod


class IPasswordManager(ABC):
    """
    Interface for password manager
    """
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """
        Function to hash a password
        Args:
            password: string to hash

        Returns:
            str: hashed password

        """
        pass

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Function to verify a password
        Args:
            password:
            hashed_password:

        Returns:
            bool: True if password matches hashed password, False otherwise

        """
        pass
