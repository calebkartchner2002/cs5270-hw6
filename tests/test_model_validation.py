from models.widget import WidgetRequest, flatten_widget_attributes

def test_type_alias_and_exclude_none():
    req = WidgetRequest(type="create", requestId="r", widgetId="w", owner="Alice", description=None)
    req.validate_against_schema()

def test_other_attributes_last_wins():
    req = WidgetRequest(
        type="create", requestId="r", widgetId="w", owner="Alice",
        otherAttributes=[{"name":"color","value":"red"},{"name":"color","value":"blue"}]
    )
    item = flatten_widget_attributes(req)
    assert item["color"] == "blue"
