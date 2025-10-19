import json
import boto3
from utils.key_utils import normalize_owner
from models.widget import WidgetRequest
from .base import WidgetStore

class S3WidgetStore(WidgetStore):
    def __init__(self, bucket: str, region: str, profile: str, logger):
        self.bucket = bucket
        self.logger = logger
        session = boto3.Session(profile_name=profile, region_name=region) if profile else boto3.Session(region_name=region)
        self.s3 = session.client("s3")

    def create(self, req: WidgetRequest) -> None:
        owner_key = normalize_owner(req.owner)
        key = f"widgets/{owner_key}/{req.widgetId}"
        body = json.dumps(req.model_dump(exclude_none=True))
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=body.encode("utf-8"), ContentType="application/json")
        self.logger.info(f"Wrote widget to s3://{self.bucket}/{key}")
