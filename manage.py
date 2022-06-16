#!/venv/Scripts/python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess

import dotenv


EMOJI_SETTING_MAP = {
    "💀": "essentials",
    "⚙️": "development",
    "🔬": "test",
    "📦": "production",
    "♾️": "infinity",
}


def main():
    dotenv.load_dotenv(encoding="utf-8")
    arguments = sys.argv
    setup_type = EMOJI_SETTING_MAP.get(os.getenv("SETTINGS"), 'essentials')

    # !Dumb Stuff - Start

    if "installrequirements" in arguments:
        subprocess.call([
            sys.executable, "-m", "pip", "install",
            "-r", f"requirements/{setup_type}.txt",
        ])
        return

    # !Dumb Stuff - Stop

    os.environ.setdefault('DJANGO_CONFIGURATION', 'Settings')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"infinity.settings.{setup_type}")

    try:
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
