import multiprocessing
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
@click.option(
    "--workers",
    type=int,
    default=None,
    help="Number of worker processes. Defaults to CPU count in prod.",
)
def main(env: str, debug: bool, workers: int | None) -> None:

    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)

    settings = get_settings()

    if env == "dev":
        num_workers = 1
    else:
        num_workers = workers or multiprocessing.cpu_count()

    uvicorn.run(
        app="app.server:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=(env == "dev"),
        workers=num_workers,
    )


if __name__ == "__main__":
    main()
