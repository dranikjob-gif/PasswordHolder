# Password Holder

A lightweight, secure, and modern desktop password manager for Windows built with **Python** and **PyQt6**. Designed for instant access from anywhere in the system via global hotkeys and seamless system tray integration.

## Features

- **Strong Local Encryption:** All passwords are encrypted using `cryptography` (Fernet / AES-128) with a key derived via `PBKDF2HMAC-SHA256` from yout Master Password.
- **Instant Global Hotkey:** Press 'Ctrl + Aly + P' at any time to smoothly slide in and out of view, even when minimized to the tray.
- **Frameless Modern UI:** Dark-themed, distraction-free interface with smooth animations and custom dialogs.
- **System Tray & Autostart:** Minimizes cleanly to the Windows system tray and automatically registers itself in Windows startup upon first launch (in `.exe` mode).
- **Master Password Management:** Change your Master Password anytime - the app automatically decrypts and re-encrypts your entire SQLite vault with the new key.

## Tech Stack

- **GUI:** PyQt6
- **Database:** SQLite3
- **Security:** `cryptography` (Fernet), `hashlib` (PBKDF2)
- **System Integration:** 'keyboard', Windows Registry ('QSettings')
- **Packaging:** PyInstaller

## Getting Started 

### Option 1: Run the Standalone `.exe` (Windows)
1. Download the latest `PasswordHolder.exe` from the [Releases](../../releases) page.
2. Run the executable—it will automatically create an encrypted local database (`acc_db.db`) in the same directory and add itself to Windows startup.
3. Create your Master Password on first launch.

### Option 2: Run from Source
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/PasswordHolder.git](https://github.com/your-username/PasswordHolder.git)
   cd PasswordHolder
