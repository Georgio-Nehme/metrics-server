from typing import Dict


class Metric:
    def __init__(self, app_name: str, metric_name: str, metric_type: str, labels: Dict[str, str], value=0):
        self.app_name: str = app_name
        self.metric_name: str = metric_name
        self.metric_type: str = metric_type
        self.labels: dict = labels
        self.metric_value: float = value
        self.value = 0 if self.metric_type == "increment" else []

    def add_label(self, key, value):
        self.labels.update({key: value})
