import boto3
from botocore.exceptions import ClientError
from models.widget import WidgetRequest, flatten_widget_attributes
from .base import WidgetStore

class DDBWidgetStore(WidgetStore):
    def __init__(self, table_name: str, region: str, profile: str, logger):
        self.table_name = table_name
        self.logger = logger
        session = boto3.Session(profile_name=profile, region_name=region) if profile else boto3.Session(region_name=region)
        self.ddb = session.resource("dynamodb").Table(table_name)

    def create(self, req: WidgetRequest) -> None:
        item = flatten_widget_attributes(req)

        if "id" not in item:
            item["id"] = req.widgetId 

        try:
            self.ddb.put_item(Item=item)
            self.logger.info(f"PutItem widgetId={req.widgetId} owner={req.owner} into {self.table_name}")
        except ClientError as e:
            self.logger.error(f"DDB PutItem failed: {e}")
            raise
