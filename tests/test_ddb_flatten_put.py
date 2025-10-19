import boto3
from moto import mock_aws
from utils.logging_setup import setup_logging
from storage.ddb_store import DDBWidgetStore
from models.widget import WidgetRequest

@mock_aws
def test_ddb_put_flatten():
    region, profile = "us-east-1", None
    ddb = boto3.client("dynamodb", region_name=region)
    ddb.create_table(
        TableName="widgets",
        KeySchema=[{"AttributeName":"widgetId","KeyType":"HASH"}],
        AttributeDefinitions=[{"AttributeName":"widgetId","AttributeType":"S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    req = WidgetRequest(
        type="create", requestId="r1", widgetId="w1", owner="Alice",
        label="L", description="D", otherAttributes=[{"name":"color","value":"red"}]
    )
    logger = setup_logging()
    store = DDBWidgetStore("widgets", region, profile, logger)
    store.create(req)

    got = boto3.resource("dynamodb", region_name=region).Table("widgets").get_item(Key={"widgetId":"w1"})
    item = got["Item"]
    assert item["owner"] == "Alice" and item["label"] == "L" and item["color"] == "red"
