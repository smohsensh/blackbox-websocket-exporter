from time import sleep
import logging
from prometheus_client import start_http_server, REGISTRY
from prometheus_client.metrics_core import GaugeMetricFamily

from websocket_exporter import settings
from .probe import WebSocketProbe


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class WebSocketUptimeCollector(object):
    def __init__(self, probe=None):
        if not probe:
            probe = WebSocketProbe(
                uri=settings.URI,
                message=settings.MESSAGE,
                expected=settings.EXPECTED_MESSAGE,
                match=settings.MATCH_TYPE,
                timeout=settings.TIMEOUT
            )
        self._probe = probe

    def collect(self):
        result = self._probe.probe()
        yield GaugeMetricFamily('websocket_probe_success', '1 if websocket is up 0 otherwise', value=result.up)
        yield GaugeMetricFamily(
            'websocket_probe_latency', 'latency in connection', value=result.latency, unit='milliseconds'
        )
        yield GaugeMetricFamily(
            'websocket_probe_received_expected_response',
            '1 if the expected message received after connection established 0 otherwise',
            value=result.received
        )


def main():
    assert settings.URI, 'URI to probe was not set, set "WEBSOCKET_EXPORTER_URI" env var'
    logging.info(f'Trying to start exporter, will probe {settings.URI}')
    if settings.MESSAGE:
        logging.info(f'sends {settings.MESSAGE} after connection')
    if settings.EXPECTED_MESSAGE:
        logging.info(f'waits for {settings.EXPECTED_MESSAGE} to match ({settings.MATCH_TYPE})')
        logging.info(f'Timeouts after {settings.TIMEOUT} seconds')
    REGISTRY.register(WebSocketUptimeCollector())
    logging.info(f'started exporter, listening on {settings.LISTEN_ADDR}:{settings.LISTEN_PORT}')
    start_http_server(port=settings.LISTEN_PORT, addr=settings.LISTEN_ADDR)
    while True:
        sleep(1)


if __name__ == '__main__':
    main()
