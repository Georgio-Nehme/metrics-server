from typing import Dict, Union

from pydantic import BaseModel


class InputMetric(BaseModel):
    app_name: str
    metric_name: str
    metric_type: str
    labels: Dict[str, str]
    value: Union[int, float]
