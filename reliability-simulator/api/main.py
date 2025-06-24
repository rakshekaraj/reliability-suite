from fastapi import FastAPI, Request
from prometheus_client import start_http_server, Summary, Counter
import random, time
import threading

app = FastAPI()

# METRICS
REQUEST_TIME = Summary('ping_latency_seconds', 'Time spent processing /ping')
REQUEST_COUNT = Counter('ping_requests_total', 'Total number of /ping requests')

# Expose Prometheus metrics on a separate port (8001)
def start_metrics_server():
    start_http_server(8001)

threading.Thread(target=start_metrics_server).start()

@app.get("/ping")
@REQUEST_TIME.time()
def ping():
    REQUEST_COUNT.inc()
    delay = random.uniform(0, 1.5)
    time.sleep(delay)
    return {"message": "pong", "delay": delay}
