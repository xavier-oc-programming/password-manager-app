import os
import sys
import subprocess
from pathlib import Path

from art import LOGO

ROOT = Path(__file__).parent

while True:
    os.system("cls" if os.name == "nt" else "clear")
    print(LOGO)
    print("Password Manager")
    print("────────────────────────────────────────")
    print("  1 → Original build  (course version)")
    print("  2 → Advanced build  (OOP / MVC)")
    print("  q → Quit")
    print("────────────────────────────────────────")

    choice = input("Select: ").strip().lower()

    if choice == "1":
        path = ROOT / "original" / "main.py"
        subprocess.run([sys.executable, str(path)], cwd=str(path.parent))
    elif choice == "2":
        path = ROOT / "advanced" / "main.py"
        subprocess.run([sys.executable, str(path)], cwd=str(path.parent))
    elif choice == "q":
        break
    else:
        print("Invalid choice. Try again.")
