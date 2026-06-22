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
            # Text Reset / End
            "end": Colors.END,
            # Standard Colors
            "black": Colors.BLACK,
            "red": Colors.RED,
            "green": Colors.GREEN,
            "brown": Colors.BROWN,
            "blue": Colors.BLUE,
            "purple": Colors.PURPLE,
            "cyan": Colors.CYAN,
            "light_gray": Colors.LIGHT_GRAY,
            # Bright / Modified Colors
            "dark_gray": Colors.DARK_GRAY,
            "light_red": Colors.LIGHT_RED,
            "light_green": Colors.LIGHT_GREEN,
            "yellow": Colors.YELLOW,
            "light_blue": Colors.LIGHT_BLUE,
            "light_purple": Colors.LIGHT_PURPLE,
            "light_cyan": Colors.LIGHT_CYAN,
            "light_white": Colors.LIGHT_WHITE,
            "bright_red": Colors.BRIGHT_RED,
            "white": Colors.WHITE,
            # Text Formatting Styles
            "bold": Colors.BOLD,
            "faint": Colors.FAINT,
            "italic": Colors.ITALIC,
            "underline": Colors.UNDERLINE,
            "blink": Colors.BLINK,
            "negative": Colors.NEGATIVE,
            "crossed": Colors.CROSSED,
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
