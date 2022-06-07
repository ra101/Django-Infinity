import os

import dotenv
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from .urls import socket_urls


dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


EMOJI_SETTING_MAP = {
    "💀": "essentials",
    "⚙️": "development",
    "🔬": "test",
    "📦": "production",
    "♾️": "infinity",
}

setup_type = EMOJI_SETTING_MAP.get(os.getenv("SETTINGS"), 'essentials')

os.environ.setdefault("DJANGO_CONFIGURATION", "Settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"infinity.settings.{setup_type}")

from configurations.asgi import get_asgi_application

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(socket_urls)),
    }
)
