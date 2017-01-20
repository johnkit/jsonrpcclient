"""Websockets http://websockets.readthedocs.io/"""
from .async_client import AsyncClient

class WebSocketsClient(AsyncClient):
    def __init__(self, socket):
        super(WebSocketsClient, self).__init__(None)
        self.socket = socket

    async def _send_message(self, request, get_response, **kwargs):
        await self.socket.send(request)
        if get_response:
            response = await self.socket.recv()
            return self._process_response(response)
