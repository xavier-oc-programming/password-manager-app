# Password Manager

Tkinter GUI app to generate, save and look up website credentials stored in JSON — Day 29 of 100 Days of Code.

---

## Table of Contents

1. [Quick start](#1-quick-start)
2. [Builds comparison](#2-builds-comparison)
3. [Controls](#3-controls)
4. [App flow](#4-app-flow)
5. [Features](#5-features)
6. [Navigation flow](#6-navigation-flow)
7. [Architecture](#7-architecture)
8. [Module reference](#8-module-reference)
9. [Configuration reference](#9-configuration-reference)
10. [Display layout](#10-display-layout)
11. [Design decisions](#11-design-decisions)
12. [Course context](#12-course-context)
13. [Dependencies](#13-dependencies)

---

## 1. Quick start

```bash
pip install pyperclip
python menu.py          # select 1 (original) or 2 (advanced)

# or run builds directly:
python original/main.py
python advanced/main.py
```

---

## 2. Builds comparison

| Feature | Original | Advanced |
|---|---|---|
| Generate random password | ✅ | ✅ |
| Copy generated password to clipboard | ✅ | ✅ |
| Save credentials to JSON | ✅ | ✅ |
| Confirm before saving (`askokcancel`) | ✅ | ✅ |
| Search credentials by website | ✅ | ✅ |
| Fill entries on search hit | ✅ (main2.py only) | ✅ |
| Path-safe (works from any cwd) | ✅ (path-fixed copy) | ✅ |
| OOP separation (logic / display / config) | ❌ | ✅ |
| Zero magic numbers (`config.py`) | ❌ | ✅ |
| Callbacks injected into Display | ❌ | ✅ |
| `PasswordManager` pure-logic class | ❌ | ✅ |

---

## 3. Controls

### Main window

| Input | Action |
|---|---|
| Type in Website field | Set website for save/search |
| Type in Email/Username field | Set email to save |
| Type in Password field | Set password manually |
| Click **Search** | Look up saved credentials for the entered website |
| Click **Generate Password** | Fill Password field with a random password and copy to clipboard |
| Click **Add** | Confirm and save current fields to `data.json` |

---

## 4. App flow

1. Run `menu.py` — terminal menu appears.
2. Select **1** to launch the original build, **2** for the advanced build.
3. The Tkinter window opens.
4. Enter a **Website** and **Email/Username**.
5. Click **Generate Password** to fill the Password field automatically (copied to clipboard).
6. Click **Add** → confirmation dialog appears → click OK to save.
7. To retrieve credentials: type a website name and click **Search** → fields are filled and password is copied to clipboard.
8. Close the window to return to the terminal menu, which loops back automatically.

---

## 5. Features

### Both builds

**Password generation**
Generates a shuffled password of 8–10 letters, 2–4 symbols, and 2–4 digits. The result is inserted into the Password field and copied to the clipboard immediately.

**Credential saving**
Reads the existing `data.json`, merges the new entry, and writes back. Handles first-run (no file) and corrupt JSON gracefully by starting fresh.

**Credential search**
Looks up the entered website in `data.json`. If found, fills the Email and Password entry fields and copies the password to the clipboard.

**Confirmation dialog**
Before saving, `askokcancel` shows a summary of website, email, and password — the user must confirm before any write occurs.

**Input validation**
All three fields must be non-empty before a save is attempted. A warning dialog is shown otherwise.

### Advanced only

**`PasswordManager` pure-logic class**
All credential logic (generate, load, save, search) lives in `advanced/password_manager.py` with no tkinter dependency. Logic can be unit-tested in isolation.

**`Display` class with injected callbacks**
`Display` owns the Tk root and every widget. It accepts `on_generate`, `on_save`, and `on_search` callables from `main.py`. No business logic lives inside `Display`.

**`config.py` — zero magic numbers**
Every dimension, width, and generation range is a named constant. No magic numbers appear anywhere else in the advanced codebase.

---

## 6. Navigation flow

### a) Terminal menu tree

```
menu.py
├── 1 → subprocess.run(original/main.py)
│         └── [Tkinter window runs, user closes it]
│              └── returns to menu loop
├── 2 → subprocess.run(advanced/main.py)
│         └── [Tkinter window runs, user closes it]
│              └── returns to menu loop
└── q → break → process exits
```

### b) In-app flow

```
┌─────────────────────────────┐
│         Main Window         │
│  (Website / Email / Pass)   │
└──────────────┬──────────────┘
               │
       ┌───────┴────────┐
       │                │
   [Search]          [Generate]
       │                │
  data.json          random pwd
  lookup             → fill field
       │             → clipboard
  found? ─── No ──→ showinfo "Not Found"
       │
      Yes
       │
  fill entries
  copy to clipboard
  showinfo "Credentials Found"
               │
           [Add]
               │
     all fields filled?
      No → showwarning
      Yes → askokcancel
               │
         OK? ──No──→ (no action)
               │
              Yes
               │
         merge → data.json
         clear website + password
         showinfo "Saved"
```

---

## 7. Architecture

```
password-manager-app/
├── menu.py                  # terminal menu — launches builds via subprocess
├── art.py                   # LOGO ascii art printed by menu.py
├── requirements.txt         # stdlib only + pyperclip note
├── .gitignore
├── README.md
│
├── docs/
│   └── COURSE_NOTES.md      # original exercise description and concepts covered
│
├── original/
│   ├── main.py              # course version (path-fixed); entry point for option 1
│   ├── main2.py             # improved iteration: search also fills entries
│   ├── data.json            # persisted credentials (original build)
│   └── logo.png             # lock/key image displayed in the GUI
│
└── advanced/
    ├── main.py              # orchestrator: wires PasswordManager → Display callbacks
    ├── config.py            # all constants — no magic numbers elsewhere
    ├── password_manager.py  # PasswordManager class — pure logic, no tkinter
    ├── display.py           # Display class — owns Tk root + all widgets
    ├── data.json            # persisted credentials (advanced build, separate file)
    └── logo.png             # copy of logo for the advanced build
```

---

## 8. Module reference

### `PasswordManager` (`advanced/password_manager.py`)

| Method | Returns | Description |
|---|---|---|
| `generate_password()` | `str` | Return a new shuffled random password |
| `load_data(data_path)` | `dict` | Load JSON credentials dict; `{}` if absent or corrupt |
| `save_credential(website, email, password, data_path)` | `None` | Merge entry into JSON and write back |
| `search_credential(website, data_path)` | `dict \| None` | Return `{email, password}` or `None` if not found |

### `Display` (`advanced/display.py`)

| Method | Returns | Description |
|---|---|---|
| `__init__(logo_path, on_generate, on_save, on_search)` | — | Build root window and all widgets; store callbacks |
| `get_website()` | `str` | Return stripped Website entry value |
| `get_email()` | `str` | Return stripped Email entry value |
| `get_password()` | `str` | Return stripped Password entry value |
| `set_password(password)` | `None` | Replace Password entry contents |
| `set_email(email)` | `None` | Replace Email entry contents |
| `clear_fields()` | `None` | Clear Website and Password entries |
| `show_info(title, message)` | `None` | Wrap `messagebox.showinfo` |
| `show_warning(title, message)` | `None` | Wrap `messagebox.showwarning` |
| `show_error(title, message)` | `None` | Wrap `messagebox.showerror` |
| `ask_ok_cancel(title, message)` | `bool` | Wrap `messagebox.askokcancel` |
| `close()` | `None` | Call `sys.exit(0)` |

---

## 9. Configuration reference

| Constant | Default | Description |
|---|---|---|
| `WINDOW_TITLE` | `"Password Manager"` | Tk window title bar text |
| `WINDOW_PADX` | `100` | Horizontal padding around the window content |
| `WINDOW_PADY` | `50` | Vertical padding around the window content |
| `LOGO_SIZE` | `200` | Canvas width and height in pixels for the logo |
| `WEBSITE_ENTRY_WIDTH` | `35` | Character width of the Website entry |
| `EMAIL_ENTRY_WIDTH` | `35` | Character width of the Email entry |
| `PASSWORD_ENTRY_WIDTH` | `20` | Character width of the Password entry |
| `LABEL_FONT` | `("Arial", 10)` | Font used for row labels |
| `MIN_LETTERS` | `8` | Minimum letters in a generated password |
| `MAX_LETTERS` | `10` | Maximum letters in a generated password |
| `MIN_SYMBOLS` | `2` | Minimum symbols in a generated password |
| `MAX_SYMBOLS` | `4` | Maximum symbols in a generated password |
| `MIN_NUMBERS` | `2` | Minimum digits in a generated password |
| `MAX_NUMBERS` | `4` | Maximum digits in a generated password |
| `DATA_FILENAME` | `"data.json"` | Filename for credential persistence |

---

## 10. Display layout

```
┌────────────────────────────────────────────────────────────────────┐
│  (padx=100)                                                         │
│                                                                     │
│              ┌──────────────────────┐                              │
│              │   logo.png canvas    │  col 1–2, row 0             │
│              │   200 × 200 px       │                              │
│              └──────────────────────┘                              │
│                                                                     │
│  Website:    [──────── entry ────────────────────] [  Search  ]   │
│              col 1–2, row 1, sticky=we              col 2, row 1  │
│                                                                     │
│  Email/      [──────── entry ────────────────────────────────]    │
│  Username:   col 1–2, row 2, sticky=we                            │
│                                                                     │
│  Password:   [── entry ──]                [Generate Password]     │
│              col 1, row 3, sticky=w        col 2, row 3           │
│                                                                     │
│              [────────────────── Add ──────────────────────]      │
│              col 1–2, row 4, sticky=we                            │
│                                                                     │
│  (pady=50)                                                          │
└────────────────────────────────────────────────────────────────────┘
  col 0        col 1                          col 2
 (labels)   (entries, weight=1)            (buttons)
```

---

## 11. Design decisions

**`display.py` owns all UI**
Keeping every widget in one class makes it trivial to swap the UI layer (e.g., replace tkinter with a web frontend) without touching logic. It also means `PasswordManager` can be unit-tested without a display at all.

**`config.py` — zero magic numbers**
A single source of truth for every dimension and range. Changing `LOGO_SIZE` or `MIN_LETTERS` propagates everywhere with no hunting through code.

**Callbacks injected via `__init__`**
`Display` accepts `on_generate`, `on_save`, `on_search` at construction time. This means Display has zero knowledge of `PasswordManager` or `data.json` — it only calls back to main.py when the user acts.

**`sys.path.insert` pattern in `advanced/main.py`**
`sys.path.insert(0, str(Path(__file__).parent))` ensures that `import config`, `import display`, and `import password_manager` work whether the file is launched from `menu.py` via `subprocess.run(cwd=...)` or directly from the terminal.

**`subprocess.run` + `cwd=` in `menu.py`**
Using `cwd=path.parent` ensures each build resolves its relative assets (logo, data.json) from its own directory, regardless of where `menu.py` is invoked from.

**`while True` in `menu.py` vs recursion**
A loop re-renders the menu cleanly after a subprocess returns. Recursion would grow the call stack on every menu visit without bound.

**Console cleared before every menu render**
`os.system("cls"/"clear")` runs at the top of every loop iteration so the menu is always presented cleanly without accumulating output from prior sessions.

**`sys.exit(0)` vs `root.destroy()` in `close()`**
`root.destroy()` alone can leave tkinter's internal event loop in an inconsistent state on some platforms, causing errors after the window closes. `sys.exit(0)` terminates the process cleanly.

**`data.json` load → update → write-back strategy**
Rather than appending or overwriting, each save reads the full file first, merges the new entry, then writes the merged dict back. This preserves all previously saved credentials and also handles the update-existing-entry case transparently.

**Separate `data.json` per build**
`original/data.json` and `advanced/data.json` are independent files. The two builds never share state, which means switching builds doesn't produce confusing cross-contamination.

---

## 12. Course context

Built as Day 29 of 100 Days of Code by Dr. Angela Yu.

**Concepts covered in the original build:**
- Tkinter grid layout (`columnspan`, `sticky`, `weight`)
- `PhotoImage` and `Canvas` for embedding images
- `Entry` widget read/write (`get`, `delete`, `insert`)
- `messagebox` dialogs (info, warning, error, askokcancel)
- `random.choice` and `random.shuffle` for password generation
- `pyperclip` for cross-platform clipboard access
- `json.load` / `json.dump` for persistent storage
- Graceful error handling for missing or corrupt JSON files

**The advanced build extends into:**
- OOP — `PasswordManager` pure-logic class
- MVC-style separation — display / logic / orchestration
- Callback injection for decoupling Display from business logic
- Named constants in `config.py` (no magic numbers)
- `pathlib.Path` for robust cross-platform file handling
- `sys.path.insert` for sibling-module imports when launched via subprocess

See [docs/COURSE_NOTES.md](docs/COURSE_NOTES.md) for full concept breakdown.

---

## 13. Dependencies

| Module | Used in | Purpose |
|---|---|---|
| `tkinter` | `original/main.py`, `original/main2.py`, `advanced/display.py` | GUI framework (ships with Python; Linux: `python3-tk`) |
| `random` | `original/main.py`, `original/main2.py`, `advanced/password_manager.py` | Password character selection and shuffling |
| `json` | `original/main.py`, `original/main2.py`, `advanced/password_manager.py` | Credential persistence |
| `pathlib` | `original/main.py`, `original/main2.py`, `advanced/main.py`, `advanced/display.py` | Cross-platform file paths |
| `os` | `menu.py` | Console clearing (`cls` / `clear`) |
| `sys` | `menu.py`, `advanced/main.py`, `advanced/display.py` | `sys.exit`, `sys.path`, `sys.executable` |
| `subprocess` | `menu.py` | Launching builds as child processes |
| `typing` | `advanced/display.py` | `Callable` type hints |
| `pyperclip` *(third-party)* | `original/main.py`, `original/main2.py`, `advanced/main.py` | Clipboard copy on all platforms |
