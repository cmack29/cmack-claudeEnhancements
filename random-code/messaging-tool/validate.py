"""
validate.py — Validate message fields before they reach storage.
"""

MAX_BODY_LENGTH = 2000
MAX_NAME_LENGTH = 50


def validate_input(sender: str, recipient: str, body: str) -> None:
    """
    Validate all fields for a new message.

    Raises:
        ValueError: With a human-readable description of what's wrong.
    """
    _validate_username(sender, field="sender")
    _validate_username(recipient, field="recipient")
    _validate_body(body)


def _validate_username(value: str, field: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field} cannot be empty.")
    if len(value) > MAX_NAME_LENGTH:
        raise ValueError(
            f"{field} is too long ({len(value)} chars); max is {MAX_NAME_LENGTH}."
        )
    if not value.replace("_", "").replace("-", "").isalnum():
        raise ValueError(
            f"{field} can only contain letters, numbers, hyphens, and underscores."
        )


def _validate_body(body: str) -> None:
    if not body or not body.strip():
        raise ValueError("Message body cannot be empty.")
    if len(body) > MAX_BODY_LENGTH:
        raise ValueError(
            f"Message is too long ({len(body)} chars); max is {MAX_BODY_LENGTH}."
        )