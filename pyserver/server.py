import http.server
import random
import time
from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary


REQUESTS = Counter('hello_worlds_total',
          'Hello Worlds requested.')

SALES = Counter('hello_world_sales_euro_total',
          'Euros made serving Hello World.')

EXCEPTIONS = Counter('hello_world_exceptions_total',
            'Exceptions serving Hello World.')

INPROGRESS = Gauge('Hello_worlds_inprogress',
                'Number of Hello Worlds in progress.')

LAST = Gauge('Hello_world_last_time_seconds',
            'The last time a Hello World was served.')

LATENCY = Summary('hello_world_latency_seconds',
            'Time for a request Hello World.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    @INPROGRESS.track_inprogress()
    def do_GET(self):
        start = time.time()
        REQUESTS.inc()
        # INPROGRESS.inc()
        with EXCEPTIONS.count_exceptions():
            if random.random() < 0.2:
                # INPROGRESS.dec()
                LATENCY.observe(time.time() - start)
                raise Exception
                
        euros = random.random()
        SALES.inc(euros)
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Hello World for {} euros.".format(euros).encode())
        # LAST.set(time.time())
        LAST.set_to_current_time()
        # INPROGRESS.dec() 
        LATENCY.observe(time.time() - start)

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('0.0.0.0', 8001), MyHandler)
    server.serve_forever()