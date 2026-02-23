# SecurePhrase
### *by Ponesk*

---

> ### Generate strong, memorable passphrases — right from your desktop.

A simple, beginner-friendly passphrase generator built with Python and Tkinter. Fully offline, customizable, and easy to use.

![SecurePhrase Screenshot](screenshot.png)
> *Screenshot coming soon — add yours here after your first run!*

---

## Features

- **Adjustable word count** — choose between 2 and 15 words using a slider
- **Multiple separators** — separate words with a hyphen, underscore, dot, or space
- **Capitalization** — optionally capitalize each word for added readability
- **Number & symbol support** — append a random number and/or symbol to boost strength
- **Passphrase strength meter** — live color-coded bar that rates your passphrase as Weak, Fair, Good, or Strong based on length, complexity, and word count
- **Color customization** — open Settings to tune every part of the UI using RGB sliders with a live preview; changes apply instantly
- **Reset to default** — one click restores the Classic Dark theme from Settings
- **One-click copy** — copy your passphrase to the clipboard instantly
- **No internet required** — runs fully offline on your machine

---

## Requirements

- Python 3.x
- Tkinter (usually bundled with Python, see install notes below)

---

## How to Install & Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/SecurePhrase.git
cd SecurePhrase
```

### 2. Install dependencies

Tkinter is built into Python on most systems. If it's missing, install it for your distro:

**Arch Linux / Manjaro:**
```bash
sudo pacman -S python tk
```

**Ubuntu / Debian:**
```bash
sudo apt install python3-tk
```

**Fedora / RHEL:**
```bash
sudo dnf install python3-tkinter
```

### 3. Run the app

```bash
python3 passphrase_generator.py
```

### Optional: Make it directly executable (Linux/macOS)

```bash
chmod +x passphrase_generator.py
./passphrase_generator.py
```

---

## How to Contribute

Contributions are welcome! Here's how to get started:

1. **Fork** this repository by clicking the Fork button at the top of the page
2. **Clone** your fork to your local machine:
   ```bash
   git clone https://github.com/YOUR-USERNAME/SecurePhrase.git
   ```
3. **Create a new branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and commit them:
   ```bash
   git commit -m "Add: description of your change"
   ```
5. **Push** to your fork and open a **Pull Request**

### Ideas for contributions
- Add more words to the word list
- Add support for loading a custom word list from a file
- Add preset color themes to the Settings menu
- Package the app as a standalone executable

---

*Built with Python and Tkinter*
