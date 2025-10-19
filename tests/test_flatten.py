from models.widget import WidgetRequest, flatten_widget_attributes

def test_flatten_basic():
    req = WidgetRequest(
        type="create",
        requestId="r1",
        widgetId="w1",
        owner="Alice Smith",
        label="L",
        description="D",
        otherAttributes=[{"name":"color","value":"red"},{"name":"size","value":"xl"}]
    )
    out = flatten_widget_attributes(req)
    assert out["widgetId"] == "w1"
    assert out["owner"] == "Alice Smith"
    assert out["label"] == "L"
    assert out["description"] == "D"
    assert out["color"] == "red"
    assert out["size"] == "xl"
