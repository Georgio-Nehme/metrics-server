from typing import List

from fastapi import FastAPI
from fastapi.responses import Response


from models.input_metric import InputMetric
from models.metric import Metric
from models.metrics_store import MetricStore
from tools.get_new_logs_settings import start_logger

my_logger = start_logger()
app = FastAPI()
store = MetricStore()

@app.get("/metrics")
async def expose_metrics():
    result = store.get_all_metrics()
    return Response(content="".join(result), media_type="text/plain")


@app.post("/push_metrics")
async def receive_metrics(metrics: List[InputMetric]):
    for item in metrics:
        metric = Metric(
            app_name=item.app_name,
            metric_name=item.metric_name,
            metric_type=item.metric_type,
            labels=item.labels,
        )
        if item.metric_type == "increment":
            metric.value = item.value
        elif item.metric_type == "collection":
            metric.metric_value = item.value
            metric.value = []
        elif item.metric_type == "static":
            metric.metric_value = item.value
            metric.value = item.value
        else:
            continue  # or raise an error
        store.add_or_merge(metric)
    return {"status": "ok", "message": f"Processed {len(metrics)} metrics."}

