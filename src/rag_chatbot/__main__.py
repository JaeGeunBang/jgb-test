import sys

from .chatbot import Chatbot
from .config import load_config
from .exceptions import ConfigError


def main() -> None:
    try:
        config = load_config()
    except ConfigError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)

    chatbot = Chatbot(config)
    chatbot.run_cli()


if __name__ == "__main__":
    main()
