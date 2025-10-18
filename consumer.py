import time
import typer
from typing import Optional
from utils.logging_setup import setup_logging
from requests_source.s3_source import S3RequestSource
from storage.s3_store import S3WidgetStore
from storage.ddb_store import DDBWidgetStore

app = typer.Typer(no_args_is_help=True, add_completion=False)

@app.command()
def run(
    backend: str = typer.Option(..., help="s3 or ddb"),
    requests_bucket: str = typer.Option(..., help="Bucket 2: source of widget requests"),
    widgets_bucket: Optional[str] = typer.Option(None, help="Bucket 3: destination for widgets (s3 backend)"),
    widgets_table: Optional[str] = typer.Option(None, help="DynamoDB table (ddb backend)"),
    region: str = typer.Option("us-east-1"),
    profile: Optional[str] = typer.Option(None, help="AWS profile name (optional)"),
    poll_ms: int = typer.Option(100, help="Sleep when no work (ms)"),
    log_file: str = typer.Option("consumer.log")
):
    logger = setup_logging(log_file=log_file)
    logger.info("Starting HW6 consumer")
    logger.info(f"backend={backend} requests_bucket={requests_bucket} widgets_bucket={widgets_bucket} widgets_table={widgets_table}")

    source = S3RequestSource(bucket=requests_bucket, region=region, profile=profile, logger=logger)

    if backend.lower() == "s3":
        if not widgets_bucket:
            raise typer.BadParameter("--widgets-bucket required for s3 backend")
        store = S3WidgetStore(bucket=widgets_bucket, region=region, profile=profile, logger=logger)
    elif backend.lower() == "ddb":
        if not widgets_table:
            raise typer.BadParameter("--widgets-table required for ddb backend")
        store = DDBWidgetStore(table_name=widgets_table, region=region, profile=profile, logger=logger)
    else:
        raise typer.BadParameter("backend must be 's3' or 'ddb'")

    try:
        while True:
            req = source.get_next_request()
            if req is None:
                time.sleep(poll_ms / 1000.0)
                continue

            t = req.type.lower()
            if t in ("create", "widgetcreaterequest"):
                store.create(req)
            elif t in ("update", "widgetupdaterequest", "delete", "widgetdeleterequest"):
                logger.warning(f"{req.type} not implemented in HW6; skipping requestId={req.requestId}")
            else:
                logger.warning(f"Unknown request type {req.type}; skipping requestId={req.requestId}")
    except KeyboardInterrupt:
        logger.info("Shutting down (Ctrl-C)")

if __name__ == '__main__':
    app()
