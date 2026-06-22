from typing import Any
from .GameRules import Colors
from .strings.EnglishStrings import STRINGS as EN_STRINGS

from .Logger import get_logger

logger = get_logger(__name__)


class TextService:
    def __init__(self, lang: str = "en") -> None:
        self.languages: dict[str, dict[str, str]] = {"en": EN_STRINGS}
        self.active_strings = self.languages.get(lang, EN_STRINGS)

        self._theme_context = {
            "end_color": Colors.END,
            "red_color": Colors.RED,
            "green_color": Colors.GREEN,
            "yellow_color": Colors.YELLOW,
            "blue_color": Colors.BLUE,
            "purple_color": Colors.LIGHT_PURPLE,
            "cyan_color": Colors.CYAN,
            "white_color": Colors.LIGHT_WHITE,
        }

    def format(self, key: str, **kwargs: Any) -> str:
        template = self.active_strings.get(key, f"{key}")

        context = self._theme_context | kwargs

        try:
            return template.format(**context)
        except KeyError as error:
            logger.debug(f"[Format Error in {key}]: Missing Field {error}")
            logger.warning(error)
            return f"[Format Error in {key}]: Missing Field {error}"


text_service = TextService("en")
