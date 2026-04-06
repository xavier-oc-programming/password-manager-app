import json
import random
from pathlib import Path

from config import (
    MIN_LETTERS, MAX_LETTERS,
    MIN_SYMBOLS, MAX_SYMBOLS,
    MIN_NUMBERS, MAX_NUMBERS,
)

_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_NUMBERS = "0123456789"
_SYMBOLS = "!#$%&()*+"


class PasswordManager:
    """Pure logic: password generation and JSON credential storage.
    No tkinter imports, no print(), no UI concerns.
    """

    def generate_password(self) -> str:
        """Return a new random password (not copied to clipboard)."""
        parts = (
            [random.choice(_LETTERS) for _ in range(random.randint(MIN_LETTERS, MAX_LETTERS))]
            + [random.choice(_SYMBOLS) for _ in range(random.randint(MIN_SYMBOLS, MAX_SYMBOLS))]
            + [random.choice(_NUMBERS) for _ in range(random.randint(MIN_NUMBERS, MAX_NUMBERS))]
        )
        random.shuffle(parts)
        return "".join(parts)

    def load_data(self, data_path: Path) -> dict:
        """Return the credentials dict from data_path, or {} if absent/corrupt."""
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_credential(self, website: str, email: str, password: str, data_path: Path) -> None:
        """Merge {website: {email, password}} into data_path (creates file if absent)."""
        data = self.load_data(data_path)
        data[website] = {"email": email, "password": password}
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)

    def search_credential(self, website: str, data_path: Path) -> dict | None:
        """Return {email, password} for website, or None if not found."""
        data = self.load_data(data_path)
        return data.get(website)
