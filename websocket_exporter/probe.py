import asyncio
import logging
from time import perf_counter
from typing import Union

from websockets import NegotiationError, client, InvalidStatusCode


EXACT_MATCH = 'exact'
CONTAINS_MATCH = 'contains'


class ProbResults(object):
    def __init__(self, up: int, latency: float = 0, received: int = 0):
        self.up = up
        self.latency = round(latency, 2)
        self.received = int(received) if received is not None else "NaN"

    def __str__(self):
        if self.up:
            return f'Websocket up, latency:{self.latency}s, expected response {"" if self.received else "NOT"} received'
        return f'Webserver DOWN'


class WebSocketProbe(object):

    def __init__(self, uri, message=None, expected=None, match=CONTAINS_MATCH, timeout=10):
        """
        Create a websocket probe that tries establishing a connection and reports the metrics
        :param uri: starts with 'ws://' or ws://
        :param message: optional message to send to server
        :param expected: (optional) response to expect for the server
        :param match_contains: weather match the expected response exactly or response should contain this only
        """
        self.uri = uri
        self.message = message
        self.expected_message = expected
        self.match = match
        self.timeout = timeout

    def probe(self) -> ProbResults:
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        future_instance = asyncio.ensure_future(self._connect_and_get())
        result = event_loop.run_until_complete(future_instance)
        event_loop.close()
        return result

    async def _connect_and_get(self) -> ProbResults:
        socket = None
        received = None
        try:
            start = perf_counter()
            socket = await client.connect(self.uri, timeout=self.timeout)
            latency_ms = (perf_counter() - start) * 1000
            if self.message:
                await socket.send(self.message)
            if self.expected_message:
                received = await self._await_expected_response(socket)
            await socket.close()
            return ProbResults(up=True, latency=latency_ms, received=received)
        except (NegotiationError, InvalidStatusCode):
            if socket:
                await socket.wait_closed()
            return ProbResults(up=False)

    async def _await_expected_response(self, connection) -> Union[bool, None]:
        elapsed = 0
        while elapsed < self.timeout:
            try:
                resp = await asyncio.wait_for(connection.recv(), timeout=(self.timeout-elapsed))
                if self._match(resp):
                    return True
                await asyncio.sleep(1)
                elapsed += 1
            except asyncio.TimeoutError:
                logging.info(f'Time out while waiting for {self.expected_message} from {self.uri}')
                return None
        return None

    def _match(self, resp: str) -> bool:
        if self.match == EXACT_MATCH:
            return resp == self.expected_message
        elif self.match == CONTAINS_MATCH:
            return self.expected_message in resp
        return False
