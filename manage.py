#!/venv/Scripts/python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess

import dotenv


EMOJI_SETTING_MAP = {
    "⚙️": "development",
    "🔬": "test",
    "📦": "staging",
    "🎁": "production",
    "♾️": "infinity",
}


def main():
    dotenv.load_dotenv(encoding="utf-8")
    arguments = sys.argv

    ###### Dumb Stuff - Start

    settings_emoji = os.getenv("SETTINGS")

    if settings_emoji not in EMOJI_SETTING_MAP:
        raise ValueError(f"`{settings_emoji}` SETTINGS not in {EMOJI_SETTING_MAP}")

    setup_type = EMOJI_SETTING_MAP[settings_emoji]

    if "installrequirements" in arguments:
        subprocess.call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r" f"requirements/{setup_type}.txt",
            ]
        )
        return

    ####### Dumb Stuff - Stop

    os.environ.update(
        {
            "DJANGO_CONFIGURATION": "Settings",
            "DJANGO_SETTINGS_MODULE": f"infinity.settings.{setup_type}",
        }
    )

    try:
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(arguments)


if __name__ == "__main__":
    main()
