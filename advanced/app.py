import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pyperclip

from config import DATA_FILENAME
from password_manager import PasswordManager
from display import Display

_HERE = Path(__file__).parent
DATA_PATH = _HERE / DATA_FILENAME
LOGO_PATH = _HERE / "logo.png"


def main() -> None:
    pm = PasswordManager()

    def on_generate() -> None:
        password = pm.generate_password()
        display.set_password(password)
        pyperclip.copy(password)
        display.show_info("Password Generated", "Password copied to clipboard!")

    def on_save() -> None:
        website = display.get_website()
        email = display.get_email()
        password = display.get_password()

        if not website or not email or not password:
            display.show_warning("Missing Information", "Please fill in all fields.")
            return

        confirmed = display.ask_ok_cancel(
            title=website,
            message=(
                f"Website: {website}\n"
                f"Email: {email}\n"
                f"Password: {password}\n\n"
                "Save to file?"
            ),
        )
        if not confirmed:
            return

        pm.save_credential(website, email, password, DATA_PATH)
        display.clear_fields()
        display.show_info("Saved", f"Saved credentials for {website}.")

    def on_search() -> None:
        website = display.get_website()
        if not website:
            display.show_warning("Missing Information", "Please enter a website to search.")
            return

        creds = pm.search_credential(website, DATA_PATH)
        if creds is None:
            if not DATA_PATH.exists():
                display.show_error("Error", "No data file found.")
            else:
                display.show_info("Not Found", f"No details for '{website}' were found.")
            return

        display.set_email(creds.get("email", ""))
        display.set_password(creds.get("password", ""))
        pyperclip.copy(creds.get("password", ""))
        display.show_info(
            "Credentials Found",
            f"Email: {creds.get('email', '')}\n"
            f"Password: {creds.get('password', '')}\n"
            "Password copied to clipboard.",
        )

    display = Display(
        logo_path=LOGO_PATH,
        on_generate=on_generate,
        on_save=on_save,
        on_search=on_search,
    )
    display.root.mainloop()


if __name__ == "__main__":
    main()
