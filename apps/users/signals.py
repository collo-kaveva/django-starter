import logging

from allauth.account.signals import password_reset
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(password_reset)
def handle_password_reset_email_sent(sender, request, email, **kwargs):
    """
    Log when password reset emails are sent and handle any failures.
    """
    logger.info(f"Password reset email sent to {email}")
    # Success message is already handled by allauth templates
    # This signal is primarily for logging and monitoring
