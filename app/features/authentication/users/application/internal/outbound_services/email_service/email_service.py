from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    async def send_password_reset(self, email: str, reset_code: str) -> None:
        """Send a password reset code to the given email address."""
        raise NotImplementedError
