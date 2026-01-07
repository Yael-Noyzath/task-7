from pathlib import Path
import typer
from .watcher import FileWatcher
from .config import Config
from .state import State
from .uploader import Uploader

app = typer.Typer(help="Enter directory path - watches a directory and uploads new files")

@app.command()
def start_watch(
    watch_dir: str = typer.Option(
       ...,
        "--watch-dir",
        exists=True,
        file_okay=False,
        dir_okay=True,
        help="Directory to watch for file changes")
        ):
        #נתיב
        watch_dir = Path(watch_dir).expanduser().resolve()
        cng = Config()
        state = State()
        watcher = FileWatcher(watch_dir, state)
        uploader = Uploader(cng.data["server_url"],state)
        typer.echo("Starting file upload client")
        typer.echo(f"Watching directory: {watch_dir}")
        try:
            for files in watcher.watch():
                for file_path in files:
                    uploader.upload_file(file_path)
        except KeyboardInterrupt:
            typer.echo("\nClient stopped by user")

if __name__ == "__main__":
    app()