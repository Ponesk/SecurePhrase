#!/usr/bin/env python3
import tkinter as tk 
from tkinter import messagebox
import random
import string

# --- A list of easy-to-remember words --- 
WORD_LIST = [
        "apple", "river", "cloud", "stone", "tiger", "flame", "ocean", "eagle",
    "forest", "silver", "thunder", "breeze", "castle", "winter", "pepper",
    "lantern", "crystal", "shadow", "golden", "falcon", "harbor", "jungle",
    "marble", "rocket", "spider", "voyage", "whisper", "dragon", "sunset",
    "mirror", "cactus", "frozen", "planet", "tulip", "candle", "storm",
    "bridge", "copper", "desert", "garden", "island", "lemon", "mountain",
    "narrow", "orbit", "pillar", "quartz", "raindrop", "summit", "temple"
]

# --- Colors ---
BG       = "#1a0a00"
FG       = "#ffe5cc"
ACCENT   = "#ff6b2b"
BTN_BG   = "#3d1a00"
ENTRY_BG = "#2e1200"
ENTRY_FG = "#ffffff"   # bright white so text is always visible

def generate_passphrase():
    """Builds a passphrase from random words + optional extras."""
    try:
        num_words = word_count_var.get()
        words = [random.choice(WORD_LIST) for _ in range(num_words)]

        if capitalize_var.get():
            words = [w.capitalize() for w in words]

        separator = separator_var.get()
        passphrase = separator.join(words)

        if add_number_var.get():
            passphrase += str(random.randint(10, 99))

        if add_symbol_var.get():
            passphrase += random.choice("!@#$%&*?")

        result_var.set(passphrase)

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

def copy_to_clipboard():
    """Copies the passphrase to the clipboard."""
    passphrase = result_var.get()
    if passphrase:
        root.clipboard_clear()
        root.clipboard_append(passphrase)
        messagebox.showinfo("Copied!", "Passphrase copied to clipboard.")
    else:
        messagebox.showwarning("Nothing to copy", "Generate a passphrase first!")

# --- Main Window ---
root = tk.Tk()
root.title("Passphrase Generator")
root.resizable(False, False)
root.configure(bg=BG)

def label(parent, text, **kwargs):
    return tk.Label(parent, text=text, bg=BG, fg=FG, font=("Segoe UI", 10), **kwargs)

# Title
tk.Label(root, text="Passphrase Generator", bg=BG, fg=ACCENT,
         font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=(18, 10))

# Number of words slider
label(root, "Number of words:").grid(row=1, column=0, sticky="w", padx=20, pady=6)
word_count_var = tk.IntVar(value=4)
tk.Scale(root, from_=2, to=15, orient="horizontal", variable=word_count_var,
         bg=BG, fg=FG, troughcolor=BTN_BG, highlightthickness=0,
         activebackground=ACCENT, length=160
         ).grid(row=1, column=1, columnspan=2, padx=10, pady=6, sticky="w")

# Separator
label(root, "Word separator:").grid(row=2, column=0, sticky="w", padx=20, pady=6)
separator_var = tk.StringVar(value="-")
sep_frame = tk.Frame(root, bg=BG)
sep_frame.grid(row=2, column=1, columnspan=2, sticky="w", padx=10)
for val, text in [("-", "Hyphen -"), ("_", "Underscore _"), (".", "Dot ."), (" ", "Space")]:
    tk.Radiobutton(sep_frame, text=text, variable=separator_var, value=val,
                   bg=BG, fg=FG, selectcolor=BTN_BG,
                   activebackground=BG, font=("Segoe UI", 9)).pack(side="left", padx=4)

# Options
label(root, "Options:").grid(row=3, column=0, sticky="w", padx=20, pady=6)
options_frame = tk.Frame(root, bg=BG)
options_frame.grid(row=3, column=1, columnspan=2, sticky="w", padx=10)

capitalize_var = tk.BooleanVar(value=True)
add_number_var = tk.BooleanVar(value=True)
add_symbol_var = tk.BooleanVar(value=False)

for text, var in [("Capitalize", capitalize_var), ("Add number", add_number_var), ("Add symbol", add_symbol_var)]:
    tk.Checkbutton(options_frame, text=text, variable=var,
                   bg=BG, fg=FG, selectcolor=BTN_BG,
                   activebackground=BG, font=("Segoe UI", 9)).pack(side="left", padx=4)

# Generate button
tk.Button(root, text="Generate Passphrase", command=generate_passphrase,
          bg=ACCENT, fg="#1a0a00", font=("Segoe UI", 11, "bold"),
          relief="flat", padx=10, pady=6, cursor="hand2"
          ).grid(row=4, column=0, columnspan=3, pady=(14, 6))

# Result box
result_var = tk.StringVar()
tk.Entry(root, textvariable=result_var, font=("Consolas", 13),
         bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG,
         relief="flat", width=40, justify="center"
         ).grid(row=5, column=0, columnspan=3, padx=20, pady=6, ipady=8)

# Copy button
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard,
          bg=BTN_BG, fg=FG, font=("Segoe UI", 10),
          relief="flat", padx=8, pady=4, cursor="hand2"
          ).grid(row=6, column=0, columnspan=3, pady=(4, 18))

root.mainloop()

