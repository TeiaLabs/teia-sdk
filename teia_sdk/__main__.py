import typer

from .melting import chat_prompts
from .search import search


def main():
    app = typer.Typer()
    app.add_typer(search.app, name="search")
    app.add_typer(chat_prompts.app, name="chat-prompts")
    app()


if __name__ == "__main__":
    main()
