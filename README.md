
# Blackbox Websocket Uptime Prometheus Exporter

A blackbox exporter to check health of websocket connection. 

## Usage

install with `python setup.py install`

configuration are done with environment variables. Run with `websocket_exporter`

## Configuration

Env Var     | Description
--------------------|---------------------------
WEBSOCKET_EXPORTER_URI | URI of websoccket connection to check, starts with `ws(s)://`
WEBSOCKET_EXPORTER_MESSAGE | Optional message to send after connection established
WEBSOCKET_EXPORTER_EXPECTED_MESSAGE | Optional message to expect to be received from server after connection
WEBSOCKET_EXPORTER_MATCH_TYPE | How to match expected message (either `contains` or `exact`)
WEBSOCKET_EXPORTER_TIMEOUT | How long to wait for the connection to be established in seconds (default: 10)
WEBSOCKET_EXPORTER_LISTEN_ADDR | What address to listen (defaults `0.0.0.0`)
WEBSOCKET_EXPORTER_LISTEN_PORT | What port to listen (defaults `9802`)


## Metrics

- `websocket_probe_success`: if the connection established successfully (`0/1`)
- `websocket_probe_latency_milliseconds`: Connection Latency
- `websocket_probe_received_expected_response`: if expected message was received through the websocket connection

## Run in Docker 

docker build : ``` docker build . -t blackbox-websocket-exporter:latest ```

docker run : ``` docker run -it -e WEBSOCKET_EXPORTER_URI=ws(s)://example.com blackbox-websocket-exporter:latest ```

docker compose : ``` docker compose up -d ```

also, this image is available on the docker hub :  ``` docker pull foxmanx2000/blackbox-websocket-exporter:latest ```


## Future Development
This exporter is still quite young and there are a handful of features that can be added soon:
- Deployment via Docker
- Command line arguments config to override env vars
- Probe multiple targets
- A static intro and doc in the base url of the exporter
- Richer Readme with Grafana examples  
