from prometheus_client import Counter, Histogram
from flask import request
import time

# Metrics definitions
REQUEST_COUNT = Counter(
    'app_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Application Request Latency',
    ['method', 'endpoint']
)

def before_request():
    request.start_time = time.time()

def after_request(response):
    # Only measure latency if start_time is set
    if hasattr(request, 'start_time'):
        request_latency = time.time() - request.start_time
        # Use request.endpoint if available, else request.path
        endpoint = request.endpoint if request.endpoint else request.path
        REQUEST_LATENCY.labels(request.method, endpoint).observe(request_latency)
        
    endpoint = request.endpoint if request.endpoint else request.path
    REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    return response

def setup_metrics(app):
    app.before_request(before_request)
    app.after_request(after_request)
