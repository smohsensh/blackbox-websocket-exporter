from time import sleep

from prometheus_client import start_http_server, REGISTRY
from prometheus_client.metrics_core import GaugeMetricFamily

from websocket_exporter import settings
from .probe import WebSocketProbe


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
    assert settings.URI, 'URI to probe was not set, set "WEBSOCKET_URI" env var'
    REGISTRY.register(WebSocketUptimeCollector())
    start_http_server(port=settings.LISTEN_PORT, addr=settings.LISTEN_ADDR)
    while True:
        sleep(1)


if __name__ == '__main__':
    main()
