# Course Notes — Day 29: Password Manager

## Exercise description

Build a GUI password manager in Python using Tkinter.

The app should:
- Display a lock / key logo at the top of the window
- Have three labelled fields: **Website**, **Email/Username**, **Password**
- Have a **Generate Password** button that creates a random strong password and copies it to the clipboard
- Have a **Search** button next to the Website field that looks up saved credentials
- Have an **Add** button that saves the current fields to a local file
- Persist credentials in `data.json` (JSON format, pretty-printed)
- Validate that no field is empty before saving
- Ask for confirmation via `messagebox.askokcancel` before writing

## Concepts covered

- **Tkinter grid layout** — `columnspan`, `sticky="we"`, `weight=1` for resizing
- **`PhotoImage` + `Canvas`** — embedding a PNG logo in the window
- **`Entry` widget** — reading and writing text fields programmatically
- **`messagebox`** — `showinfo`, `showwarning`, `showerror`, `askokcancel`
- **`random.choice` + `random.shuffle`** — generating shuffled password character lists
- **`pyperclip.copy`** — cross-platform clipboard access
- **JSON read/write** — `json.load`, `json.dump` with `indent` and `sort_keys`
- **Error handling** — `FileNotFoundError`, `json.JSONDecodeError` for first-run and corrupt data
- **`data.json` merge strategy** — load → update → write-back to preserve existing entries

## Differences between `main.py` and `main2.py`

`main2.py` (the later iteration) improves `search_password()`:
- Also fills the **Email** and **Password** entry fields with the found credentials
- Slightly different "not found" error message that includes the filename

Everything else is identical.
