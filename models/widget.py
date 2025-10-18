from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import json
from jsonschema import validate, ValidationError
from pathlib import Path
import json
from jsonschema import validate, ValidationError

_SCHEMA_PATH = Path(__file__).parent.parent / "widgetRequest-schema.json"  # put a copy next to repo root

def _schema() -> dict:
    try:
        return json.loads(_SCHEMA_PATH.read_text())
    except FileNotFoundError:
        raise RuntimeError(f"Schema file not found at {_SCHEMA_PATH}. Place widgetRequest-schema.json there.")

class OtherAttribute(BaseModel):
    name: str
    value: str

class WidgetRequest(BaseModel):
    type: str = Field(..., description="create|update|delete or WidgetCreateRequest|WidgetUpdateRequest|WidgetDeleteRequest")
    requestId: str
    widgetId: str
    owner: str
    label: Optional[str] = None
    description: Optional[str] = None
    otherAttributes: Optional[List[OtherAttribute]] = None

    def validate_against_schema(self) -> None:
        try:
            validate(self.model_dump(), _schema())
        except ValidationError as e:
            raise ValueError(f"Schema validation failed: {e.message} at path {e.json_path}")

def flatten_widget_attributes(req: WidgetRequest) -> Dict[str, Any]:
    """Flatten a create request into a flat dict of attributes for DDB.
    otherAttributes -> top-level keys.
    """
    out: Dict[str, Any] = {}
    out["widgetId"] = req.widgetId
    out["owner"] = req.owner
    if req.label is not None:
        out["label"] = req.label
    if req.description is not None:
        out["description"] = req.description
    if req.otherAttributes:
        for oa in req.otherAttributes:
            # updates can overwrite same keys
            out[oa.name] = oa.value
    return out
