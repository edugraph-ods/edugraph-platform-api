import smtplib
from email.message import EmailMessage

from app.features.authentication.application.internal.outbound_services.email_service.email_service import EmailService


class SMTPEmailService(EmailService):
    def __init__(self, host: str, port: int, username: str, password: str, sender: str | None = None) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sender = sender or username

    async def send_password_reset(self, email: str, reset_code: str) -> None:
        message = EmailMessage()
        message["Subject"] = "Password Reset Request"
        message["From"] = self.sender
        message["To"] = email
        message.set_content(
            "Hola,\n\nHas solicitado restablecer tu contraseña. "
            f"Ingresa el siguiente código de verificación para completar el proceso: {reset_code}\n\n"
            "Si no solicitaste este cambio, ignora este mensaje."
        )

        with smtplib.SMTP_SSL(self.host, self.port) as smtp:
            smtp.login(self.username, self.password)
            smtp.send_message(message)
