#!/usr/bin/env python3
"""
Gamify Your Life — Installer
Supports Windows and Linux.
Run this once after downloading from GitHub.
"""

import sys
import os
import subprocess
import shutil
import platform

REQUIRED_PACKAGES = ["matplotlib", "numpy", "simple-term-menu"]
APP_NAME = "GamifyLife"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEM = platform.system()  # "Windows" or "Linux"


# ─────────────────────────────────────────────
# STEP 1 — Install dependencies
# ─────────────────────────────────────────────

def is_package_installed(package):
    try:
        __import__(package.replace("-", "_"))
        return True
    except ImportError:
        return False

def install_dependencies():
    print("\n[1/4] Checking dependencies...")
    missing = []

    check_names = {
        "matplotlib": "matplotlib",
        "numpy": "numpy",
        "questionary": "questionary"
    }

    for package, import_name in check_names.items():
        try:
            __import__(import_name)
            print(f"  ✅ {package} already installed")
        except ImportError:
            print(f"  ⬇  {package} missing — will install")
            missing.append(package)

    if missing:
        print("\n  Installing missing packages...")
        cmd = [sys.executable, "-m", "pip", "install"] + missing
        if SYSTEM == "Linux":
            cmd.append("--break-system-packages")
        subprocess.check_call(cmd)
        print("  ✅ All dependencies installed.")
    else:
        print("  ✅ All dependencies already present.")


# ─────────────────────────────────────────────
# STEP 2 — Set up data.json
# ─────────────────────────────────────────────

def setup_data():
    print("\n[2/4] Setting up data file...")
    data_path = os.path.join(SCRIPT_DIR, "data.json")
    template_path = os.path.join(SCRIPT_DIR, "data_template.json")

    if os.path.exists(data_path):
        print("  ✅ data.json already exists — skipping.")
    elif os.path.exists(template_path):
        shutil.copy(template_path, data_path)
        print("  ✅ data.json created from template.")
    else:
        print("  ⚠  data_template.json not found — data.json will be created on first run.")


# ─────────────────────────────────────────────
# STEP 3 — Build exe (Windows only)
# ─────────────────────────────────────────────

def build_exe():
    if SYSTEM != "Windows":
        return None

    print("\n[3/4] Building .exe (this may take a minute)...")
    exe_path = os.path.join(SCRIPT_DIR, "dist", f"{APP_NAME}.exe")

    if os.path.exists(exe_path):
        print("  ✅ .exe already exists — skipping build.")
        return exe_path

    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--console",
            f"--name={APP_NAME}",
            os.path.join(SCRIPT_DIR, "main.py")
        ])
        print("  ✅ .exe built successfully.")
        return exe_path
    except Exception as e:
        print(f"  ⚠  PyInstaller failed: {e}")
        print("  Shortcut will point to main.py instead.")
        return None


# ─────────────────────────────────────────────
# STEP 4 — Create desktop shortcut
# ─────────────────────────────────────────────

def get_desktop_path():
    if SYSTEM == "Windows":
        return os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    else:
        return os.path.join(os.path.expanduser("~"), "Desktop")

def create_shortcut_windows(exe_path):
    print("\n[4/4] Creating desktop shortcut...")
    desktop = get_desktop_path()
    main_py = os.path.join(SCRIPT_DIR, "main.py")

    # Always delete old shortcut/bat so we recreate fresh
    for old in [os.path.join(desktop, f"{APP_NAME}.lnk"),
                os.path.join(desktop, f"{APP_NAME}.bat")]:
        if os.path.exists(old):
            os.remove(old)

    try:
        import winshell
        from win32com.client import Dispatch

        shortcut_path = os.path.join(desktop, f"{APP_NAME}.lnk")
        python_exe = sys.executable  # explicit path to python.exe
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = python_exe
        shortcut.Arguments = f'"{main_py}"'
        shortcut.WorkingDirectory = SCRIPT_DIR
        shortcut.IconLocation = python_exe
        shortcut.save()
        print(f"  ✅ Shortcut created at: {shortcut_path}")

    except ImportError:
        # Fallback: .bat launcher — explicitly calls python, not the .py file
        bat_path = os.path.join(desktop, f"{APP_NAME}.bat")
        with open(bat_path, "w") as f:
            f.write(
                f'@echo off\n'
                f'cd /d "{SCRIPT_DIR}"\n'
                f'python "{main_py}"\n'
                f'pause\n'
            )
        print(f"  ✅ Launcher created at: {bat_path}")
        print("  (Install pywin32 for a proper .lnk shortcut: pip install pywin32)")


def create_shortcut_linux():
    print("\n[4/4] Creating desktop shortcut...")
    desktop = get_desktop_path()
    shortcut_path = os.path.join(desktop, f"{APP_NAME}.desktop")
    main_py = os.path.join(SCRIPT_DIR, "main.py")

    # Always recreate so changes apply
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)

    os.chmod(main_py, 0o755)

    # Find python3 explicitly so it doesn't depend on PATH
    python3 = shutil.which("python3") or "python3"

    desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Gamify Life
Comment=Gamify your daily life
Exec=bash -c "cd '{SCRIPT_DIR}' && '{python3}' '{main_py}'; read -p 'Press Enter to close...'"
Icon=utilities-terminal
Terminal=true
Categories=Utility;
"""

    os.makedirs(desktop, exist_ok=True)
    with open(shortcut_path, "w") as f:
        f.write(desktop_entry)

    os.chmod(shortcut_path, 0o755)
    print(f"  ✅ Shortcut created at: {shortcut_path}")
    print("  (Right-click it → Allow Launching if needed)")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    print("=" * 45)
    print("  GAMIFY YOUR LIFE — INSTALLER")
    print("=" * 45)

    if SYSTEM not in ("Windows", "Linux"):
        print(f"  Unsupported OS: {SYSTEM}")
        sys.exit(1)

    install_dependencies()
    setup_data()

    if SYSTEM == "Windows":
        exe_path = build_exe()
        create_shortcut_windows(exe_path)
    else:
        print("\n[3/4] Skipping .exe build (Linux)")
        create_shortcut_linux()

    print("\n" + "=" * 45)
    print("  ✅ Installation complete!")
    if SYSTEM == "Windows":
        print(f"  Launch the app from your desktop: {APP_NAME}")
    else:
        print("  Launch the app from your desktop shortcut.")
        print("  Or run anywhere: ./main.py")
    print("=" * 45 + "\n")

if __name__ == "__main__":
    main()
