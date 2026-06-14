"""
cli.py — Read and route user commands from stdin.
"""

from dataclasses import dataclass


@dataclass
class Command:
    verb: str           # e.g. "send", "inbox", "delete"
    args: list[str]     # remaining tokens after the verb


def get_user_input(prompt: str = "> ") -> str | None:
    """
    Read a line from stdin.

    Returns:
        The stripped input string, or None if the user pressed Ctrl-C / Ctrl-D.
    """
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        return None


def parse_command(raw: str) -> Command | None:
    """
    Parse a raw input string into a Command.

    Expects commands prefixed with '/'.  Returns None for empty or
    non-command input (so the caller can re-prompt).

    Examples:
        "/send alice Hello there"  → Command("send", ["alice", "Hello there"])
        "/inbox"                   → Command("inbox", [])
        "/delete abc-123"          → Command("delete", ["abc-123"])
    """
    if not raw or not raw.startswith("/"):
        return None

    parts = raw[1:].split(maxsplit=1)   # strip leading '/', split into verb + rest
    verb  = parts[0].lower()
    rest  = parts[1] if len(parts) > 1 else ""

    # /send needs <recipient> and <body> as separate args
    if verb == "send":
        send_parts = rest.split(maxsplit=1)
        args = send_parts if len(send_parts) == 2 else []
    else:
        args = [rest] if rest else []

    return Command(verb=verb, args=args)


def handle_command(cmd: Command, current_user: str) -> bool:
    """
    Dispatch a parsed Command to the appropriate handler.

    Imports are local to avoid circular dependencies between layers.

    Args:
        cmd:          The parsed Command to execute.
        current_user: The logged-in username.

    Returns:
        False if the user asked to quit, True otherwise.
    """
    from messaging import send_message
    from storage   import load_messages, delete_message, mark_as_read
    from display   import display_messages, print_help

    RESET  = "\033[0m"
    GREEN  = "\033[32m"
    RED    = "\033[31m"
    DIM    = "\033[2m"

    if cmd.verb == "send":
        if len(cmd.args) != 2:
            print(f"  {RED}Usage: /send <recipient> <message>{RESET}")
            return True
        recipient, body = cmd.args
        try:
            msg = send_message(sender=current_user, recipient=recipient, body=body)
            print(f"  {GREEN}✓ Sent (ID: {DIM}{msg['id']}{RESET}{GREEN}){RESET}")
        except ValueError as e:
            print(f"  {RED}Error: {e}{RESET}")

    elif cmd.verb == "inbox":
        messages = load_messages(recipient=current_user, unread_only=True)
        print(f"\n  {DIM}Inbox — {len(messages)} unread{RESET}\n")
        display_messages(messages, current_user)

    elif cmd.verb == "all":
        messages = load_messages()
        print(f"\n  {DIM}All messages — {len(messages)} total{RESET}\n")
        display_messages(messages, current_user)

    elif cmd.verb == "read":
        if not cmd.args:
            print(f"  {RED}Usage: /read <message_id>{RESET}")
            return True
        success = mark_as_read(cmd.args[0])
        if success:
            print(f"  {GREEN}✓ Marked as read.{RESET}")
        else:
            print(f"  {RED}Message not found.{RESET}")

    elif cmd.verb == "delete":
        if not cmd.args:
            print(f"  {RED}Usage: /delete <message_id>{RESET}")
            return True
        success = delete_message(cmd.args[0])
        if success:
            print(f"  {GREEN}✓ Deleted.{RESET}")
        else:
            print(f"  {RED}Message not found.{RESET}")

    elif cmd.verb == "help":
        print_help()

    elif cmd.verb == "quit":
        return False

    else:
        print(f"  {RED}Unknown command: /{cmd.verb}. Type /help for options.{RESET}")

    return True