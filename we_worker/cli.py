from typing_extensions import Annotated
import typer
from rich import print

from .settings import get_settings
from .celery import celery_app
from .logging import configure_logging

app = typer.Typer()


@app.command()
def run_we_worker(
    num_procs: Annotated[int, typer.Option("--num-procs", "-p", help="number of worker processes")] = None,
):
    configure_logging()
    settings = get_settings()
    print("[green]Running worker[/green]")
    print(settings.broker_url)

    argv = ["worker", "--loglevel=info", "--without-gossip"]
    if num_procs:
        print(f"Running worker with {num_procs} processes")
        argv.append(f"--concurrency={num_procs}")
    else:
        print("Running worker")

    print(argv)
    celery_app.worker_main(argv)


def main():
    app()
