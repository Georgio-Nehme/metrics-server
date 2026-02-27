from models.metric import Metric
from models.prometheus.prometheus_metric import PrometheusMetric


class MetricStore:
    def __init__(self):
        self.metrics = {}

    def _generate_key(self, metric: Metric) -> tuple:
        return (metric.app_name, metric.metric_name, metric.metric_type, frozenset(metric.labels.items()))

    def add_or_merge(self, metric: Metric):
        key = self._generate_key(metric)
        if metric.metric_type == "increment":
            if key in self.metrics:
                self.metrics[key].value += metric.value
            else:
                self.metrics[key] = metric

        elif metric.metric_type == "static":
            if key in self.metrics:
                self.metrics[key].value = metric.value
            else:
                self.metrics[key] = metric

        elif metric.metric_type == "collection":
            metric_value = getattr(metric, "metric_value", metric.value)
            if key not in self.metrics:
                self.metrics[key] = metric
                self.metrics[key].value = []
            self.metrics[key].value.append(metric_value)

    def generate_collection_metrics(self):
        new_metrics = []
        for key, metric in list(self.metrics.items()):
            if metric.metric_type == "collection":
                values = metric.value
                labels = metric.labels
                if values:
                    min_metric = Metric(
                        app_name=metric.app_name,
                        metric_name=metric.metric_name,
                        metric_type=metric.metric_type,
                        labels=labels.copy()
                    )
                    max_metric = Metric(
                        app_name=metric.app_name,
                        metric_name=metric.metric_name,
                        metric_type=metric.metric_type,
                        labels=labels.copy()
                    )
                    avg_metric = Metric(
                        app_name=metric.app_name,
                        metric_name=metric.metric_name,
                        metric_type=metric.metric_type,
                        labels=labels.copy()
                    )

                    min_metric.value = min(values)
                    max_metric.value = max(values)
                    avg_metric.value = sum(values) / len(values)

                    min_metric.add_label('stat', 'min')
                    max_metric.add_label('stat', 'max')
                    avg_metric.add_label('stat', 'avg')

                    new_metrics.extend([min_metric, max_metric, avg_metric])

        self.metrics.clear()
        return new_metrics


    def get_all_metrics(self) -> list:
        prom_metrics = []
        simple_metrics = [m for m in self.metrics.values() if m.metric_type != "collection"]
        derived_metrics = self.generate_collection_metrics()


        for metric in simple_metrics + derived_metrics:

            prom_metric = PrometheusMetric(
                app=metric.app_name,
                metric_name=metric.metric_name,
                labels=metric.labels,
                value=metric.value
            )
            str_metric = str(prom_metric)
            prom_metrics.append(str_metric)

        return prom_metrics
