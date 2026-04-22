import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import urllib.parse
from app.utils.config import settings

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM

    def send_email(self, to_email: str, subject: str, body: str, is_html: bool = False):
        """
        Envía un correo electrónico
        """
        if not self.username or not self.password:
            logger.warning("⚠️ Credenciales SMTP no configuradas. No se enviará el correo.")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html' if is_html else 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Correo enviado a {to_email}")
            return True
        except Exception as e:
            logger.error(f"❌ Error enviando correo: {e}")
            return False

    def generate_whatsapp_link(self, phone_number: str, message: str) -> str:
        """
        Genera un enlace de WhatsApp para enviar un mensaje manualmente
        """
        base_url = "https://wa.me/"
        # Limpiar número (eliminar espacios, +, etc)
        clean_number = "".join(filter(str.isdigit, phone_number))
        
        encoded_message = urllib.parse.quote(message)
        return f"{base_url}{clean_number}?text={encoded_message}"

    def send_whatsapp_test(self, phone_number: str, message: str):
        """
        Simula el envío de WhatsApp generando el link
        """
        link = self.generate_whatsapp_link(phone_number, message)
        logger.info(f"📱 Enlace de WhatsApp generado para {phone_number}:")
        logger.info(link)
        return link
