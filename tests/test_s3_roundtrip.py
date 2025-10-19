import json, boto3
from moto import mock_aws
from utils.logging_setup import setup_logging
from requests_source.s3_source import S3RequestSource
from storage.s3_store import S3WidgetStore

@mock_aws
def test_s3_source_and_store_roundtrip(tmp_path):
    region, profile = "us-east-1", None
    req_bucket = "bucket-2-requests"
    out_bucket = "bucket-3-website"

    s3 = boto3.client("s3", region_name=region)
    s3.create_bucket(Bucket=req_bucket)
    s3.create_bucket(Bucket=out_bucket)

    req = {
        "type":"create","requestId":"r1","widgetId":"w1","owner":"Alice Smith",
        "label":"L","otherAttributes":[{"name":"color","value":"green"}]
    }
    s3.put_object(Bucket=req_bucket, Key="0001.json", Body=json.dumps(req).encode())

    logger = setup_logging(log_file=str(tmp_path/"consumer.log"))
    source = S3RequestSource(req_bucket, region, profile, logger)
    store = S3WidgetStore(out_bucket, region, profile, logger)

    got = source.get_next_request()
    assert got is not None and got.requestId == "r1"

    store.create(got)

    # request deleted
    assert "Contents" not in s3.list_objects_v2(Bucket=req_bucket)
    # widget written
    out_key = "widgets/alice-smith/w1"
    body = s3.get_object(Bucket=out_bucket, Key=out_key)["Body"].read().decode()
    data = json.loads(body)
    assert data["owner"] == "Alice Smith" and data["widgetId"] == "w1"
