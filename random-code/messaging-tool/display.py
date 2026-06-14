"""
display.py — Format and render messages to the terminal.
"""

from datetime import datetime, timezone, timedelta


# ANSI colour codes (gracefully degrade in terminals that don't support them)
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"


def format_timestamp(iso_str: str) -> str:
    """
    Convert a UTC ISO timestamp to a human-friendly local time string.

    Today's messages show as "HH:MM"; older messages include the date.
    """
    dt_utc = datetime.fromisoformat(iso_str).replace(tzinfo=timezone.utc)
    dt_local = dt_utc.astimezone()
    now_local = datetime.now(dt_local.tzinfo)

    if dt_local.date() == now_local.date():
        return dt_local.strftime("%H:%M")
    elif dt_local.date() == (now_local - timedelta(days=1)).date():
        return "yesterday " + dt_local.strftime("%H:%M")
    else:
        return dt_local.strftime("%d %b %H:%M")


def format_message(msg: dict, current_user: str) -> str:
    """
    Render a single message as a coloured terminal string.

    Sent messages appear right-attributed; received messages left-attributed.
    Unread received messages are highlighted in bold.
    """
    timestamp = format_timestamp(msg["timestamp"])
    is_mine   = msg["sender"] == current_user
    is_unread = not msg["read"] and not is_mine

    if is_mine:
        header = f"{DIM}{timestamp}{RESET}  {CYAN}{BOLD}you → {msg['recipient']}{RESET}"
    else:
        name_color = BOLD if is_unread else ""
        header = f"{DIM}{timestamp}{RESET}  {GREEN}{name_color}{msg['sender']}{RESET}"

    body = f"{BOLD}{msg['body']}{RESET}" if is_unread else msg["body"]
    return f"  {header}\n  {body}"


def display_messages(messages: list[dict], current_user: str, page_size: int = 20) -> None:
    """
    Print messages to stdout, paginated by page_size.

    Prompts the user to press Enter between pages.
    """
    if not messages:
        print(f"  {DIM}No messages.{RESET}")
        return

    for i, msg in enumerate(messages, start=1):
        print(format_message(msg, current_user))
        print()  # blank line between messages

        if i % page_size == 0 and i < len(messages):
            try:
                input(f"  {DIM}-- {i}/{len(messages)} messages shown. Press Enter for more --{RESET}")
            except KeyboardInterrupt:
                print()
                return


def print_help() -> None:
    """Print all available commands to stdout."""
    commands = [
        ("/send <recipient> <message>", "Send a message"),
        ("/inbox",                      "Show your unread messages"),
        ("/all",                        "Show all messages"),
        ("/delete <message_id>",        "Delete a message by ID"),
        ("/read <message_id>",          "Mark a message as read"),
        ("/help",                       "Show this help text"),
        ("/quit",                       "Exit the app"),
    ]
    print(f"\n  {BOLD}Available commands:{RESET}")
    for cmd, desc in commands:
        print(f"  {CYAN}{cmd:<35}{RESET} {DIM}{desc}{RESET}")
    print()