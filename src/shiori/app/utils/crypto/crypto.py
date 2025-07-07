from passlib.context import CryptContext


class Crypto:

    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encrypt(self, secret: str) -> str:
        """
        password hashing
        :param secret: password
        :return: hashed password
        """
        return self._pwd_context.encrypt(secret)

    def verify(self, password: str, hashed: str) -> bool:
        """
        password verification
        :param password: password
        :param hashed: hashed password
        :return: True if password matches hashed password, False otherwise
        """
        return self._pwd_context.verify(password, hashed)
