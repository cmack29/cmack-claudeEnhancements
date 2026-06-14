"""
messaging.py — Create, validate, and send messages.
"""

import uuid
from datetime import datetime, timezone

from storage import save_message
from validate import validate_input


def create_message(sender: str, recipient: str, body: str) -> dict:
    """
    Build a message dict with a unique ID and UTC timestamp.

    Does NOT persist — call send_message() for the full pipeline.
    """
    return {
        "id":        str(uuid.uuid4()),
        "sender":    sender,
        "recipient": recipient,
        "body":      body,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "read":      False,
    }


def send_message(sender: str, recipient: str, body: str) -> dict:
    """
    Full send pipeline: validate → create → persist.

    Args:
        sender:    Username of the sender.
        recipient: Username of the intended recipient.
        body:      Raw message text from user input.

    Returns:
        The saved message dict.

    Raises:
        ValueError: If input fails validation (propagated from validate_input).
    """
    validate_input(sender=sender, recipient=recipient, body=body)
    message = create_message(sender, recipient, body)
    return save_message(message)