import json
from typing import Optional
import boto3
from botocore.exceptions import ClientError
from models.widget import WidgetRequest
from .base import RequestSource

class S3RequestSource(RequestSource):
    def __init__(self, bucket: str, region: str, profile: str, logger):
        self.bucket = bucket
        self.logger = logger
        session = boto3.Session(profile_name=profile, region_name=region) if profile else boto3.Session(region_name=region)
        self.s3 = session.client("s3")

    def get_next_request(self) -> Optional[WidgetRequest]:
        try:
            resp = self.s3.list_objects_v2(Bucket=self.bucket, MaxKeys=1)
            contents = resp.get("Contents")
            if not contents:
                return None
            key = contents[0]["Key"]
            obj = self.s3.get_object(Bucket=self.bucket, Key=key)
            raw = obj["Body"].read().decode("utf-8")
            data = json.loads(raw)

            # get minimal required fields
            req = WidgetRequest(**data)
            req.validate_against_schema()

            # delete after validating
            self.s3.delete_object(Bucket=self.bucket, Key=key)
            self.logger.info(f"Consumed request key={key} requestId={req.requestId}")
            return req
        except ClientError as e:
            self.logger.error(f"S3 error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to parse request: {e}")
            return None
