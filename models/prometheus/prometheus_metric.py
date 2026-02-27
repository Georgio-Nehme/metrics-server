


class PrometheusMetric:
    def __init__(self, app, metric_name, labels, value):
        self.app = app
        self.metric_name = metric_name
        self.labels = labels
        self.value = value


    def __str__(self):
        label_str = ",".join([f'{k}="{v}"' for k, v in self.labels.items()])
        return f'{self.app}{self.metric_name}{{{label_str}}} {float(self.value)}\n'
