from typing import Optional
from urllib.parse import urlparse

from aiohttp import ClientSession, ClientResponse

from ._decos import require_session
from .errors import *
from .enums import *


def _process_resp(resp: ClientResponse) -> None:
    if resp.ok:
        return None
    else:
        raise HTTPException(resp.reason, status_code=resp.status)


class AsyncEasyGTTSSession:
    """An interface with the easy Text-To-Speech API.

    A JSONWebTokenHandler must be passed, to provide headers to the ClientSession.

    A ClientSession can also be passed, which will be used to make requests. This is useful for connection pooling."""

    def __init__(
        self, 
        endpoint: str = "https://easy-gtts-api.dingus-server.regulad.xyz/", 
        *, 
        client_session: ClientSession = None
    ):
        parsed_endpoint = urlparse(endpoint)

        self._endpoint = f"{parsed_endpoint.scheme}://{parsed_endpoint.netloc}/"

        self.client_session = client_session
        self._client_session_is_passed = self.client_session is not None

    async def __aenter__(self):
        if not self._client_session_is_passed:
            self.client_session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._client_session_is_passed:
            await self.client_session.close()

    @require_session
    async def synthesize(
            self,
            text: str,
            lang: str = "en-US",
            voice: str = "en-US-Wavenet-D",
            encoding: AudioEncoding = AudioEncoding.MP3
    ) -> bytes:
        """Synthesizes text using the /v1beta1/synthesize endpoint."""

        query_params = {
            "lang": lang,
            "voice": voice,
            "encoding": encoding.value,
            "text": text,
        }

        async with self.client_session.get(f"{self._endpoint}v1beta1/synthesize", params=query_params) as resp:
            _process_resp(resp)

            return await resp.read()

    @require_session
    async def list(self, language_code: Optional[str] = None):
        """Returns a list of voices from the /v1beta1/list endpoint."""

        if language_code is not None:
            query_params = {"languageCode": language_code}
        else:
            query_params = {}

        async with self.client_session.get(f"{self._endpoint}v1beta1/voices", params=query_params) as resp:
            _process_resp(resp)

            return await resp.json()


__all__ = ["AsyncEasyGTTSSession"]
