from infinity.libs.constant import ConstantClass


class ProjectDetails(ConstantClass):
    """Project Details used for initalizing swagger"""

    TITLE = "Django Infinity"
    DESCRIPTION = "A Big Project of Django with All its Infinite Extensions"

    AUTHOR_NAME = "〈 RA 〉"
    AUTHOR_EMAIL = "dev.ra.101@protonmail.com"
    AUTHOR_WEB = "https://ra101.github.io"

    LICENSE_TYPE = "MIT License"
    LICENSE_URL = "https://raw.githubusercontent.com/ra101/Django-Infinity/core/LICENSE"

    IS_PUBLIC = True


class LiveDemoInitialConfig(ConstantClass):
    """Config values used in constance for Live Demo"""

    KEY = "some_random_key"
    KEY_HELP = "Editable Key for live-setting endpoint"

    VALUE = "some_random_value"
    VALUE_HELP = "Editable Value for live-setting endpoint"

    ENDPOINT = "some_random_url_endpoint"
    ENDPOINT_HELP = (
        "Editable URL Endpoint,"
        "\nTo get the response send a GET Request at "
        "\n/live_settings/<LIVE_URL_ENDPOINT>"
    )
