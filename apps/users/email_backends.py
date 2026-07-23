import logging

from django.core.mail.backends.smtp import EmailBackend

logger = logging.getLogger(__name__)


class LoggingEmailBackend(EmailBackend):
    """
    Custom SMTP email backend that provides enhanced logging and error handling
    for email operations including password resets and account verification emails.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log_config()

    def _log_config(self):
        """Log email configuration (without sensitive data)"""
        logger.info(f"Email backend initialized with host: {self.host}, port: {self.port}, use_tls: {self.use_tls}")
        if self.username:
            logger.info(f"Email authentication configured for user: {self.username}")

    def send_messages(self, email_messages):
        """
        Send email messages with enhanced error handling and logging.
        """
        if not email_messages:
            return 0

        num_sent = 0
        for message in email_messages:
            try:
                logger.info(f"Attempting to send email to: {message.to}")
                result = super().send_messages([message])
                if result:
                    num_sent += result
                    logger.info(f"Successfully sent email to: {message.to}")
                else:
                    logger.warning(f"Failed to send email to: {message.to}")
            except Exception as e:
                logger.error(f"Error sending email to {message.to}: {str(e)}", exc_info=True)
                # Continue with next message instead of failing all
                continue

        return num_sent
