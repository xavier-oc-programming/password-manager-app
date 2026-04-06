import sys
from pathlib import Path
from tkinter import *
from tkinter import messagebox
from typing import Callable

from config import (
    WINDOW_TITLE, WINDOW_PADX, WINDOW_PADY,
    LOGO_SIZE,
    WEBSITE_ENTRY_WIDTH, EMAIL_ENTRY_WIDTH, PASSWORD_ENTRY_WIDTH,
)


class Display:
    """Owns the Tk root window and every widget.
    No app logic lives here — all decisions are made in main.py callbacks.
    """

    def __init__(
        self,
        logo_path: Path,
        on_generate: Callable[[], None],
        on_save: Callable[[], None],
        on_search: Callable[[], None],
    ) -> None:
        self._on_generate = on_generate
        self._on_save = on_save
        self._on_search = on_search

        self.root = Tk()
        self.root.title(WINDOW_TITLE)
        self.root.config(padx=WINDOW_PADX, pady=WINDOW_PADY)
        self.root.grid_columnconfigure(1, weight=1)

        self._build_logo(logo_path)
        self._build_labels()
        self._build_entries()
        self._build_buttons()

        self.root.focus_set()

    # ------------------------------------------------------------------ build

    def _build_logo(self, logo_path: Path) -> None:
        self._logo_image = PhotoImage(file=str(logo_path))
        canvas = Canvas(self.root, width=LOGO_SIZE, height=LOGO_SIZE, highlightthickness=0)
        canvas.create_image(LOGO_SIZE // 2, LOGO_SIZE // 2, image=self._logo_image)
        canvas.grid(column=1, row=0, columnspan=2)

    def _build_labels(self) -> None:
        Label(self.root, text="Website:").grid(column=0, row=1, sticky="e")
        Label(self.root, text="Email/Username:").grid(column=0, row=2, sticky="e")
        Label(self.root, text="Password:").grid(column=0, row=3, sticky="e")

    def _build_entries(self) -> None:
        self._website_entry = Entry(self.root, width=WEBSITE_ENTRY_WIDTH)
        self._website_entry.grid(column=1, row=1, columnspan=2, sticky="we")
        self._website_entry.focus()

        self._email_entry = Entry(self.root, width=EMAIL_ENTRY_WIDTH)
        self._email_entry.grid(column=1, row=2, columnspan=2, sticky="we")

        self._password_entry = Entry(self.root, width=PASSWORD_ENTRY_WIDTH)
        self._password_entry.grid(column=1, row=3, sticky="w")

    def _build_buttons(self) -> None:
        Button(self.root, text="Search", width=20, command=self._on_search).grid(
            column=2, row=1, sticky="we"
        )
        Button(self.root, text="Generate Password", width=20, command=self._on_generate).grid(
            column=2, row=3, sticky="we"
        )
        Button(self.root, text="Add", command=self._on_save).grid(
            column=1, row=4, columnspan=2, sticky="we"
        )

    # ------------------------------------------------------------------ getters

    def get_website(self) -> str:
        return self._website_entry.get().strip()

    def get_email(self) -> str:
        return self._email_entry.get().strip()

    def get_password(self) -> str:
        return self._password_entry.get().strip()

    # ------------------------------------------------------------------ setters / render

    def set_password(self, password: str) -> None:
        """Replace the password entry contents."""
        self._password_entry.delete(0, END)
        self._password_entry.insert(0, password)

    def set_email(self, email: str) -> None:
        """Replace the email entry contents."""
        self._email_entry.delete(0, END)
        self._email_entry.insert(0, email)

    def clear_fields(self) -> None:
        """Clear website and password entries after a successful save."""
        self._website_entry.delete(0, END)
        self._password_entry.delete(0, END)

    # ------------------------------------------------------------------ dialogs (thin wrappers)

    def show_info(self, title: str, message: str) -> None:
        messagebox.showinfo(title=title, message=message)

    def show_warning(self, title: str, message: str) -> None:
        messagebox.showwarning(title=title, message=message)

    def show_error(self, title: str, message: str) -> None:
        messagebox.showerror(title=title, message=message)

    def ask_ok_cancel(self, title: str, message: str) -> bool:
        return messagebox.askokcancel(title=title, message=message)

    # ------------------------------------------------------------------ lifecycle

    def close(self) -> None:
        sys.exit(0)
