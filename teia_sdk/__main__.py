import typer

from .search import search


def main():
    app = typer.Typer()
    app.add_typer(search.app, name="search")
    app()


if __name__ == "__main__":
    main()
