#!/usr/bin/env python3
import tkinter as tk 
from tkinter import messagebox
import random
import string

# --- Word List ---
WORD_LIST = [
    "apple", "river", "cloud", "stone", "tiger", "flame", "ocean", "eagle",
    "forest", "silver", "thunder", "breeze", "castle", "winter", "pepper",
    "lantern", "crystal", "shadow", "golden", "falcon", "harbor", "jungle",
    "marble", "rocket", "spider", "voyage", "whisper", "dragon", "sunset",
    "mirror", "cactus", "frozen", "planet", "tulip", "candle", "storm",
    "bridge", "copper", "desert", "garden", "island", "lemon", "mountain",
    "narrow", "orbit", "pillar", "quartz", "raindrop", "summit", "temple"
]

# --- Default Colors (Classic Dark) ---
colors = {
    "bg":         [30,  30,  30],
    "fg":         [255, 255, 255],
    "accent":     [180, 180, 180],
    "btn_bg":     [55,  55,  55],
    "entry_bg":   [45,  45,  45],
    "entry_text": [255, 255, 255],
}

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def apply_colors():
    bg         = rgb_to_hex(colors["bg"])
    fg         = rgb_to_hex(colors["fg"])
    accent     = rgb_to_hex(colors["accent"])
    btn_bg     = rgb_to_hex(colors["btn_bg"])
    entry_bg   = rgb_to_hex(colors["entry_bg"])
    entry_text = rgb_to_hex(colors["entry_text"])

    root.configure(bg=bg)

    # Title now follows the fg (text) color
    title_label.configure(bg=bg, fg=fg)

    for w in all_labels:
        w.configure(bg=bg, fg=fg)

    sep_frame.configure(bg=bg)
    for w in all_radiobuttons:
        w.configure(bg=bg, fg=fg, selectcolor=btn_bg, activebackground=bg)

    options_frame.configure(bg=bg)
    for w in all_checkbuttons:
        w.configure(bg=bg, fg=fg, selectcolor=btn_bg, activebackground=bg)

    bottom_frame.configure(bg=bg)
    strength_frame.configure(bg=bg)
    strength_label.configure(bg=bg, fg=fg)

    word_scale.configure(bg=bg, fg=fg, troughcolor=btn_bg, activebackground=accent)
    generate_btn.configure(bg=accent, fg=bg)
    copy_btn.configure(bg=btn_bg, fg=fg)
    settings_btn.configure(bg=btn_bg, fg=fg)
    result_entry.configure(bg=entry_bg, fg=entry_text, insertbackground=entry_text)

    update_strength_display()

# --- Strength Meter ---
def get_strength(passphrase):
    if not passphrase:
        return 0, "None", "#555555"
    length = len(passphrase)
    has_upper  = any(c.isupper() for c in passphrase)
    has_digit  = any(c.isdigit() for c in passphrase)
    has_symbol = any(c in "!@#$%&*?" for c in passphrase)
    word_count = len([w for w in passphrase.replace("-", " ").replace("_", " ").replace(".", " ").split() if w.isalpha()])

    score = 0
    if length >= 10:  score += 1
    if length >= 20:  score += 1
    if length >= 35:  score += 1
    if has_upper:     score += 1
    if has_digit:     score += 1
    if has_symbol:    score += 1
    if word_count >= 4: score += 1
    if word_count >= 6: score += 1

    if score <= 2:
        return score, "Weak", "#e05252"
    elif score <= 4:
        return score, "Fair", "#e0a052"
    elif score <= 6:
        return score, "Good", "#a0c050"
    else:
        return score, "Strong", "#52c070"

def update_strength_display(passphrase=None):
    if passphrase is None:
        passphrase = result_var.get()
    score, label_text, color = get_strength(passphrase)

    max_score = 8
    filled = round((score / max_score) * 10)

    bar = ""
    for i in range(10):
        bar += "█" if i < filled else "░"

    strength_label.configure(
        text=f"Strength:  {bar}  {label_text}",
        fg=color if passphrase else rgb_to_hex(colors["fg"])
    )

# --- Passphrase Logic ---
def generate_passphrase():
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
        update_strength_display(passphrase)
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

def copy_to_clipboard():
    passphrase = result_var.get()
    if passphrase:
        root.clipboard_clear()
        root.clipboard_append(passphrase)
        messagebox.showinfo("Copied!", "Passphrase copied to clipboard.")
    else:
        messagebox.showwarning("Nothing to copy", "Generate a passphrase first!")

# --- Settings Window ---
def open_settings():
    win = tk.Toplevel(root)
    win.title("Settings - Customize Colors")
    win.resizable(False, False)
    win.configure(bg=rgb_to_hex(colors["bg"]))

    tk.Label(win, text="Color Settings", font=("Segoe UI", 14, "bold"),
             bg=rgb_to_hex(colors["bg"]), fg=rgb_to_hex(colors["fg"])
             ).grid(row=0, column=0, columnspan=4, pady=(16, 10), padx=20)

    color_keys = {
        "bg":         "Background",
        "fg":         "Text + Title",
        "accent":     "Accent / Buttons",
        "btn_bg":     "Button Background",
        "entry_bg":   "Result Box Background",
        "entry_text": "Result Box Text",
    }

    preview_labels = {}

    def make_slider_row(row, key, name):
        lbl = tk.Label(win, text=name, font=("Segoe UI", 9, "bold"),
                       bg=rgb_to_hex(colors["bg"]), fg=rgb_to_hex(colors["fg"]),
                       width=20, anchor="w")
        lbl.grid(row=row, column=0, padx=(20, 8), pady=4, sticky="w")

        frame = tk.Frame(win, bg=rgb_to_hex(colors["bg"]))
        frame.grid(row=row, column=1, columnspan=2, pady=4)

        for i, channel in enumerate(["R", "G", "B"]):
            tk.Label(frame, text=channel, font=("Segoe UI", 8),
                     bg=rgb_to_hex(colors["bg"]), fg=rgb_to_hex(colors["fg"]),
                     width=2).grid(row=0, column=i * 2, padx=(6, 0))

            var = tk.IntVar(value=colors[key][i])

            def on_change(val, k=key, idx=i, v=var):
                colors[k][idx] = v.get()
                update_preview(k)
                apply_colors()
                win.configure(bg=rgb_to_hex(colors["bg"]))

            tk.Scale(frame, from_=0, to=255, orient="horizontal",
                     variable=var, length=100, command=on_change,
                     bg=rgb_to_hex(colors["bg"]), fg=rgb_to_hex(colors["fg"]),
                     troughcolor=rgb_to_hex(colors["btn_bg"]),
                     highlightthickness=0, showvalue=False
                     ).grid(row=0, column=i * 2 + 1, padx=2)

        preview = tk.Label(win, width=4, relief="flat", bg=rgb_to_hex(colors[key]))
        preview.grid(row=row, column=3, padx=(8, 20))
        preview_labels[key] = preview

    def update_preview(key):
        preview_labels[key].configure(bg=rgb_to_hex(colors[key]))

    for i, (key, name) in enumerate(color_keys.items()):
        make_slider_row(i + 1, key, name)

    def reset_defaults():
        defaults = {
            "bg":         [30,  30,  30],
            "fg":         [255, 255, 255],
            "accent":     [180, 180, 180],
            "btn_bg":     [55,  55,  55],
            "entry_bg":   [45,  45,  45],
            "entry_text": [255, 255, 255],
        }
        for key, vals in defaults.items():
            colors[key] = vals[:]
        apply_colors()
        win.destroy()
        open_settings()

    tk.Button(win, text="Reset to Default", command=reset_defaults,
              bg=rgb_to_hex(colors["btn_bg"]), fg=rgb_to_hex(colors["fg"]),
              font=("Segoe UI", 9), relief="flat", padx=8, pady=4
              ).grid(row=len(color_keys) + 2, column=0, columnspan=4, pady=(10, 16))

# --- Main Window ---
root = tk.Tk()
root.title("SecurePhrase")
root.resizable(False, False)
root.configure(bg=rgb_to_hex(colors["bg"]))

all_labels       = []
all_radiobuttons = []
all_checkbuttons = []

def lbl(parent, text, **kwargs):
    l = tk.Label(parent, text=text, bg=rgb_to_hex(colors["bg"]),
                 fg=rgb_to_hex(colors["fg"]), font=("Segoe UI", 10), **kwargs)
    all_labels.append(l)
    return l

# Title — follows fg (text) color
title_label = tk.Label(root, text="SecurePhrase", bg=rgb_to_hex(colors["bg"]),
                        fg=rgb_to_hex(colors["fg"]), font=("Segoe UI", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=(18, 10))

# Word count
lbl(root, "Number of words:").grid(row=1, column=0, sticky="w", padx=20, pady=6)
word_count_var = tk.IntVar(value=4)
word_scale = tk.Scale(root, from_=2, to=15, orient="horizontal", variable=word_count_var,
                      bg=rgb_to_hex(colors["bg"]), fg=rgb_to_hex(colors["fg"]),
                      troughcolor=rgb_to_hex(colors["btn_bg"]), highlightthickness=0,
                      activebackground=rgb_to_hex(colors["accent"]), length=160)
word_scale.grid(row=1, column=1, columnspan=2, padx=10, pady=6, sticky="w")

# Separator
lbl(root, "Word separator:").grid(row=2, column=0, sticky="w", padx=20, pady=6)
separator_var = tk.StringVar(value="-")
sep_frame = tk.Frame(root, bg=rgb_to_hex(colors["bg"]))
sep_frame.grid(row=2, column=1, columnspan=2, sticky="w", padx=10)
for val, text in [("-", "Hyphen -"), ("_", "Underscore _"), (".", "Dot ."), (" ", "Space")]:
    rb = tk.Radiobutton(sep_frame, text=text, variable=separator_var, value=val,
                        bg=rgb_to_hex(colors["bg"]), fg=rgb_to_hex(colors["fg"]),
                        selectcolor=rgb_to_hex(colors["btn_bg"]),
                        activebackground=rgb_to_hex(colors["bg"]), font=("Segoe UI", 9))
    rb.pack(side="left", padx=4)
    all_radiobuttons.append(rb)

# Options
lbl(root, "Options:").grid(row=3, column=0, sticky="w", padx=20, pady=6)
options_frame = tk.Frame(root, bg=rgb_to_hex(colors["bg"]))
options_frame.grid(row=3, column=1, columnspan=2, sticky="w", padx=10)

capitalize_var = tk.BooleanVar(value=True)
add_number_var = tk.BooleanVar(value=True)
add_symbol_var = tk.BooleanVar(value=False)

for text, var in [("Capitalize", capitalize_var), ("Add number", add_number_var), ("Add symbol", add_symbol_var)]:
    cb = tk.Checkbutton(options_frame, text=text, variable=var,
                        bg=rgb_to_hex(colors["bg"]), fg=rgb_to_hex(colors["fg"]),
                        selectcolor=rgb_to_hex(colors["btn_bg"]),
                        activebackground=rgb_to_hex(colors["bg"]), font=("Segoe UI", 9))
    cb.pack(side="left", padx=4)
    all_checkbuttons.append(cb)

# Generate button
generate_btn = tk.Button(root, text="Generate Passphrase", command=generate_passphrase,
                          bg=rgb_to_hex(colors["accent"]), fg=rgb_to_hex(colors["bg"]),
                          font=("Segoe UI", 11, "bold"), relief="flat",
                          padx=10, pady=6, cursor="hand2")
generate_btn.grid(row=4, column=0, columnspan=3, pady=(14, 6))

# Result box
result_var = tk.StringVar()
result_entry = tk.Entry(root, textvariable=result_var, font=("Consolas", 13),
                        bg=rgb_to_hex(colors["entry_bg"]),
                        fg=rgb_to_hex(colors["entry_text"]),
                        insertbackground=rgb_to_hex(colors["entry_text"]),
                        relief="flat", width=40, justify="center")
result_entry.grid(row=5, column=0, columnspan=3, padx=20, pady=6, ipady=8)

# Strength meter
strength_frame = tk.Frame(root, bg=rgb_to_hex(colors["bg"]))
strength_frame.grid(row=6, column=0, columnspan=3, pady=(2, 6))
strength_label = tk.Label(strength_frame, text="Strength:  ----------  None",
                           font=("Consolas", 10), bg=rgb_to_hex(colors["bg"]),
                           fg=rgb_to_hex(colors["fg"]))
strength_label.pack()

# Bottom buttons
bottom_frame = tk.Frame(root, bg=rgb_to_hex(colors["bg"]))
bottom_frame.grid(row=7, column=0, columnspan=3, pady=(4, 18))

copy_btn = tk.Button(bottom_frame, text="Copy to Clipboard", command=copy_to_clipboard,
                     bg=rgb_to_hex(colors["btn_bg"]), fg=rgb_to_hex(colors["fg"]),
                     font=("Segoe UI", 10), relief="flat", padx=8, pady=4, cursor="hand2")
copy_btn.pack(side="left", padx=8)

settings_btn = tk.Button(bottom_frame, text="Settings", command=open_settings,
                          bg=rgb_to_hex(colors["btn_bg"]), fg=rgb_to_hex(colors["fg"]),
                          font=("Segoe UI", 10), relief="flat", padx=8, pady=4, cursor="hand2")
settings_btn.pack(side="left", padx=8)

update_strength_display()
root.mainloop()

