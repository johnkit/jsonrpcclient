"""Abstract base class for asynchronous clients"""
from abc import ABCMeta, abstractmethod

from future.utils import with_metaclass

from . import config
from .client import Client
from .request import Request, Notification
from .prepared_request import PreparedRequest

class AsyncClient(with_metaclass(ABCMeta, Client)):
    @abstractmethod
    async def _send_message(self, request, get_response, **kwargs):
        """Abstract"""

    async def send(self, request, get_response, **kwargs):
        request = PreparedRequest(request)
        self._prepare_request(request, **kwargs)
        if config.log_requests:
            self._log_request(request, request.log_extra, request.log_format)
        return await self._send_message(request, get_response, **kwargs)

    async def notify(self, method_name, *args, **kwargs):
        return await self.send(Notification(method_name, *args, **kwargs), False)

    async def request(self, method_name, *args, **kwargs):
        return await self.send(Request(method_name, *args, **kwargs), True)
