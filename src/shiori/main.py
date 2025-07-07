import os
import sys

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)


import click
import uvicorn
from app.core.config import get_settings


@click.command()
@click.option(
    "--env",
    type=click.Choice(["dev", "prod"], case_sensitive=False),
    default="dev",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
def main(env: str, debug: bool) -> None:

    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)

    settings = get_settings()

    uvicorn.run(
        app="app.server:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True if env == "dev" else False,
        workers=1,
    )


if __name__ == "__main__":
    main()
