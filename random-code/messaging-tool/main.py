"""
main.py — Entry point. Initialises the app and runs the event loop.

Project layout:
    main.py       ← you are here
    storage.py    ← SQLite persistence (save, load, delete, mark_as_read)
    messaging.py  ← business logic (create_message, send_message)
    validate.py   ← input validation
    display.py    ← terminal rendering (format_message, display_messages, print_help)
    cli.py        ← input parsing and command dispatch (get_user_input, parse_command, handle_command)
"""

import sys

from storage import init_db
from display import print_help
from cli     import get_user_input, parse_command, handle_command


BOLD  = "\033[1m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def get_current_user() -> str:
    """
    Resolve the active username.

    Checks CLI args first (python main.py alice), then prompts interactively.
    """
    if len(sys.argv) > 1:
        return sys.argv[1]

    print(f"\n  {BOLD}CLI Messenger{RESET}")
    while True:
        username = input("  Enter your username: ").strip()
        if username:
            return username
        print("  Username cannot be empty.")


def run_event_loop(current_user: str) -> None:
    """
    Main read-dispatch loop.

    Reads a line of input, parses it into a Command, and hands it to
    handle_command(). Exits cleanly when handle_command returns False
    (i.e. the user typed /quit) or when stdin closes.
    """
    prompt = f"  {CYAN}{current_user}{RESET} > "

    while True:
        raw = get_user_input(prompt)

        if raw is None:          # Ctrl-C or Ctrl-D
            break

        if not raw:              # blank line — re-prompt silently
            continue

        cmd = parse_command(raw)
        if cmd is None:
            print(f"  {DIM}Commands start with /. Type /help to see options.{RESET}")
            continue

        keep_running = handle_command(cmd, current_user)
        if not keep_running:
            break


def shutdown(current_user: str) -> None:
    """Flush any pending output and print a goodbye message."""
    print(f"\n  {DIM}Goodbye, {current_user}.{RESET}\n")
    sys.stdout.flush()


def main() -> None:
    """
    Application lifecycle:
        1. init_db()         — ensure schema exists
        2. get_current_user()— resolve username from args or prompt
        3. print_help()      — show commands on startup
        4. run_event_loop()  — block until /quit or EOF
        5. shutdown()        — clean exit message
    """
    init_db()
    current_user = get_current_user()

    print(f"\n  Welcome, {BOLD}{current_user}{RESET}. Type /help for commands.\n")
    print_help()

    run_event_loop(current_user)
    shutdown(current_user)


if __name__ == "__main__":
    main()