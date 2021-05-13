import logging


from aiohttp.typedefs import StrOrURL
from aiohttp import ClientSession


class LoggedSession(ClientSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._logger = logging.getLogger(__name__)

    async def _request(self, method: str, str_or_url: StrOrURL, *args, **kwargs):
        response = await super()._request(method, str_or_url, *args, **kwargs)

        self._logger.info(f'{method} {str_or_url} -> {response.status}')

        return response
