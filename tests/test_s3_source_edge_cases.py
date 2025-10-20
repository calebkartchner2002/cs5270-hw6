import json, boto3
from moto import mock_aws
from utils.logging_setup import setup_logging
from requests_source.s3_source import S3RequestSource

BUCKET2 = "usu-cs5270-sky-requests"

@mock_aws
def test_empty_bucket_returns_none(tmp_path):
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=BUCKET2)
    logger = setup_logging(log_file=str(tmp_path/"log.txt"))
    src = S3RequestSource(BUCKET2, "us-east-1", None, logger)
    assert src.get_next_request() is None

@mock_aws
def test_lexicographic_order(tmp_path):
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=BUCKET2)
    good = lambda rid, wid, owner: {
        "type":"WidgetCreateRequest","requestId":rid,"widgetId":wid,"owner":owner
    }
    s3.put_object(Bucket=BUCKET2, Key="0002.json", Body=json.dumps(good("r2","w2","B B")).encode())
    s3.put_object(Bucket=BUCKET2, Key="0001.json", Body=json.dumps(good("r1","w1","A A")).encode())

    logger = setup_logging(log_file=str(tmp_path/"log.txt"))
    src = S3RequestSource(BUCKET2, "us-east-1", None, logger)
    first = src.get_next_request()
    assert first and first.requestId == "r1"

@mock_aws
def test_bad_json_not_deleted(tmp_path):
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=BUCKET2)
    s3.put_object(Bucket=BUCKET2, Key="0001.json", Body=b"{not-json")
    logger = setup_logging(log_file=str(tmp_path/"log.txt"))
    src = S3RequestSource(BUCKET2, "us-east-1", None, logger)
    assert src.get_next_request() is None
    # still present
    assert "Contents" in s3.list_objects_v2(Bucket=BUCKET2)

@mock_aws
def test_schema_violation_not_deleted(tmp_path):
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=BUCKET2)
    bad = {"type":"WidgetCreateRequest","requestId":"r1","widgetId":"w1"}  # missing owner
    s3.put_object(Bucket=BUCKET2, Key="0001.json", Body=json.dumps(bad).encode())
    logger = setup_logging(log_file=str(tmp_path/"log.txt"))
    src = S3RequestSource(BUCKET2, "us-east-1", None, logger)
    assert src.get_next_request() is None
    assert "Contents" in s3.list_objects_v2(Bucket=BUCKET2)
